# Bounded translation of the supplied source. All text is decoded printable ASCII.
INPUT_COLUMNS <- c("row_id", "raw", "suffix", "flag")
OUTPUT_COLUMNS <- list(
  stage = c("row_id", "short", "joined", "tag"),
  want = c("row_id", "short", "copy", "wrapped", "joined", "tag", "n", "z"),
  descriptor = c("table", "column", "bytes")
)

validate_text <- function(x, name, width = NULL) {
  if (!is.character(x) || anyNA(x)) stop(paste(name, "must be nonmissing text"))
  valid <- vapply(x, function(s) {
    b <- as.integer(charToRaw(s))
    all(b >= 32L & b <= 126L)
  }, logical(1))
  if (!all(valid)) stop(paste(name, "must be printable ASCII"))
  if (!is.null(width) && any(nchar(x, type = "bytes") != width)) {
    stop(paste(name, "must already contain exactly", width, "bytes"))
  }
  if (name == "row_id" && any(nchar(x, type = "bytes") == 0L)) {
    stop("row_id must be nonempty")
  }
}

fixed <- function(value, width) {
  left <- substr(value, 1L, width)
  paste0(left, strrep(" ", width - nchar(left, type = "bytes")))
}

translate <- function(tables) {
  if (!is.list(tables) || is.null(tables$have) || !is.data.frame(tables$have)) {
    stop("tables must contain the have data.frame")
  }
  have <- tables$have
  if (!identical(names(have), INPUT_COLUMNS)) stop("have has incorrect columns")
  validate_text(have$row_id, "row_id")
  validate_text(have$raw, "raw", 6L)
  validate_text(have$suffix, "suffix", 2L)
  if (!is.numeric(have$flag) || anyNA(have$flag) ||
      any(!is.finite(have$flag)) || any(!have$flag %in% c(0, 1))) {
    stop("flag must be numeric 0 or 1")
  }

  stage <- data.frame(row_id = character(), short = character(),
                      joined = character(), tag = character(),
                      stringsAsFactors = FALSE, check.names = FALSE)
  want <- data.frame(row_id = character(), short = character(), copy = character(),
                     wrapped = character(), joined = character(), tag = character(),
                     n = numeric(), z = numeric(),
                     stringsAsFactors = FALSE, check.names = FALSE)
  for (i in seq_len(nrow(have))) {
    short <- fixed(have$raw[[i]], 3L)
    joined <- fixed(paste0(short, have$suffix[[i]]), 6L)
    # The first lexical assignment determines the width, regardless of branch.
    tag <- fixed(if (have$flag[[i]] == 1) "Y" else "LONG", 1L)
    stage[i, ] <- list(have$row_id[[i]], short, joined, tag)
  }
  for (i in seq_len(nrow(stage))) {
    # LENGTH $5 precedes SET, so the three input bytes are blank-padded.
    short <- fixed(stage$short[[i]], 5L)
    copy <- fixed(short, 2L)
    short <- fixed(paste0(short, "!"), 5L)
    wrapped <- fixed(paste0("[", short, "]"), 8L)
    z <- nchar(sub(" +$", "", short), type = "bytes")
    want[i, ] <- list(stage$row_id[[i]], short, copy, wrapped,
                     stage$joined[[i]], stage$tag[[i]], as.numeric(max(1L, z)),
                     as.numeric(z))
  }
  descriptor <- data.frame(
    table = c(rep("stage", 3L), rep("want", 5L)),
    column = c("short", "joined", "tag", "short", "copy", "wrapped", "joined", "tag"),
    bytes = as.numeric(c(3, 6, 1, 5, 2, 8, 6, 1)),
    stringsAsFactors = FALSE, check.names = FALSE
  )
  list(stage = stage, want = want, descriptor = descriptor)
}

read_have <- function(directory) {
  path <- file.path(directory, "have.csv")
  size <- file.info(path)$size
  if (is.na(size)) stop("have.csv cannot be read")
  raw_file <- readBin(path, "raw", n = size)
  codes <- as.integer(raw_file)
  if (any(!codes %in% c(10L, 13L, 32L:126L))) {
    stop("CSV contains bytes outside ASCII text and line terminators")
  }
  have <- read.csv(path, header = TRUE, colClasses = "character",
                   na.strings = character(), strip.white = FALSE,
                   check.names = FALSE, stringsAsFactors = FALSE,
                   comment.char = "", blank.lines.skip = FALSE,
                   fileEncoding = "ASCII")
  if (!identical(names(have), INPUT_COLUMNS)) stop("have.csv has incorrect columns")
  flag <- suppressWarnings(as.numeric(have$flag))
  if (anyNA(flag)) stop("flag must be numeric 0 or 1")
  have$flag <- flag
  have
}

main <- function(args = commandArgs(trailingOnly = TRUE)) {
  if (length(args) != 2L) {
    stop("usage: Rscript --vanilla converted.R INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY")
  }
  destination <- args[[2L]]
  link <- Sys.readlink(destination)
  if (file.exists(destination) || dir.exists(destination) ||
      (!is.na(link) && nzchar(link))) stop("output destination already exists")
  result <- translate(list(have = read_have(args[[1L]])))
  if (!dir.create(destination, recursive = FALSE, showWarnings = FALSE)) {
    stop("could not create a new output destination")
  }
  for (name in names(OUTPUT_COLUMNS)) {
    write.table(result[[name]], file.path(destination, paste0(name, ".csv")),
                sep = ",", row.names = FALSE, col.names = TRUE,
                quote = TRUE, qmethod = "double", na = "", fileEncoding = "ASCII")
  }
  invisible(result)
}

if (sys.nframe() == 0L) {
  tryCatch(main(), error = function(e) {
    message("conversion failed: ", conditionMessage(e))
    quit(status = 1L)
  })
}
