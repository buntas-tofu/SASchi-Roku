# Native base R API checks against independent expected rows supplied by self_test.py.
args <- commandArgs(trailingOnly = TRUE)
root <- normalizePath(args[1L], mustWork = TRUE)
run <- normalizePath(args[2L], mustWork = TRUE)

read_text <- function(path) {
  read.csv(path, colClasses = "character", na.strings = NULL,
            stringsAsFactors = FALSE, check.names = FALSE,
            strip.white = FALSE, comment.char = "", row.names = NULL)
}
to_number <- function(x) {
  result <- rep(NA_real_, length(x))
  present <- x != ""
  result[present] <- as.numeric(x[present])
  result
}
checks <- 0L
check <- function(condition, description) {
  checks <<- checks + 1L
  if (!isTRUE(condition)) stop(paste("Check failed:", description))
}

engine <- new.env(parent = baseenv())
source_output <- capture.output(sys.source(file.path(root, "converted.R"), envir = engine))
check(length(source_output) == 0L, "sourcing emits no output")
check(is.function(engine$translate), "sourcing defines translate")

index <- read_text(file.path(run, "suite_case_index.csv"))
inputs <- read_text(file.path(run, "suite_input.csv"))
expected <- read_text(file.path(run, "suite_expected.csv"))
empty_input <- data.frame(row_id = character(), value = numeric(),
                           eligible = integer(), stringsAsFactors = FALSE)
cols <- c("row_id", "value", "prev", "total")
paths <- c("where_path", "if_path")
results <- character(nrow(index))

for (case_index in seq_len(nrow(index))) {
  case <- index$case_id[case_index]
  rows <- inputs[inputs$case_id == case, , drop = FALSE]
  df <- data.frame(row_id = rows$row_id, value = to_number(rows$value),
                   eligible = as.integer(rows$eligible), stringsAsFactors = FALSE)
  saved <- serialize(df, NULL)
  got <- engine$translate(df)
  check(identical(saved, serialize(df, NULL)), paste(case, "input unchanged"))
  check(identical(names(got), paths), paste(case, "table names/order"))
  check(identical(engine$translate(empty_input)$where_path$row_id, character()),
        paste(case, "interleaved empty call"))
  check(identical(got, engine$translate(df)), paste(case, "fresh repeat"))
  for (path in paths) {
    table <- got[[path]]
    want <- expected[expected$case_id == case & expected$path == path, , drop = FALSE]
    check(is.data.frame(table), paste(case, path, "data.frame"))
    check(identical(names(table), cols), paste(case, path, "columns/order"))
    check(is.character(table$row_id), paste(case, path, "character identifier"))
    check(identical(table$row_id, want$row_id), paste(case, path, "identifier sequence"))
    check(nrow(table) == nrow(want), paste(case, path, "row count"))
    for (column in c("value", "prev", "total")) {
      values <- to_number(want[[column]])
      check(typeof(table[[column]]) == "double", paste(case, path, column, "numeric type"))
      check(identical(is.na(table[[column]]), is.na(values)),
            paste(case, path, column, "missing pattern"))
      keep <- !is.na(values)
      check(all(table[[column]][keep] == values[keep]),
            paste(case, path, column, "exact numeric cells"))
    }
  }
  if (nrow(got$where_path) > 0L) {
    original_if <- got$if_path
    got$where_path$total[1L] <- -987654321
    check(identical(original_if, got$if_path), paste(case, "independent output tables"))
    check(identical(saved, serialize(df, NULL)), paste(case, "output mutation preserves input"))
    fresh <- engine$translate(df)
    check(fresh$where_path$total[1L] != -987654321 || is.na(fresh$where_path$total[1L]),
          paste(case, "output mutation does not leak"))
  }
  results[case_index] <- "PASS"
}

write.csv(data.frame(case_id = index$case_id, status = results),
           file.path(run, "r_api_cases.csv"), row.names = FALSE, quote = TRUE)
cat(sprintf("PASS: %d R API cases; %d assertions.\n", nrow(index), checks))
