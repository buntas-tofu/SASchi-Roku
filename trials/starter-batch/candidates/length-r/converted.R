# Candidate translation of packet/source.sas for the supplied descriptor.
translate <- function(df) {
  if (!is.data.frame(df) || !identical(names(df), c("row_id", "text"))) {
    stop("Expected a data.frame with columns row_id,text in that order.")
  }
  if (!is.character(df$row_id) || !is.character(df$text) ||
      anyNA(df$row_id) || anyNA(df$text)) {
    stop("row_id and text must contain decoded character values without R NA.")
  }
  if (any(!validUTF8(df$row_id)) || any(nchar(df$row_id, type = "bytes") > 8L)) {
    stop("row_id must be valid UTF-8 and fit its 8-byte descriptor.")
  }
  text_size <- nchar(df$text, type = "bytes")
  ascii <- vapply(df$text, function(x) all(as.integer(charToRaw(x)) < 128L),
                  logical(1L))
  if (any(text_size > 10L) || any(!ascii)) {
    stop("text must contain at most 10 ASCII bytes per value.")
  }
  stored <- paste0(df$text, strrep(" ", 10L - text_size))
  if (nrow(df) == 0L) stored <- character()
  # SAS blanks are literal spaces. Tabs and leading spaces remain significant.
  lengths <- as.double(pmax(1L, nchar(sub(" +$", "", stored, useBytes = TRUE),
                                     type = "bytes")))
  data.frame(row_id = df$row_id, text = stored, len = lengths,
             stringsAsFactors = FALSE, check.names = FALSE)
}

# Parse quoted CSV without normalizing embedded CR or LF characters.
.read_csv_bytes <- function(path) {
  con <- file(path, "rb")
  on.exit(close(con))
  bytes <- as.integer(readBin(con, what = "raw", n = file.info(path)$size))
  if (length(bytes) >= 3L && identical(bytes[1:3], c(239L, 187L, 191L))) {
    bytes <- bytes[-(1:3)]
  }
  if (any(bytes == 0L)) stop("R character strings cannot represent NUL bytes.")
  records <- list()
  fields <- character()
  value <- integer()
  state <- "start"
  active <- FALSE
  i <- 1L
  while (i <= length(bytes)) {
    b <- bytes[i]
    if (state == "quoted") {
      if (b == 34L) {
        if (i < length(bytes) && bytes[i + 1L] == 34L) {
          value <- c(value, 34L)
          i <- i + 1L
        } else {
          state <- "closed"
        }
      } else {
        value <- c(value, b)
      }
    } else if (b %in% c(44L, 10L, 13L)) {
      fields <- c(fields, rawToChar(as.raw(value)))
      value <- integer()
      state <- "start"
      if (b == 44L) {
        active <- TRUE
      } else {
        records[[length(records) + 1L]] <- fields
        fields <- character()
        active <- FALSE
        if (b == 13L && i < length(bytes) && bytes[i + 1L] == 10L) {
          i <- i + 1L
        }
      }
    } else {
      if (state == "closed") stop("Unexpected bytes after a closing CSV quote.")
      active <- TRUE
      if (b == 34L) {
        if (state != "start") stop("Quote inside an unquoted CSV field.")
        state <- "quoted"
      } else {
        value <- c(value, b)
        state <- "plain"
      }
    }
    i <- i + 1L
  }
  if (state == "quoted") stop("Unclosed CSV quote.")
  if (active) {
    records[[length(records) + 1L]] <- c(fields, rawToChar(as.raw(value)))
  }
  if (!length(records)) stop("CSV header is required.")
  header <- records[[1L]]
  if (!length(header) || anyDuplicated(header)) stop("Invalid CSV header.")
  if (any(lengths(records) != length(header))) stop("Unequal CSV field counts.")
  values <- unlist(records[-1L], use.names = FALSE)
  if (any(!validUTF8(c(header, values)))) stop("CSV must be valid UTF-8.")
  columns <- lapply(seq_along(header), function(j) {
    vapply(records[-1L], function(row) row[[j]], character(1L))
  })
  names(columns) <- header
  as.data.frame(columns, stringsAsFactors = FALSE, check.names = FALSE)
}

.write_csv_bytes <- function(df, path) {
  write.table(df, file = path, sep = ",", quote = TRUE, row.names = FALSE,
              col.names = TRUE, qmethod = "double", na = "", eol = "\r\n",
              fileEncoding = "UTF-8")
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 2L) stop("Usage: Rscript converted.R input.csv output.csv")
  .write_csv_bytes(translate(.read_csv_bytes(args[1L])), args[2L])
}
