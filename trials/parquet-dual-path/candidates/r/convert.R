#!/usr/bin/env Rscript
suppressPackageStartupMessages({library(arrow); library(haven); library(jsonlite)})
fail <- function(message) stop(message, call. = FALSE)
need <- function(ok, message) if (!isTRUE(ok)) fail(message)
scalar <- function(x, type) length(x) == 1L && !is.na(x) && typeof(x) %in% type
string <- function(x) scalar(x, "character")
object <- function(x) is.list(x) && (length(x) == 0L || (!is.null(names(x)) && !anyDuplicated(names(x))))
sha <- function(path) {
  need(file.exists(path) && !dir.exists(path), paste("Missing file:", path))
  result <- system2("sha256sum", c("--", shQuote(normalizePath(path))), stdout = TRUE, stderr = TRUE)
  need(is.null(attr(result, "status")) && length(result) == 1L && grepl("^[a-f0-9]{64} ", result), "sha256sum failed")
  substr(result, 1L, 64L)
}
read_json <- function(path) fromJSON(path, simplifyVector = FALSE)
json_text <- function(x) toJSON(x, auto_unbox = TRUE, null = "null", na = "null", digits = NA, pretty = TRUE)
json_equal <- function(a, b) identical(json_text(a), json_text(b))
canonical_tag <- function(x) {
  if (!is.na(x) && is_tagged_na(x)) paste0(".", toupper(na_tag(x))) else if (is.na(x)) {
    tag <- na_tag(x)
    if (is.na(tag)) "." else paste0(".", toupper(tag))
  } else ""
}
check_names <- function(nms) {
  need(!anyNA(nms) && !anyDuplicated(nms) && all(nzchar(nms)), "Invalid or duplicate source names")
  need(!any(nms == "__row_index" | endsWith(nms, "__sas_missing")), "Reserved source name")
}
hex_raw <- function(x) if (!nzchar(x)) raw() else as.raw(strtoi(substring(x, seq(1L, nchar(x), 2L), seq(2L, nchar(x), 2L)), 16L))
raw_hex <- function(x) paste(sprintf("%02x", as.integer(x)), collapse = "")
normalize_character <- function(hex, encoding) {
  bytes <- hex_raw(hex)
  if (any(bytes == as.raw(0))) return(list(value = NA_character_, action = "embedded-nul"))
  codec <- tolower(gsub("_", "-", encoding, fixed = TRUE))
  if (codec %in% c("windows-1252", "cp1252", "cp-1252") && any(as.integer(bytes) %in% c(129, 141, 143, 144, 157))) return(list(value = NA_character_, action = "decode-error"))
  decoded <- iconv(rawToChar(bytes), from = encoding, to = "UTF-8", sub = NA)
  if (is.na(decoded)) return(list(value = NA_character_, action = "decode-error"))
  trimmed <- sub(" +$", "", decoded, perl = TRUE)
  if (!nzchar(trimmed)) return(list(value = NA_character_, action = "blank-to-null"))
  list(value = trimmed, action = if (!identical(trimmed, decoded)) "right-trim" else NULL)
}
read_envelope <- function(input, catalog) {
  need(is.null(catalog), "A catalog is supported only for SAS inputs")
  x <- read_json(input)
  need(object(x) && identical(x$version, 1L) && string(x$encoding), "Invalid envelope header")
  need(is.null(x$timezone), "This profile requires an unknown timezone")
  need(!is.null(iconv("a", from = x$encoding, to = "UTF-8", sub = NA)), "Unsupported codec")
  need(is.list(x$columns) && is.null(names(x$columns)) && is.list(x$rows) && is.null(names(x$rows)), "Columns and rows must be arrays")
  required <- c("name", "kind", "logical", "width_bytes", "label", "format", "informat", "origin", "units", "timezone", "value_labels")
  for (d in x$columns) {
    need(object(d) && all(required %in% names(d)), "Incomplete descriptor")
    need(string(d$name) && string(d$kind) && string(d$logical), "Invalid descriptor strings")
    need(d$kind %in% c("numeric", "character"), "Unsupported source kind")
    need(d$logical %in% if (d$kind == "numeric") c("number", "date", "datetime", "time") else "text", "Unsupported logical kind")
    need(scalar(d$width_bytes, c("integer", "double")) && is.finite(d$width_bytes) && d$width_bytes >= 0 && d$width_bytes == floor(d$width_bytes), "Invalid byte width")
    for (key in c("label", "format", "informat", "origin", "units")) need(is.null(d[[key]]) || string(d[[key]]), paste("Invalid descriptor", key))
    need(is.null(d$timezone), "This profile requires an unknown timezone")
    need(is.null(d$value_labels) || (object(d$value_labels) && all(vapply(d$value_labels, string, logical(1)))), "Invalid value labels")
    if (d$logical == "date") need(identical(d$origin, "1960-01-01") && identical(d$units, "days"), "Invalid date units or origin")
    if (d$logical == "datetime") need(identical(d$origin, "1960-01-01T00:00:00") && identical(d$units, "seconds"), "Invalid datetime units or origin")
    if (d$logical == "time") need(identical(d$units, "seconds"), "Invalid time units")
  }
  nms <- vapply(x$columns, `[[`, "", "name")
  check_names(nms)
  for (row in x$rows) {
    need(object(row) && setequal(names(row), nms) && length(row) == length(nms), "Row fields differ from descriptors")
    for (d in x$columns) {
      cell <- row[[d$name]]
      need(object(cell) && length(cell) == 1L, "Invalid cell")
      if (d$kind == "character") {
        need(identical(names(cell), "hex") && string(cell$hex) && grepl("^([0-9a-f]{2})*$", cell$hex) && nchar(cell$hex, type = "bytes") == 2 * d$width_bytes, "Invalid character bytes or width")
      } else if (identical(names(cell), "value")) {
        need(scalar(cell$value, c("integer", "double")) && is.finite(cell$value), "Invalid finite numeric value")
        if (d$logical == "date") need(cell$value == floor(cell$value) && cell$value - 3653 >= -2147483648 && cell$value - 3653 <= 2147483647, "Date is not representable as date32")
        if (d$logical == "datetime") need(abs((cell$value - 315619200) * 1e6) <= 2^53, "Timestamp exceeds exact native microsecond range")
      } else need(identical(names(cell), "missing") && string(cell$missing) && grepl("^\\.([A-Z_])?$", cell$missing), "Invalid numeric missing marker")
    }
  }
  list(source_format = "envelope", encoding = x$encoding, fidelity = "exact-envelope-bytes", columns = x$columns, rows = x$rows, dataset_label = x$dataset_label, gaps = character())
}
format_kind <- function(fmt) {
  if (is.null(fmt)) return("number")
  fmt <- toupper(fmt)
  if (grepl("^DATETIME([0-9]+)?(\\.[0-9]+)?\\.?$", fmt)) return("datetime")
  if (grepl("^(DATE|YYMMDD)([0-9]+)?\\.?$", fmt)) return("date")
  if (grepl("^TIME([0-9]+)?(\\.[0-9]+)?\\.?$", fmt)) return("time")
  "number"
}
read_sas_source <- function(input, catalog) {
  data <- read_sas(input, catalog_file = catalog, .name_repair = "minimal")
  check_names(names(data))
  columns <- list(); values <- list()
  for (nm in names(data)) {
    v <- data[[nm]]
    kind <- if (is.character(v)) "character" else "numeric"
    need(kind == "character" || typeof(v) %in% c("double", "integer"), "Unsupported SAS reader type")
    fmt <- attr(v, "format.sas", exact = TRUE)
    logical <- if (kind == "character") "text" else format_kind(fmt)
    labels <- attr(v, "labels", exact = TRUE)
    value_labels <- NULL
    if (!is.null(labels)) {
      keys <- vapply(seq_along(labels), function(i) if (is.numeric(labels)) {
        if (is.na(labels[i])) canonical_tag(labels[i]) else format(as.double(labels[i]), digits = 17, trim = TRUE, scientific = FALSE)
      } else as.character(labels[i]), "")
      need(!anyDuplicated(keys), "Duplicate value label keys")
      value_labels <- setNames(as.list(names(labels)), keys)
    }
    columns[[length(columns) + 1L]] <- list(name = nm, kind = kind, logical = logical, width_bytes = NULL, label = attr(v, "label", exact = TRUE), format = fmt, informat = NULL, origin = if (logical == "date") "1960-01-01" else if (logical == "datetime") "1960-01-01T00:00:00" else NULL, units = if (logical == "date") "days" else if (logical %in% c("datetime", "time")) "seconds" else NULL, timezone = NULL, value_labels = value_labels)
    if (kind == "character") {
      need(!anyNA(v), "SAS reader returned unavailable character values")
      values[[nm]] <- lapply(v, function(s) list(hex = raw_hex(charToRaw(enc2utf8(s)))))
    } else {
      raw <- as.double(v)
      values[[nm]] <- lapply(seq_along(raw), function(i) {
        if (is.na(raw[i])) return(list(missing = canonical_tag(raw[i])))
        z <- raw[i]
        if (inherits(v, "Date")) z <- z + 3653
        if (inherits(v, "POSIXct")) z <- z + 315619200
        need(is.finite(z), "Nonfinite source numeric value")
        list(value = z)
      })
    }
  }
  rows <- lapply(seq_len(nrow(data)), function(i) setNames(lapply(names(data), function(nm) values[[nm]][[i]]), names(data)))
  list(source_format = "sas7bdat", encoding = NULL, fidelity = "reader-utf8-reencoding", columns = columns, rows = rows, dataset_label = attr(data, "label", exact = TRUE), gaps = c("haven does not expose source encoding, original byte widths or informats on this path; these remain null", "Character data is reader-decoded UTF-8 reencoding, not original SAS physical bytes or padding", "Date/time interpretation uses an explicit DATE, YYMMDD, DATETIME, TIME format profile; reader UTC display attributes are not source timezone evidence"))
}
read_source <- function(input, catalog) {
  sha(input)
  if (!is.null(catalog)) sha(catalog)
  if (grepl("\\.sas7bdat$", input, ignore.case = TRUE)) read_sas_source(input, catalog) else read_envelope(input, catalog)
}
source_entries <- function(input, catalog) {
  paths <- c(input, catalog)
  roles <- c("data", if (!is.null(catalog)) "catalog")
  license <- file.path(dirname(input), "LICENSE")
  if (file.exists(license)) { paths <- c(paths, license); roles <- c(roles, "license") }
  need(!anyDuplicated(basename(paths)), "Retained source basenames collide")
  entries <- lapply(seq_along(paths), function(i) list(role = roles[i], path = paste0("source/", basename(paths[i])), sha256 = sha(paths[i])))
  list(paths = paths, entries = entries)
}
make_projection <- function(src, entries, mode) {
  n <- length(src$rows)
  arrays <- setNames(list(Array$create(as.double(seq_len(n) - 1L), type = int64())), "__row_index")
  events <- list()
  for (d in src$columns) {
    nm <- d$name
    if (d$kind == "character") {
      hex <- vapply(src$rows, function(r) r[[nm]]$hex, "")
      norm <- lapply(hex, normalize_character, encoding = if (src$source_format == "envelope") src$encoding else "UTF-8")
      values <- if (mode == "archive") hex else vapply(norm, `[[`, "", "value")
      arrays[[nm]] <- Array$create(values, type = utf8())
      if (mode == "analysis") for (i in seq_len(n)) if (!is.null(norm[[i]]$action)) events[[length(events) + 1L]] <- list(row = i - 1L, column = nm, action = norm[[i]]$action)
    } else {
      values <- vapply(src$rows, function(r) if (is.null(r[[nm]]$value)) NA_real_ else as.double(r[[nm]]$value), 0)
      tags <- vapply(src$rows, function(r) if (is.null(r[[nm]]$missing)) "" else r[[nm]]$missing, "")
      if (mode == "archive") {
        arrays[[nm]] <- Array$create(values, type = float64())
        arrays[[paste0(nm, "__sas_missing")]] <- Array$create(tags, type = utf8())
      } else {
        if (d$logical == "date") arrays[[nm]] <- Array$create(values - 3653, type = int32())$cast(date32())
        else if (d$logical == "datetime") arrays[[nm]] <- Array$create(round((values - 315619200) * 1e6), type = int64())$cast(timestamp("us"))
        else arrays[[nm]] <- Array$create(values, type = float64())
        for (i in seq_len(n)) {
          event <- NULL
          if (nzchar(tags[i])) event <- list(row = i - 1L, column = nm, action = "missing-to-null", tag = tags[i])
          else if (d$logical == "date") event <- list(row = i - 1L, column = nm, action = "date-to-date32")
          else if (d$logical == "datetime") event <- list(row = i - 1L, column = nm, action = "datetime-to-timestamp-us")
          if (!is.null(event)) events[[length(events) + 1L]] <- event
        }
      }
    }
  }
  original_names <- names(arrays)
  names(arrays) <- paste0("field", seq_along(arrays))
  table <- do.call(Table$create, arrays)$RenameColumns(original_names)
  metadata <- list(saschi.source_sha256 = entries[[1L]]$sha256, saschi.catalog_sha256 = "", saschi.mode = mode, saschi.schema_version = "1")
  for (e in entries) if (e$role == "catalog") metadata$saschi.catalog_sha256 <- e$sha256
  table <- table$ReplaceSchemaMetadata(metadata)
  if (length(events)) {
    order_events <- order(vapply(events, `[[`, 0L, "row"), match(vapply(events, `[[`, "", "column"), vapply(src$columns, `[[`, "", "name")))
    events <- events[order_events]
  }
  list(table = table, events = events)
}
make_metadata <- function(src, entries, events, files) list(schema_version = 1L, source_format = src$source_format, row_count = length(src$rows), source_files = entries, source_encoding = src$encoding, character_fidelity = src$fidelity, catalog_status = if (any(vapply(entries, function(e) e$role == "catalog", logical(1)))) "provided" else "absent", timezone = NULL, columns = src$columns, events = events, files = files, libraries = list(R = as.character(getRversion()), arrow = as.character(packageVersion("arrow")), haven = as.character(packageVersion("haven")), jsonlite = as.character(packageVersion("jsonlite"))), dataset_label = src$dataset_label, metadata_gaps = as.list(src$gaps), timestamp_policy = "Nearest microsecond; exact integer microseconds within the supported native numeric range; no source timezone inferred")
validate_output <- function(input, output, catalog = NULL, src = NULL, sources = NULL) {
  if (is.null(src)) src <- read_source(input, catalog)
  if (is.null(sources)) sources <- source_entries(input, catalog)
  need(dir.exists(output), "Output directory missing")
  for (e in sources$entries) need(identical(sha(file.path(output, e$path)), e$sha256), paste("Retained source differs:", e$path))
  hashes <- list()
  analysis_events <- list()
  for (mode in c("archive", "analysis")) {
    expected <- make_projection(src, sources$entries, mode)
    file <- paste0(mode, ".parquet")
    actual <- read_parquet(file.path(output, file), as_data_frame = FALSE)
    need(actual$schema$Equals(expected$table$schema, check_metadata = TRUE), paste("Schema or schema metadata differs:", mode))
    need(actual$Equals(expected$table), paste("Typed projection differs:", mode))
    hashes[[file]] <- sha(file.path(output, file))
    if (mode == "analysis") analysis_events <- expected$events
  }
  expected_meta <- make_metadata(src, sources$entries, analysis_events, hashes)
  normalized <- fromJSON(json_text(expected_meta), simplifyVector = FALSE)
  need(json_equal(read_json(file.path(output, "metadata.json")), normalized), "Metadata differs from source-derived contract")
  invisible(TRUE)
}
convert <- function(input, output, catalog = NULL) {
  need(!file.exists(output) && !dir.exists(output) && is.na(Sys.readlink(output)), "Destination already exists")
  src <- read_source(input, catalog)
  sources <- source_entries(input, catalog)
  archive <- make_projection(src, sources$entries, "archive")
  analysis <- make_projection(src, sources$entries, "analysis")
  need(dir.exists(dirname(output)), "Destination parent does not exist")
  need(dir.create(output), "Could not create destination")
  complete <- FALSE
  on.exit(if (!complete) unlink(output, recursive = TRUE), add = TRUE)
  need(dir.create(file.path(output, "source")), "Could not create source directory")
  for (i in seq_along(sources$paths)) need(file.copy(sources$paths[i], file.path(output, sources$entries[[i]]$path), overwrite = FALSE), "Source retention failed")
  write_parquet(archive$table, file.path(output, "archive.parquet"), compression = "uncompressed")
  write_parquet(analysis$table, file.path(output, "analysis.parquet"), compression = "uncompressed", coerce_timestamps = "us", allow_truncated_timestamps = FALSE)
  hashes <- setNames(lapply(c("archive.parquet", "analysis.parquet"), function(f) sha(file.path(output, f))), c("archive.parquet", "analysis.parquet"))
  writeLines(json_text(make_metadata(src, sources$entries, analysis$events, hashes)), file.path(output, "metadata.json"), useBytes = TRUE)
  validate_output(input, output, catalog, src, sources)
  complete <- TRUE
  invisible(TRUE)
}
main <- function(args) {
  need(length(args) %in% c(3L, 5L), "Usage: convert.R {convert|validate} INPUT OUTPUT [--catalog CATALOG]")
  need(args[1] %in% c("convert", "validate"), "Unknown command")
  catalog <- NULL
  if (length(args) == 5L) { need(args[4] == "--catalog", "Expected --catalog"); catalog <- args[5] }
  if (args[1] == "convert") convert(args[2], args[3], catalog) else validate_output(args[2], args[3], catalog)
  cat(if (args[1] == "convert") "CONVERTED AND VALIDATED\n" else "VALIDATED\n")
}
if (sys.nframe() == 0L) tryCatch(main(commandArgs(trailingOnly = TRUE)), error = function(e) {cat("ERROR:", conditionMessage(e), "\n", file = stderr()); quit(status = 1L)})
