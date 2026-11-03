# R API and R-consumer checks against independently hand-traced tables.
args <- commandArgs(trailingOnly = TRUE)
work <- args[[1L]]
script <- sub("^--file=", "", commandArgs()[grepl("^--file=", commandArgs())])
here <- dirname(normalizePath(script))
root <- dirname(here)
source(file.path(here, "converted.R"))

read_result <- function(directory) {
  setNames(lapply(names(OUTPUT_COLUMNS), function(name) {
    classes <- rep("character", length(OUTPUT_COLUMNS[[name]]))
    if (name == "want") classes[7:8] <- "numeric"
    if (name == "descriptor") classes[3] <- "numeric"
    read.csv(file.path(directory, paste0(name, ".csv")), colClasses = classes,
             na.strings = character(), strip.white = FALSE, check.names = FALSE,
             stringsAsFactors = FALSE, comment.char = "", fileEncoding = "ASCII")
  }), names(OUTPUT_COLUMNS))
}
for (case in c("main", "boundary", "blank", "single-false", "empty", "ascii")) {
  input <- if (case == "ascii") file.path(work, "ascii-input") else file.path(root, "packet", "cases", case)
  have <- read_have(input)
  before <- serialize(have, NULL)
  result <- translate(list(have = have))
  truth <- read_result(file.path(work, paste0(case, "-truth")))
  stopifnot(identical(result, truth), identical(serialize(have, NULL), before))
  for (language in c("python", "r")) {
    stopifnot(identical(read_result(file.path(work, paste0(case, "-", language))), truth))
  }
  empty <- have[FALSE, , drop = FALSE]
  stopifnot(identical(translate(list(have = empty)), read_result(file.path(work, "empty-truth"))))
  stopifnot(identical(translate(list(have = have)), truth))
  result$descriptor$bytes[[1L]] <- 99
  stopifnot(identical(translate(list(have = have)), truth))
}
bad_values <- list(list("raw", "short"), list("suffix", "\t "),
                   list("row_id", ""), list("row_id", "caf\u00e9"),
                   list("flag", 2), list("flag", NA_real_))
base <- read_have(file.path(root, "packet", "cases", "single-false"))
for (bad_value in bad_values) {
  bad <- base
  bad[[bad_value[[1L]]]][[1L]] <- bad_value[[2L]]
  error <- tryCatch({translate(list(have = bad)); FALSE}, error = function(e) TRUE)
  stopifnot(error)
}
cat("PASS: R API and both CSV consumers; typed empty schemas; fresh calls; unchanged inputs; 6 R API domain rejections\n")
