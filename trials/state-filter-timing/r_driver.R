args <- commandArgs(trailingOnly = TRUE)
env <- new.env(parent = globalenv())
sys.source(args[[1]], envir = env)
df <- read.csv(args[[2]], colClasses = c("character", "numeric", "integer"),
               na.strings = "", check.names = FALSE, strip.white = FALSE)
before <- serialize(df, NULL)
first <- env$translate(df)
snapshot <- serialize(first, NULL)
second <- env$translate(df)
empty <- env$translate(df[FALSE, , drop = FALSE])
third <- env$translate(df)
tables <- c("where_path", "if_path")
columns <- c("row_id", "value", "prev", "total")
stopifnot(identical(before, serialize(df, NULL)), identical(snapshot, serialize(first, NULL)),
          identical(first, second), identical(first, third),
          is.list(first), identical(names(first), tables),
          is.list(empty), identical(names(empty), tables))
stopifnot(dir.create(args[[3]]))
for (table in tables) {
  for (result in list(first[[table]], empty[[table]])) {
    stopifnot(is.data.frame(result), identical(names(result), columns),
              is.character(result$row_id), all(vapply(result[-1], is.numeric, logical(1))),
              !any(vapply(result[-1], function(x) any(is.nan(x) | is.infinite(x)), logical(1))))
  }
  stopifnot(nrow(empty[[table]]) == 0L)
  write.csv(first[[table]], file.path(args[[3]], paste0(table, ".csv")), row.names = FALSE, na = "")
}
