# Independent parent reader. No converter helper is imported.
args <- commandArgs(trailingOnly=TRUE)
observed <- list()
for (mode in c("archive","analysis")) {
  tab <- arrow::read_parquet(file.path(args[1],paste0(mode,".parquet")),as_data_frame=FALSE)
  frame <- as.data.frame(tab)
  fields <- tab$schema$fields
  schema <- lapply(fields,function(field) list(field$name,field$type$ToString()))
  rows <- lapply(seq_len(nrow(frame)),function(i) {
    lapply(frame,function(column) {
      v <- column[i]
      if (is.na(v)) return(NULL)
      if (inherits(v,"Date")) return(unname(as.numeric(v)))
      if (inherits(v,"POSIXct")) return(unname(as.numeric(v)*1000000))
      if (inherits(v,"integer64")) return(unname(as.numeric(v)))
      if (is.numeric(v)) return(unname(as.numeric(v)))
      unname(as.character(v))
    })
  })
  # Row arrays preserve source order and duplicate identifiers without keying.
  rows <- lapply(rows,unname)
  observed[[mode]] <- list(schema=schema,rows=rows,metadata=tab$schema$metadata)
}
jsonlite::write_json(observed,args[2],auto_unbox=TRUE,null="null",na="null",digits=NA,pretty=TRUE)
