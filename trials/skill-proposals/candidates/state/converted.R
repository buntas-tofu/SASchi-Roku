# Translation of the supplied two-step SAS slice, using ordinary missing only.

translate <- function(df) {
  total <- 10
  lag_queue <- NA_real_
  n_output <- sum(df$emit == 1L)
  stage <- data.frame(row_id = character(n_output),
                      value = rep(NA_real_, n_output),
                      prev = rep(NA_real_, n_output),
                      total = numeric(n_output),
                      stringsAsFactors = FALSE)
  output_position <- 0L
  for (i in seq_len(nrow(df))) {
    value <- as.numeric(df$value[[i]])
    prev <- NA_real_
    if (df$take[[i]] == 1L) {
      prev <- lag_queue
      lag_queue <- value
    }
    if (!is.na(value)) {
      total <- total + value
    }
    if (df$emit[[i]] == 1L) {
      output_position <- output_position + 1L
      stage$row_id[[output_position]] <- as.character(df$row_id[[i]])
      stage$value[[output_position]] <- value
      stage$prev[[output_position]] <- prev
      stage$total[[output_position]] <- total
    }
  }

  want <- stage
  want$delta <- want$value - want$prev
  list(stage = stage, want = want)
}

read_input <- function(path) {
  df <- read.csv(path, colClasses = "character", na.strings = character(),
                 stringsAsFactors = FALSE, check.names = FALSE,
                 strip.white = FALSE, comment.char = "")
  value <- rep(NA_real_, nrow(df))
  present <- nzchar(df$value)
  value[present] <- as.numeric(df$value[present])
  df$value <- value
  df$take <- as.integer(df$take)
  df$emit <- as.integer(df$emit)
  df
}

main <- function(args = commandArgs(trailingOnly = TRUE)) {
  if (length(args) != 2L) {
    stop("Usage: converted.R INPUT.csv NEW_OUTPUT_DIRECTORY", call. = FALSE)
  }
  result <- translate(read_input(args[[1L]]))
  directory <- args[[2L]]
  if (file.exists(directory) || dir.exists(directory)) {
    stop("Output directory must be new", call. = FALSE)
  }
  if (!dir.create(directory, recursive = TRUE)) {
    stop("Could not create output directory", call. = FALSE)
  }
  for (name in c("stage", "want")) {
    write.csv(result[[name]], file.path(directory, paste0(name, ".csv")),
              row.names = FALSE, na = "")
  }
  invisible(result)
}

if (sys.nframe() == 0L) {
  main()
}
