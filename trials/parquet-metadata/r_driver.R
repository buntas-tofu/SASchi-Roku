# Parent consumer adapter. Candidate code supplies consume(), not expectations.
args <- commandArgs(trailingOnly=TRUE)
e <- new.env(parent=globalenv())
sys.source(args[1], envir=e)
x <- e$consume(args[2])
expected <- c('id','text','value','date','stamp','all_missing','status')
stopifnot(is.list(x), identical(names(x$data),expected))
n <- length(x$data$id)
stopifnot(is.character(x$data$id),is.list(x$data$text),inherits(x$data$date,'Date'))
for (name in expected) stopifnot(length(x$data[[name]])==n)
for (name in c('value','stamp','all_missing','status')) stopifnot(typeof(x$data[[name]])=='double')
stopifnot(all(vapply(x$data$text,is.raw,logical(1))))
stopifnot(is.data.frame(x$tags),is.data.frame(x$metadata),is.data.frame(x$labels))
stopifnot(identical(names(x$tags),c('row','column','tag')))
stopifnot(identical(names(x$metadata),c('column','property','type','value')))
stopifnot(identical(names(x$labels),c('column','value_hex','label_hex')))
hex <- function(x) paste(sprintf('%02x',as.integer(x)),collapse='')
rows <- list()
for (i in seq_len(n)) for (name in expected) {
  value <- x$data[[name]][[i]]
  if (name=='text') {
    kind <- 'text_hex'; encoded <- hex(value); tag <- ''
  } else if (name=='id') {
    kind <- 'text_hex'; encoded <- hex(charToRaw(enc2utf8(value))); tag <- ''
  } else {
    kind <- if (name=='date') 'date_iso' else 'float64_hex'
    found <- which(as.integer(x$tags$row)==i-1L & x$tags$column==name)
    if (is.na(value)) {
      stopifnot(length(found)==1L)
      encoded <- ''; tag <- x$tags$tag[found]
    } else {
      stopifnot(length(found)==0L)
      encoded <- if (name=='date') format(x$data$date[i],'%Y-%m-%d') else hex(writeBin(as.double(value),raw(),size=8,endian='little'))
      tag <- ''
    }
  }
  rows[[length(rows)+1L]] <- c(as.character(i-1L),name,kind,encoded,tag)
}
result <- if (length(rows)) as.data.frame(do.call(rbind,rows),stringsAsFactors=FALSE) else as.data.frame(setNames(rep(list(character()),5),c('row','column','kind','value','tag')))
names(result) <- c('row','column','kind','value','tag')
dir.create(args[3])
write.csv(result,file.path(args[3],'cells.csv'),row.names=FALSE,na='')
write.csv(x$metadata,file.path(args[3],'columns.csv'),row.names=FALSE,na='')
write.csv(x$labels,file.path(args[3],'labels.csv'),row.names=FALSE,na='')
