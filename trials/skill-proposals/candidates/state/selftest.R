# Independent index/prefix witnesses; no live SAS results are assumed.
root <- commandArgs(trailingOnly = TRUE)[[1L]]
source_output <- capture.output(source(file.path(root, "converted.R")))
stopifnot(length(source_output) == 0L)

witness <- function(df) {
  n <- nrow(df)
  positions <- which(df$take == 1L)
  previous <- rep(NA_real_, n)
  if (length(positions) > 1L) {
    previous[positions[-1L]] <- df$value[positions[-length(positions)]]
  }
  values <- df$value
  values[is.na(values)] <- 0
  totals <- 10 + cumsum(values)
  emitted <- which(df$emit == 1L)
  stage <- data.frame(row_id = df$row_id[emitted], value = df$value[emitted],
                      prev = previous[emitted], total = totals[emitted],
                      stringsAsFactors = FALSE)
  want <- stage
  want$delta <- want$value - want$prev
  list(stage = stage, want = want)
}

check <- function(actual, expected) {
  stopifnot(identical(names(actual), c("stage", "want")))
  for (table in c("stage", "want")) {
    a <- actual[[table]]
    e <- expected[[table]]
    stopifnot(is.data.frame(a), identical(names(a), names(e)), nrow(a) == nrow(e),
              is.character(a$row_id), identical(a$row_id, e$row_id))
    for (column in names(a)[-1L]) {
      stopifnot(is.numeric(a[[column]]), identical(is.na(a[[column]]), is.na(e[[column]])))
      present <- !is.na(e[[column]])
      stopifnot(all(a[[column]][present] == e[[column]][present]))
    }
  }
}

empty <- data.frame(row_id = character(), value = numeric(), take = integer(), emit = integer())
possibilities <- expand.grid(value = c(NA_real_, -2, 0, 3), take = 0:1, emit = 0:1)
count <- 0L
for (n in 0:3) {
  selections <- if (n == 0L) matrix(integer(), nrow = 1L, ncol = 0L) else
    as.matrix(expand.grid(rep(list(seq_len(nrow(possibilities))), n)))
  for (j in seq_len(nrow(selections))) {
    df <- if (n == 0L) empty else {
      selected <- possibilities[selections[j, ], , drop = FALSE]
      data.frame(row_id = paste0("x", seq_len(n) - 1L), value = selected$value,
                  take = selected$take, emit = selected$emit, stringsAsFactors = FALSE)
    }
    before <- serialize(df, NULL)
    expected <- witness(df)
    check(translate(df), expected)
    stopifnot(identical(serialize(df, NULL), before))
    check(translate(df), expected)
    check(translate(empty), witness(empty))
    count <- count + 1L
  }
}

df <- read_input(file.path(root, "evidence/frozen/main.csv"))
before <- serialize(df, NULL)
expected <- list(stage = data.frame(
  row_id = c("r9", "r8", "r1", "r6", "r3", "r7"),
  value = c(5, NA_real_, 7, 9, 2, -4), prev = c(NA_real_, 5, NA_real_, 3, NA_real_, 9),
  total = c(15, 115, 122, 134, 136, 132), stringsAsFactors = FALSE))
expected$want <- expected$stage
expected$want$delta <- c(NA_real_, NA_real_, NA_real_, 6, NA_real_, -13)
check(translate(df), expected)
result <- translate(df)
result$want$total[[1L]] <- -999
stopifnot(result$stage$total[[1L]] == 15)
result$stage$row_id[[1L]] <- "changed"
stopifnot(identical(serialize(df, NULL), before))
check(translate(df), expected)
cat("R API cases passed:", count, "\n")
cat(R.version.string, "\n")
