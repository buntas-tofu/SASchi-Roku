# Candidate self-test only. The independent parent adapter is not used here.
args <- commandArgs(trailingOnly = TRUE)
source(args[[1L]])
bridge <- args[[2L]]
read_chars <- function(name) read.csv(file.path(bridge, name),
  colClasses = "character", na.strings = character(), check.names = FALSE,
  stringsAsFactors = FALSE, strip.white = FALSE, fileEncoding = "UTF-8")
hexraw <- function(value) {
  if (value == "") return(raw())
  starts <- seq.int(1L, nchar(value), 2L)
  as.raw(strtoi(substring(value, starts, starts + 1L), 16L))
}
ashex <- function(bytes) paste(sprintf("%02x", as.integer(bytes)), collapse = "")
result <- consume(bridge)
cells <- read_chars("cells.csv")
expected_names <- c("id", "text", "value", "date", "stamp", "all_missing", "status")
count <- nrow(cells) %/% 7L
stopifnot(identical(names(result), c("data", "tags", "metadata", "labels")),
  identical(names(result$data), expected_names),
  identical(vapply(result$data, length, integer(1L)), setNames(rep(count, 7L), expected_names)),
  is.character(result$data$id), is.list(result$data$text), inherits(result$data$date, "Date"),
  all(vapply(result$data[c("value", "stamp", "all_missing", "status")], is.double, logical(1L))),
  identical(result$metadata, read_chars("columns.csv")),
  identical(result$labels, read_chars("labels.csv")),
  all(vapply(result$metadata, is.character, logical(1L))),
  all(vapply(result$labels, is.character, logical(1L))))
for (index in seq_len(nrow(cells))) {
  row <- (index - 1L) %/% 7L + 1L
  column <- cells$column[index]
  expected <- cells$value[index]
  actual <- result$data[[column]][[row]]
  if (cells$tag[index] != "") {
    stopifnot(is.na(actual))
  } else if (column == "id") {
    stopifnot(identical(ashex(charToRaw(enc2utf8(actual))), tolower(expected)))
  } else if (column == "text") {
    stopifnot(is.raw(actual), identical(actual, hexraw(expected)))
  } else if (column == "date") {
    stopifnot(identical(format(actual, "%Y-%m-%d"), expected))
  } else {
    stopifnot(identical(ashex(writeBin(actual, raw(), size = 8L, endian = "little")), tolower(expected)))
  }
}
tagged <- cells[cells$tag != "", c("row", "column", "tag"), drop = FALSE]
stopifnot(identical(as.character(result$tags$row), tagged$row),
  identical(result$tags$column, tagged$column), identical(result$tags$tag, tagged$tag))
cat(sprintf("R bridge self-test passed: %d rows, %d tags\n", count, nrow(result$tags)))
