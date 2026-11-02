args <- commandArgs(trailingOnly = TRUE)
env <- new.env(parent = globalenv())
sys.source(args[[1]], envir = env)
df <- read.csv(args[[2]], colClasses = c("character", "numeric", "integer", "integer"),
               na.strings = "", check.names = FALSE, strip.white = FALSE)
before <- serialize(df, NULL)
first <- env$translate(df)
snapshot <- serialize(first, NULL)
second <- env$translate(df)
stopifnot(identical(before, serialize(df, NULL)), identical(snapshot, serialize(first, NULL)),
          identical(first, second), is.list(first), identical(names(first), c("stage", "want")))
dir.create(args[[3]])
for (table in c("stage", "want")) {
  columns <- c("row_id", "value", "prev", "total", if (table == "want") "delta")
  stopifnot(is.data.frame(first[[table]]), identical(names(first[[table]]), columns),
            is.character(first[[table]]$row_id),
            all(vapply(first[[table]][-1], is.numeric, logical(1))))
  write.csv(first[[table]], file.path(args[[3]], paste0(table, ".csv")), row.names = FALSE, na = "")
}
