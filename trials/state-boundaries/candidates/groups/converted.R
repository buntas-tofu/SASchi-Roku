# Bounded translation of the supplied BY-group DATA step.
input_columns <- c('row_id', 'region', 'account', 'value')
output_columns <- c(input_columns, 'raw_prev', 'prev', 'total',
                    'first_region', 'last_region', 'first_account', 'last_account')

same_number <- function(a, b) {
  if (is.na(a) || is.na(b)) return(is.na(a) && is.na(b))
  a == b
}

less_number <- function(a, b) {
  if (is.na(a) || is.na(b)) return(is.na(a) && !is.na(b))
  a < b
}

translate <- function(tables) {
  if (!is.list(tables) || is.null(tables$have) || !is.data.frame(tables$have)) {
    stop('tables must contain have as a data.frame')
  }
  rows <- tables$have
  if (!identical(names(rows), input_columns)) stop('incorrect input schema')
  if (!is.character(rows$row_id) || anyNA(rows$row_id) ||
      any(!nzchar(rows$row_id)) || any(!grepl('^[ -~]+$', rows$row_id))) {
    stop('row_id must be nonempty printable ASCII')
  }
  for (name in input_columns[-1L]) {
    values <- rows[[name]]
    if (!is.numeric(values) || any(is.nan(values)) || any(is.infinite(values))) {
      stop(paste(name, 'must be numeric with ordinary numeric NA'))
    }
    if (name != 'value' && any(values != trunc(values), na.rm = TRUE)) {
      stop(paste(name, 'must be integer-valued'))
    }
  }
  n <- nrow(rows)
  if (n > 1L) {
    for (i in 2L:n) {
      if (less_number(rows$region[i], rows$region[i - 1L]) ||
          (same_number(rows$region[i], rows$region[i - 1L]) &&
           less_number(rows$account[i], rows$account[i - 1L]))) {
        stop(paste('row', i, 'input is not sorted by region, account'))
      }
    }
  }
  out <- data.frame(row_id = as.character(rows$row_id),
                    region = as.numeric(rows$region), account = as.numeric(rows$account),
                    value = as.numeric(rows$value), stringsAsFactors = FALSE)
  for (name in output_columns[-seq_along(input_columns)]) out[[name]] <- rep(NA_real_, n)
  queue <- NA_real_
  total <- 0
  for (i in seq_len(n)) {
    fr <- i == 1L || !same_number(rows$region[i], rows$region[i - 1L])
    lr <- i == n || !same_number(rows$region[i], rows$region[i + 1L])
    fa <- fr || !same_number(rows$account[i], rows$account[i - 1L])
    la <- lr || !same_number(rows$account[i], rows$account[i + 1L])
    raw_prev <- queue
    queue <- rows$value[i]
    prev <- if (fa) NA_real_ else raw_prev
    if (fr) total <- 100
    if (!is.na(total) || !is.na(rows$value[i])) {
      total <- (if (is.na(total)) 0 else total) + (if (is.na(rows$value[i])) 0 else rows$value[i])
      if (!is.finite(total)) total <- NA_real_
    }
    out$raw_prev[i] <- raw_prev
    out$prev[i] <- prev
    out$total[i] <- total
    out$first_region[i] <- as.numeric(fr)
    out$last_region[i] <- as.numeric(lr)
    out$first_account[i] <- as.numeric(fa)
    out$last_account[i] <- as.numeric(la)
  }
  list(want = out)
}

read_input <- function(directory) {
  rows <- read.csv(file.path(directory, 'have.csv'), colClasses = 'character',
                   na.strings = NULL, check.names = FALSE, strip.white = FALSE,
                   comment.char = '', blank.lines.skip = FALSE, fill = FALSE,
                   stringsAsFactors = FALSE, fileEncoding = 'UTF-8')
  if (!identical(names(rows), input_columns)) stop('have.csv has incorrect headers')
  for (name in input_columns[-1L]) {
    tokens <- rows[[name]]
    values <- suppressWarnings(as.numeric(tokens))
    if (any(tokens != '' & (is.na(values) | !is.finite(values)))) {
      stop(paste('invalid numeric CSV field in', name))
    }
    values[tokens == ''] <- NA_real_
    rows[[name]] <- values
  }
  list(have = rows)
}

main <- function(args = commandArgs(trailingOnly = TRUE)) {
  if (length(args) != 2L) stop('usage: converted.R INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY')
  target <- args[2L]
  if (file.exists(target) || dir.exists(target)) stop('destination already exists')
  result <- translate(read_input(args[1L]))
  if (!dir.create(target, recursive = FALSE)) stop('cannot create destination')
  # Format each numeric cell with enough precision for a binary64 round trip.
  output <- result$want
  for (name in output_columns[-1L]) {
    output[[name]] <- ifelse(is.na(output[[name]]), '', sprintf('%.17g', output[[name]]))
  }
  write.table(output, file.path(target, 'want.csv'), sep = ',', row.names = FALSE,
              col.names = TRUE, quote = TRUE, na = '', qmethod = 'double',
              fileEncoding = 'UTF-8')
}

if (sys.nframe() == 0L) main()
