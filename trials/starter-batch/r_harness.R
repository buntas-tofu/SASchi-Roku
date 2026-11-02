# Invoke a candidate, checking caller preservation, repeated calls and types.
args <- commandArgs(trailingOnly = TRUE)
candidate <- args[[1]]
input_path <- args[[2]]
output_path <- args[[3]]
mechanism <- args[[4]]
env <- new.env(parent = globalenv())
sys.source(candidate, envir = env)
if (mechanism == "length") {
  df <- read.csv(input_path, colClasses = c("character", "character"),
                 na.strings = NULL, strip.white = FALSE, check.names = FALSE)
  columns <- c("row_id", "text", "len")
} else {
  df <- read.csv(input_path, colClasses = c("character", "numeric"),
                 na.strings = "", strip.white = FALSE, check.names = FALSE)
  columns <- c("row_id", "value", "prev", "prev2", "change")
}
before <- serialize(df, NULL)
first <- env$translate(df)
if (!identical(before, serialize(df, NULL))) stop("caller input changed")
snapshot <- serialize(first, NULL)
second <- env$translate(df)
if (!identical(before, serialize(df, NULL))) stop("caller input changed")
if (!identical(snapshot, serialize(first, NULL)) || !identical(first, second)) {
  stop("fresh-call results differ")
}
if (!is.data.frame(first) || !identical(names(first), columns)) stop("output schema differs")
if (!is.character(first$row_id)) stop("row_id must be character")
if (mechanism == "length" && !is.character(first$text)) stop("text must be character")
numeric_columns <- if (mechanism == "length") "len" else columns[-1]
if (!all(vapply(first[numeric_columns], is.numeric, logical(1)))) stop("numeric type differs")
write.csv(first, output_path, row.names = FALSE, na = "", fileEncoding = "UTF-8")
