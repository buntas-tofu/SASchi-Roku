# Candidate translation of packet/source.sas for its stated input contract.
translate <- function(df) {
  if (!is.data.frame(df) ||
      !identical(names(df), c("row_id", "value"))) {
    stop("Input must be a data.frame with columns row_id,value in that order.")
  }
  if (!is.character(df$row_id) || !is.numeric(df$value)) {
    stop("row_id must be character and value must be numeric.")
  }
  if (any(is.infinite(df$value))) {
    stop("Infinite input values are outside the SAS input contract.")
  }

  value <- as.double(df$value)
  value[is.na(value)] <- NA_real_
  n <- length(value)
  prev <- rep(NA_real_, n)
  prev2 <- rep(NA_real_, n)
  if (n > 1L) prev[2L:n] <- value[seq_len(n - 1L)]
  if (n > 2L) prev2[3L:n] <- value[seq_len(n - 2L)]
  change <- value - prev
  change[!is.finite(change)] <- NA_real_

  data.frame(
    row_id = df$row_id, value = value, prev = prev, prev2 = prev2,
    change = change, stringsAsFactors = FALSE, check.names = FALSE
  )
}

read_input <- function(path) {
  df <- read.csv(
    path, header = TRUE, colClasses = "character", na.strings = character(),
    stringsAsFactors = FALSE, check.names = FALSE, strip.white = FALSE,
    comment.char = "", fileEncoding = "UTF-8", encoding = "UTF-8",
    row.names = NULL
  )
  if (!identical(names(df), c("row_id", "value"))) {
    stop("CSV must have columns row_id,value in that order.")
  }
  value_text <- df$value
  blank <- !nzchar(trimws(value_text))
  value <- suppressWarnings(as.double(value_text))
  if (any(!blank & (is.na(value) | !is.finite(value)))) {
    stop("Numeric CSV cells must be finite numbers or blank.")
  }
  value[blank] <- NA_real_
  df$value <- value
  df
}

main <- function(args = commandArgs(trailingOnly = TRUE)) {
  if (length(args) != 2L) {
    stop("Usage: Rscript converted.R input.csv output.csv")
  }
  result <- translate(read_input(args[[1L]]))
  csv_result <- result
  for (name in names(csv_result)[-1L]) {
    x <- csv_result[[name]]
    text <- sprintf("%.17g", x)
    text[is.na(x)] <- ""
    csv_result[[name]] <- text
  }
  write.table(csv_result, file = args[[2L]], sep = ",", quote = 1L,
              row.names = FALSE, col.names = TRUE, na = "", qmethod = "double",
              fileEncoding = "UTF-8")
  invisible(result)
}

if (sys.nframe() == 0L) main()
