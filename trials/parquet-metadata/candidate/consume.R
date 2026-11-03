# Engineering evaluation consumer for the specified CSV bridge, using base R.
# This file is sourceable and does not read Parquet or SAS binary files itself.

consume <- function(bridge_dir) {
  schema <- c("id", "text", "value", "date", "stamp", "all_missing", "status")
  valid_tags <- c(".", "._", paste0(".", LETTERS))
  fail <- function(message) stop(message, call. = FALSE)
  csv <- function(name, headers) {
    result <- read.csv(file.path(bridge_dir, name), colClasses = "character",
      na.strings = character(), stringsAsFactors = FALSE, check.names = FALSE,
      strip.white = FALSE, comment.char = "", quote = "\"", allowEscapes = FALSE,
      blank.lines.skip = FALSE, fileEncoding = "UTF-8")
    if (!identical(names(result), headers)) fail(paste("wrong CSV headers:", name))
    result
  }
  unhex <- function(value) {
    if (length(value) != 1L || is.na(value) || nchar(value, type = "bytes") %% 2L != 0L ||
        !grepl("^[0-9A-Fa-f]*$", value)) fail("invalid hexadecimal cell")
    if (value == "") return(raw())
    starts <- seq.int(1L, nchar(value, type = "bytes"), by = 2L)
    as.raw(strtoi(substring(value, starts, starts + 1L), base = 16L))
  }
  cells <- csv("cells.csv", c("row", "column", "kind", "value", "tag"))
  metadata <- csv("columns.csv", c("column", "property", "type", "value"))
  labels <- csv("labels.csv", c("column", "value_hex", "label_hex"))
  if (nrow(cells) %% length(schema) != 0L) fail("incomplete bridge rows")
  count <- nrow(cells) %/% length(schema)
  expected_rows <- if (count == 0L) character() else
    rep(as.character(seq_len(count) - 1L), each = length(schema))
  if (!identical(cells$row, expected_rows) ||
      !identical(cells$column, rep(schema, times = count))) fail("wrong bridge cell order")
  data <- list(id = character(count), text = vector("list", count),
    value = rep(NA_real_, count), date = structure(rep(NA_real_, count), class = "Date"),
    stamp = rep(NA_real_, count), all_missing = rep(NA_real_, count),
    status = rep(NA_real_, count))
  tags <- data.frame(row = integer(), column = character(), tag = character(),
    stringsAsFactors = FALSE)
  for (index in seq_len(nrow(cells))) {
    column <- cells$column[index]
    row <- (index - 1L) %/% length(schema) + 1L
    kind <- cells$kind[index]
    value <- cells$value[index]
    tag <- cells$tag[index]
    expected_kind <- if (column %in% c("id", "text")) "text_hex" else
      if (column == "date") "date_iso" else "float64_hex"
    if (kind != expected_kind) fail("wrong bridge cell kind")
    if (column %in% c("id", "text")) {
      if (tag != "") fail("tag on character cell")
      bytes <- unhex(value)
      if (column == "text") {
        data$text[[row]] <- bytes
      } else {
        if (any(bytes == as.raw(0))) fail("embedded NUL cannot fit the required R id character vector")
        decoded <- rawToChar(bytes)
        Encoding(decoded) <- "UTF-8"
        if (!validUTF8(decoded)) fail("invalid UTF-8 identifier from bridge")
        data$id[row] <- decoded
      }
    } else if (tag != "") {
      if (!(tag %in% valid_tags) || value != "") fail("invalid tagged null")
      tags[nrow(tags) + 1L, ] <- list(row - 1L, column, tag)
    } else if (column == "date") {
      if (!grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", value)) fail("invalid date text")
      day <- as.Date(value, format = "%Y-%m-%d")
      if (is.na(day) || format(day, "%Y-%m-%d") != value) fail("invalid date")
      data$date[row] <- day
    } else {
      bytes <- unhex(value)
      if (length(bytes) != 8L) fail("invalid binary64 byte length")
      number <- readBin(bytes, what = "double", n = 1L, size = 8L, endian = "little")
      if (length(number) != 1L || !is.finite(number)) fail("non-finite binary64 cell")
      data[[column]][row] <- number
    }
  }
  list(data = data, tags = tags, metadata = metadata, labels = labels)
}
