# Independent R API checks using expectations prepared by selftest.py.
args <- commandArgs(trailingOnly = TRUE)
root <- normalizePath(args[1L])
self <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1L])
source(file.path(dirname(normalizePath(self)), "converted.R"))
cols <- c("key", "left_seq", "right_seq", "a", "b", "shared", "from_left", "from_right")
inputs <- list(left = c("key", "left_seq", "a", "shared"),
               right = c("key", "right_seq", "b", "shared"))
read_numeric <- function(path) {
  read.csv(path, colClasses = "numeric", na.strings = "", check.names = FALSE)
}
empty <- lapply(inputs, function(columns) {
  as.data.frame(setNames(rep(list(numeric()), length(columns)), columns))
})
check <- function(actual, expected) {
  stopifnot(identical(names(actual), "want"), identical(names(actual$want), cols),
            identical(actual$want, expected), all(vapply(actual$want, is.numeric, logical(1))))
}
count <- 0L
for (path in list.dirs(root, recursive = FALSE, full.names = TRUE)) {
  if (!file.exists(file.path(path, "expected.csv"))) next
  tables <- lapply(names(inputs), function(name) read_numeric(file.path(path, paste0(name, ".csv"))))
  names(tables) <- names(inputs)
  expected <- read_numeric(file.path(path, "expected.csv"))
  before <- serialize(tables, NULL)
  check(translate(tables), expected)
  stopifnot(identical(before, serialize(tables, NULL)))
  blank <- translate(empty)$want
  stopifnot(nrow(blank) == 0L, identical(names(blank), cols),
            all(vapply(blank, is.numeric, logical(1))))
  check(translate(tables), expected)
  changed <- translate(tables)
  if (nrow(changed$want)) changed$want$shared[1L] <- 999
  check(translate(tables), expected)
  stopifnot(identical(before, serialize(tables, NULL)))
  count <- count + 1L
}
for (name in names(inputs)) {
  for (keys in list(c(2, 1), c(0, NA_real_), c(NA_real_, 3, 2))) {
    tables <- empty
    bad <- as.data.frame(setNames(rep(list(rep(1, length(keys))), length(inputs[[name]])), inputs[[name]]))
    bad$key <- keys
    tables[[name]] <- bad
    before <- serialize(tables, NULL)
    observed <- tryCatch({translate(tables); FALSE}, error = function(e) grepl("not sorted", conditionMessage(e)))
    stopifnot(observed, identical(before, serialize(tables, NULL)))
  }
}
cat("PASS:", count, "R API cases; empty-call isolation; numeric schemas; 6 unsorted API refusals\n")
