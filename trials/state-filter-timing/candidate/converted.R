# Translation of the supplied two DATA steps. Requires only base R.

.input_columns <- c("row_id", "value", "eligible")
.output_columns <- c("row_id", "value", "prev", "total")

.validate_input <- function(df) {
  if (!is.data.frame(df) || !identical(names(df), .input_columns)) {
    stop("df must have ordered columns row_id, value and eligible")
  }
  valid_id <- function(identifier) {
    if (is.na(identifier) || !nzchar(identifier)) return(FALSE)
    bytes <- as.integer(charToRaw(identifier))
    all(bytes >= 32L & bytes <= 126L)
  }
  if (!is.character(df$row_id) || !all(vapply(df$row_id, valid_id, logical(1)))) {
    stop("row_id must contain nonempty printable ASCII identifiers")
  }
  if (!is.numeric(df$value) || is.complex(df$value) ||
      any(is.nan(df$value)) || any(!is.na(df$value) & !is.finite(df$value))) {
    stop("value must be numeric, finite or ordinary NA")
  }
  if (!is.numeric(df$eligible) || is.complex(df$eligible) ||
      anyNA(df$eligible) || any(!df$eligible %in% c(0, 1))) {
    stop("eligible must contain integer 0 or 1")
  }
  invisible(NULL)
}

.add_to_total <- function(total, value) {
  if (is.na(value)) return(total)
  if (is.na(total)) return(value)
  result <- total + value
  if (is.finite(result)) result else NA_real_
}

.step <- function(df, filter_before) {
  count <- sum(df$eligible == 1L)
  output <- data.frame(row_id = character(count), value = numeric(count),
                       prev = numeric(count), total = numeric(count),
                       stringsAsFactors = FALSE, check.names = FALSE)
  queue <- NA_real_
  total <- 10.0
  output_position <- 0L
  for (i in seq_len(nrow(df))) {
    if (filter_before && df$eligible[i] != 1L) next
    value <- as.numeric(df$value[i])
    prev <- queue
    queue <- value
    total <- .add_to_total(total, value)
    if (df$eligible[i] == 1L) {
      output_position <- output_position + 1L
      output$row_id[output_position] <- df$row_id[i]
      output$value[output_position] <- value
      output$prev[output_position] <- prev
      output$total[output_position] <- total
    }
  }
  output
}

translate <- function(df) {
  .validate_input(df)
  list(where_path = .step(df, TRUE), if_path = .step(df, FALSE))
}

.read_input_csv <- function(path) {
  # Read every field as text first, including the literal identifier NA.
  raw <- read.csv(path, colClasses = "character", na.strings = NULL,
                  stringsAsFactors = FALSE, check.names = FALSE,
                  strip.white = FALSE, comment.char = "", row.names = NULL,
                  fill = FALSE, blank.lines.skip = FALSE)
  if (!identical(names(raw), .input_columns)) {
    stop("CSV header must be row_id,value,eligible in that order")
  }
  if (anyNA(raw) || any(!raw$eligible %in% c("0", "1"))) {
    stop("CSV fields must be present and eligible must be 0 or 1")
  }
  values <- rep(NA_real_, nrow(raw))
  present <- raw$value != ""
  values[present] <- suppressWarnings(as.numeric(raw$value[present]))
  if (any(!is.finite(values[present]))) stop("nonblank value must be finite numeric")
  data.frame(row_id = raw$row_id, value = values,
             eligible = as.integer(raw$eligible), stringsAsFactors = FALSE,
             check.names = FALSE)
}

.write_output_csv <- function(df, path) {
  # Seventeen significant digits preserve binary64 values through CSV transport.
  serialized <- df
  for (column in c("value", "prev", "total")) {
    serialized[[column]] <- ifelse(is.na(df[[column]]), "",
                                   sprintf("%.17g", df[[column]]))
  }
  write.table(serialized, file = path, sep = ",", row.names = FALSE,
               col.names = TRUE, quote = TRUE, qmethod = "double", na = "")
}

.path_exists <- function(path) {
  link <- Sys.readlink(path)
  file.exists(path) || dir.exists(path) || (!is.na(link) && nzchar(link))
}

.main <- function(args = commandArgs(trailingOnly = TRUE)) {
  if (length(args) != 2L) {
    stop("Usage: Rscript converted.R INPUT_CSV NEW_OUTPUT_DIRECTORY")
  }
  destination <- args[2L]
  if (.path_exists(destination)) stop("output destination already exists")
  outputs <- translate(.read_input_csv(args[1L]))
  if (!dir.create(destination, showWarnings = FALSE, recursive = FALSE)) {
    stop("could not create a new output destination")
  }
  for (name in names(outputs)) {
    .write_output_csv(outputs[[name]], file.path(destination, paste0(name, ".csv")))
  }
  invisible(NULL)
}

if (sys.nframe() == 0L) {
  tryCatch(.main(), error = function(error) {
    message("Error: ", conditionMessage(error))
    quit(status = 1L)
  })
}
