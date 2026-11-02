source("output/converted.R")
columns <- c("row_id", "value", "prev", "prev2", "change")
checks <- 0L
check <- function(ok, label) {
  if (!isTRUE(ok)) stop(paste("FAIL:", label))
  checks <<- checks + 1L
  cat("PASS:", label, "\n")
}
expected <- list(
  main = data.frame(row_id = c("l7", "l2", "l9", "l1"),
    value = c(12,18,15,9), prev = c(NA,12,18,15),
    prev2 = c(NA,NA,12,18), change = c(NA,6,-3,-6)),
  edge = data.frame(row_id = c("e9", "e2", "e7", "e4"),
    value = c(5,NA,-2,0), prev = c(NA,5,NA,-2),
    prev2 = c(NA,NA,5,NA), change = c(NA,NA,NA,2)),
  single = data.frame(row_id = "s1", value = -3, prev = NA_real_,
    prev2 = NA_real_, change = NA_real_),
  empty = data.frame(row_id = character(), value = numeric(),
    prev = numeric(), prev2 = numeric(), change = numeric())
)
for (name in names(expected)) {
  input_path <- paste0("packet/", name, ".csv")
  df <- read_input(input_path)
  before <- serialize(df, NULL)
  actual <- translate(df)
  check(identical(actual, expected[[name]]), paste(name, "API exact hand truth"))
  check(identical(before, serialize(df, NULL)), paste(name, "input unchanged"))
  check(identical(translate(df), expected[[name]]), paste(name, "fresh invocation"))
  output_path <- paste0("output/", name, ".csv")
  status <- system2("Rscript", c("output/converted.R", input_path, output_path))
  check(identical(status, 0L), paste(name, "CLI exit"))
  disk <- read.csv(output_path, colClasses = c("character", rep("numeric", 4)),
    na.strings = character(), check.names = FALSE, fileEncoding = "UTF-8")
  check(identical(disk, expected[[name]]), paste(name, "CSV exact hand truth"))
  check(!any(grepl("NA", readLines(output_path), fixed = TRUE)),
    paste(name, "missing cells written blank"))
}

# Independent scalar queue witness, separate from the vector implementation.
queue_witness <- function(df) {
  q1 <- NA_real_
  q2 <- c(NA_real_, NA_real_)
  out <- data.frame(row_id = df$row_id, value = df$value,
    prev = rep(NA_real_, nrow(df)), prev2 = rep(NA_real_, nrow(df)),
    change = rep(NA_real_, nrow(df)))
  for (i in seq_len(nrow(df))) {
    out$prev[i] <- q1
    out$prev2[i] <- q2[1]
    if (!is.na(df$value[i]) && !is.na(q1)) out$change[i] <- df$value[i] - q1
    q1 <- df$value[i]
    q2 <- c(q2[2], df$value[i])
  }
  out
}
set.seed(20261101)
for (n in c(0L, 1L, 2L, 3L, 7L, 1000L)) {
  df <- data.frame(row_id = sprintf("r%06d", seq_len(n)),
    value = sample(c(NA_real_, -99:99), n, replace = TRUE))
  check(identical(translate(df), queue_witness(df)), paste(n, "rows queue witness"))
}

# Negative control: wrongly retain the last nonmissing value in lag1.
wrong <- expected$edge
wrong$prev[3] <- 5
wrong$change[3] <- -7
check(!identical(wrong, expected$edge), "comparator rejects missing-skipping lag variant")

# Exercise textual keys vulnerable to automatic type/NA conversion or CSV parsing.
keys <- c("0007", "NA", "", " a ", "a,b", "é", 'x"y', "#k")
text_df <- data.frame(row_id = keys, value = c(1,NA,3,4,5,6,7,8))
write.csv(text_df, "output/text_input.csv", row.names = FALSE, na = "",
  fileEncoding = "UTF-8")
check(system2("Rscript", c("output/converted.R", "output/text_input.csv",
  "output/text_output.csv")) == 0L, "text CLI exit")
text_out <- read.csv("output/text_output.csv", colClasses = c("character", rep("numeric", 4)),
  na.strings = character(), strip.white = FALSE, fileEncoding = "UTF-8")
check(identical(lapply(text_out$row_id, charToRaw), lapply(keys, charToRaw)),
  "UTF-8 and special text key bytes preserved")
check(identical(text_out, queue_witness(text_df)), "text CLI values and schema")

# Source a separate R process carrying two CLI-like arguments; no output may appear.
writeLines('source("output/converted.R"); stopifnot(is.function(translate))',
  "output/source_probe.R")
probe_path <- "output/must_not_exist.csv"
if (file.exists(probe_path)) stop("Source probe output already exists")
probe_status <- system2("Rscript", c("output/source_probe.R", "packet/main.csv", probe_path))
check(probe_status == 0L && !file.exists(probe_path), "sourcing does not run CLI")
precision_df <- data.frame(row_id = c("p1", "p2", "p3"),
  value = c(0.12345678901234567, 1.0000000000000002, -0.33333333333333331))
writeLines(c("row_id,value", "p1,0.12345678901234567", "p2,1.0000000000000002",
  "p3,-0.33333333333333331"), "output/precision_input.csv")
check(system2("Rscript", c("output/converted.R", "output/precision_input.csv",
  "output/precision_output.csv")) == 0L, "precision CLI exit")
precision_out <- read.csv("output/precision_output.csv",
  colClasses = c("character", rep("numeric", 4)), na.strings = character())
check(identical(precision_out, queue_witness(precision_df)),
  "17-digit numeric CSV round trip")
overflow_df <- data.frame(row_id = c("o1", "o2"), value = c(-1e308, 1e308))
check(identical(translate(overflow_df)$change, c(NA_real_, NA_real_)),
  "subtraction overflow maps to ordinary missing")
cat("TOTAL:", checks, "checks passed\n")
cat("\nEnvironment:\n")
print(sessionInfo())
