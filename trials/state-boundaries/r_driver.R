# Parent adapter for the frozen base R interface, not candidate logic.
args <- commandArgs(trailingOnly=TRUE)
source(args[1], local=TRUE)
schema <- read.csv(args[2], colClasses="character", stringsAsFactors=FALSE)
inputs <- schema[schema$side == "input", , drop=FALSE]
outputs <- schema[schema$side == "output", , drop=FALSE]
read_tables <- function(directory) {
  result <- list()
  for (table in unique(inputs$table)) {
    spec <- inputs[inputs$table == table, , drop=FALSE]
    frame <- read.csv(file.path(directory,paste0(table,".csv")), colClasses="character",
                      na.strings=NULL, strip.white=FALSE, check.names=FALSE,
                      stringsAsFactors=FALSE, comment.char="")
    stopifnot(identical(names(frame), spec$column))
    for (i in seq_len(nrow(spec))) {
      if (spec$type[i] == "number") {
        values <- frame[[i]]
        values[values == ""] <- NA_character_
        frame[[i]] <- as.numeric(values)
      }
    }
    result[[table]] <- frame
  }
  result
}
validate <- function(tables) {
  stopifnot(is.list(tables), identical(names(tables), unique(outputs$table)))
  for (table in names(tables)) {
    frame <- tables[[table]]
    spec <- outputs[outputs$table == table, , drop=FALSE]
    stopifnot(is.data.frame(frame), identical(names(frame),spec$column))
    for (i in seq_len(nrow(spec))) {
      if (spec$type[i] == "text") stopifnot(is.character(frame[[i]]), !anyNA(frame[[i]]))
      else stopifnot(is.numeric(frame[[i]]), !any(is.nan(frame[[i]])), !any(is.infinite(frame[[i]])))
    }
  }
}
tables <- read_tables(args[3])
before <- serialize(tables,NULL)
if (length(args) == 5 && args[5] == "--reject") {
  rejected <- tryCatch({translate(tables); FALSE}, error=function(e) TRUE)
  stopifnot(rejected, identical(serialize(tables,NULL),before))
} else {
  result <- translate(tables)
  validate(result)
  saved <- serialize(result,NULL)
  empty <- lapply(tables,function(x) x[FALSE,,drop=FALSE])
  validate(translate(empty))
  stopifnot(identical(serialize(translate(tables),NULL),saved),
            identical(serialize(result,NULL),saved), identical(serialize(tables,NULL),before))
  stopifnot(dir.create(args[4]))
  for (table in names(result)) write.table(result[[table]],file.path(args[4],paste0(table,".csv")),
    sep=",",quote=TRUE,row.names=FALSE,col.names=TRUE,na="",qmethod="double",fileEncoding="UTF-8")
}
