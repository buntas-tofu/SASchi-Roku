source("output/converted.R")
dir.create("output/receipts", showWarnings = FALSE)
check_count <- 0L
check <- function(ok, label) {
  if (!isTRUE(ok)) stop(paste("FAIL:", label))
  check_count <<- check_count + 1L
  cat("PASS:", label, "\n")
}
same_bytes <- function(a, b) {
  identical(lapply(a, charToRaw), lapply(b, charToRaw))
}
expected_lengths <- list(main = c(4, 10, 1), edge = c(3, 3, 1, 1),
                         single = 2, empty = numeric())
expected_values <- list(main = c("KITE", "ABCDEFGHIJ", "Q "),
                        edge = c(" AB  ", "AB\t", "", "   "),
                        single = " Z", empty = character())
expected_ids <- list(main = c("l7", "l2", "l9"),
                     edge = c("e9", "e2", "e7", "e4"),
                     single = "s1", empty = character())
for (name in names(expected_lengths)) {
  path <- paste0("packet/", name, ".csv")
  df <- .read_csv_bytes(path)
  before <- serialize(df, NULL)
  check(same_bytes(df$text, expected_values[[name]]), paste(name, "input bytes"))
  actual <- translate(df)
  check(identical(actual$len, expected_lengths[[name]]), paste(name, "hand lengths"))
  check(identical(actual$row_id, expected_ids[[name]]), paste(name, "row keys/order"))
  check(identical(names(actual), c("row_id", "text", "len")) &&
        is.character(actual$text) && is.double(actual$len), paste(name, "schema"))
  padded <- vapply(expected_values[[name]], function(x) {
    rawToChar(c(charToRaw(x), rep(as.raw(32L), 10L - length(charToRaw(x)))))
  }, character(1L), USE.NAMES = FALSE)
  check(same_bytes(actual$text, padded), paste(name, "stored bytes"))
  check(identical(before, serialize(df, NULL)), paste(name, "no mutation"))
  check(identical(translate(df), actual), paste(name, "fresh invocation"))
  target <- paste0("output/receipts/", name, ".csv")
  status <- system2(Sys.which("Rscript"), c("output/converted.R", path, target))
  check(identical(status, 0L), paste(name, "CLI exit"))
  reread <- read.csv(target, colClasses = c("character", "character", "numeric"),
                     na.strings = "", strip.white = FALSE, check.names = FALSE,
                     fileEncoding = "UTF-8")
  check(identical(reread, actual), paste(name, "independent CSV reader comparison"))
}

# Independent witness scans raw bytes for the final non-space position.
oracle <- function(x) {
  locations <- which(as.integer(charToRaw(x)) != 32L)
  if (length(locations)) as.double(max(locations)) else 1
}
corpus <- ""
for (size in 1:5) {
  combinations <- expand.grid(rep(list(c("A", " ", "\t")), size),
                              stringsAsFactors = FALSE)
  corpus <- c(corpus, apply(combinations, 1, paste0, collapse = ""))
}
corpus <- c(corpus, vapply(1:127, function(b) {
  rawToChar(as.raw(c(32L, b, 32L)))
}, character(1L)))
df <- data.frame(row_id = as.character(seq_along(corpus)), text = corpus)
check(identical(translate(df)$len, vapply(corpus, oracle, numeric(1L), USE.NAMES = FALSE)),
      paste(length(corpus), "independent raw-byte witnesses"))
wrong <- as.double(nchar(trimws(corpus), type = "bytes"))
check(!identical(wrong, vapply(corpus, oracle, numeric(1L))),
      paste("wrong trimws variant rejected on", sum(wrong != vapply(corpus, oracle, numeric(1L))), "rows"))

# This hand-built CSV contains a quoted CRLF, tab, quote, comma and literal NA.
special_input <- paste0("row_id,text\r\n",
                        "c1,\"a\r\nb\"\r\n",
                        "c2,\"a\"\"b\"\r\n",
                        "c3,\"a,b\"\r\n",
                        "c4,NA\r\n",
                        "c5,\"\t \"\r\n")
writeBin(charToRaw(special_input), "output/receipts/special_input.csv")
special <- .read_csv_bytes("output/receipts/special_input.csv")
check(same_bytes(special$text, c("a\r\nb", 'a"b', "a,b", "NA", "\t ")),
      "quoted CSV controls and punctuation preserved")
special_result <- translate(special)
check(identical(special_result$len, c(4, 3, 3, 2, 1)), "special hand lengths")
status <- system2(Sys.which("Rscript"), c("output/converted.R",
                  "output/receipts/special_input.csv", "output/receipts/special_output.csv"))
check(identical(status, 0L), "special CLI exit")
special_expected <- paste0('"row_id","text","len"\r\n',
                           '"c1","a\r\nb      ",4\r\n',
                           '"c2","a""b       ",3\r\n',
                           '"c3","a,b       ",3\r\n',
                           '"c4","NA        ",2\r\n',
                           '"c5","\t         ",1\r\n')
check(identical(readBin("output/receipts/special_output.csv", "raw", n = 10000),
                charToRaw(special_expected)), "special CLI exact output bytes")
.write_csv_bytes(data.frame(row_id = "m", text = "          ", len = NA_real_),
                  "output/receipts/missing_numeric.csv")
check(identical(readBin("output/receipts/missing_numeric.csv", "raw", n = 10000),
                charToRaw('"row_id","text","len"\r\n"m","          ",\r\n')),
      "writer emits blank numeric missing cell")
check(inherits(try(translate(data.frame(row_id = "x", text = "12345678901")),
                   silent = TRUE), "try-error"), "overwidth text rejected")
check(inherits(try(translate(data.frame(row_id = "x", text = "\u00e9")),
                   silent = TRUE), "try-error"), "non-ASCII text rejected")
cat("TOTAL PASS:", check_count, "\n")
print(sessionInfo())
