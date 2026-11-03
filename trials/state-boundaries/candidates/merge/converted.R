# Candidate translation of packet/source.sas; live SAS execution is pending.
INPUT_COLUMNS <- list(
  left = c("key", "left_seq", "a", "shared"),
  right = c("key", "right_seq", "b", "shared")
)
OUTPUT_COLUMNS <- c(
  "key", "left_seq", "right_seq", "a", "b", "shared", "from_left", "from_right"
)

validate_tables <- function(tables) {
  if (!is.list(tables) || length(tables) != 2L ||
      !setequal(names(tables), names(INPUT_COLUMNS))) {
    stop("Expected exactly the left and right input tables")
  }
  for (name in names(INPUT_COLUMNS)) {
    tab <- tables[[name]]
    if (!is.data.frame(tab) || !identical(names(tab), INPUT_COLUMNS[[name]])) {
      stop(paste(name, "has an incorrect schema"))
    }
    for (column in names(tab)) {
      x <- tab[[column]]
      if (!(typeof(x) %in% c("integer", "double")) || !is.null(dim(x))) {
        stop(paste(name, column, "must be a numeric vector"))
      }
      if (any(is.nan(x)) || any(!is.na(x) & !is.finite(x))) {
        stop(paste(name, column, "contains nonfinite values"))
      }
    }
    key <- tab$key
    if (any(!is.na(key) & key != floor(key))) {
      stop(paste(name, "key must be an integer"))
    }
    if (length(key) > 1L) {
      for (i in 2:length(key)) {
        if ((!is.na(key[i - 1L]) && is.na(key[i])) ||
            (!is.na(key[i - 1L]) && !is.na(key[i]) && key[i] < key[i - 1L])) {
          stop(paste(name, "is not sorted at row", i))
        }
      }
    }
  }
  invisible(NULL)
}

same_key <- function(a, b) {
  if (is.na(a)) is.na(b) else !is.na(b) && a == b
}

key_le <- function(a, b) {
  if (is.na(a)) TRUE else !is.na(b) && a <= b
}

translate <- function(tables) {
  validate_tables(tables)
  left <- tables$left
  right <- tables$right
  li <- ri <- 1L
  nl <- nrow(left)
  nr <- nrow(right)
  rows <- vector("list", nl + nr)
  count <- 0L
  while (li <= nl || ri <= nr) {
    if (ri > nr || (li <= nl && key_le(left$key[li], right$key[ri]))) {
      group <- left$key[li]
    } else {
      group <- right$key[ri]
    }
    pdv <- setNames(rep(NA_real_, length(OUTPUT_COLUMNS)), OUTPUT_COLUMNS)
    pdv[c("from_left", "from_right")] <- 0
    repeat {
      read_left <- li <= nl && same_key(left$key[li], group)
      read_right <- ri <= nr && same_key(right$key[ri], group)
      if (!(read_left || read_right)) break
      # Only actual reads replace columns. Right reads follow left reads.
      if (read_left) {
        for (column in INPUT_COLUMNS$left) pdv[column] <- left[[column]][li]
        pdv["from_left"] <- 1
        li <- li + 1L
      }
      if (read_right) {
        for (column in INPUT_COLUMNS$right) pdv[column] <- right[[column]][ri]
        pdv["from_right"] <- 1
        ri <- ri + 1L
      }
      count <- count + 1L
      rows[[count]] <- pdv
    }
  }
  if (count == 0L) {
    want <- as.data.frame(setNames(rep(list(numeric()), length(OUTPUT_COLUMNS)), OUTPUT_COLUMNS))
  } else {
    want <- as.data.frame(do.call(rbind, rows[seq_len(count)]))
    rownames(want) <- NULL
  }
  list(want = want)
}

read_tables <- function(directory) {
  tables <- list()
  pattern <- "^[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?$"
  for (name in names(INPUT_COLUMNS)) {
    path <- file.path(directory, paste0(name, ".csv"))
    raw <- read.csv(path, header = TRUE, colClasses = "character", na.strings = NULL,
                    check.names = FALSE, stringsAsFactors = FALSE, comment.char = "",
                    strip.white = FALSE, fill = FALSE, row.names = NULL)
    if (!identical(names(raw), INPUT_COLUMNS[[name]])) {
      stop(paste(name, "has an incorrect CSV header"))
    }
    for (column in names(raw)) {
      fields <- raw[[column]]
      missing <- fields == ""
      if (any(!missing & !grepl(pattern, trimws(fields), perl = TRUE))) {
        stop(paste(name, column, "contains invalid numeric CSV fields"))
      }
      values <- rep(NA_real_, length(fields))
      values[!missing] <- as.numeric(fields[!missing])
      if (any(!missing & !is.finite(values))) {
        stop(paste(name, column, "contains nonfinite numeric CSV fields"))
      }
      raw[[column]] <- values
    }
    tables[[name]] <- raw
  }
  tables
}

main <- function(args = commandArgs(trailingOnly = TRUE)) {
  if (length(args) != 2L) {
    stop("Usage: Rscript --vanilla converted.R INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY")
  }
  destination <- args[2L]
  link <- Sys.readlink(destination)
  if (file.exists(destination) || dir.exists(destination) ||
      (!is.na(link) && nzchar(link))) {
    stop(paste("Destination already exists:", destination))
  }
  result <- translate(read_tables(args[1L]))
  if (!dir.create(destination, recursive = FALSE)) stop("Could not create destination")
  # Decimal text with 17 significant digits round-trips finite doubles.
  encoded <- as.data.frame(lapply(result$want, function(x) {
    ifelse(is.na(x), "", sprintf("%.17g", x))
  }), stringsAsFactors = FALSE)
  names(encoded) <- OUTPUT_COLUMNS
  write.table(encoded, file.path(destination, "want.csv"), sep = ",", quote = FALSE,
              row.names = FALSE, col.names = TRUE, na = "", eol = "\n")
  invisible(NULL)
}

if (sys.nframe() == 0L) {
  tryCatch(main(), error = function(error) {
    message(conditionMessage(error))
    quit(status = 1L)
  })
}
