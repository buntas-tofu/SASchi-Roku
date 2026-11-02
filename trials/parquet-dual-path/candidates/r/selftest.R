# Engineering self-test; source-derived checks, not live SAS proof.
source("output/convert.R")
need(!file.exists("scratch"), "Self-test requires a new scratch directory")
dir.create("scratch")
for (name in c("main", "empty", "all-missing", "utf8", "reordered")) {
  convert(paste0("packet/synthetic/", name, ".json"), paste0("scratch/", name))
}
convert("packet/fixtures/sample.sas7bdat", "scratch/sample")
convert("packet/fixtures/missing.sas7bdat", "scratch/missing-no-catalog")
convert("packet/fixtures/missing.sas7bdat", "scratch/missing-catalog", "packet/fixtures/missing.sas7bcat")
cat("CONVERTED AND SELF-VALIDATED eight configurations\n")
base <- "scratch/selftest"
dir.create(base, recursive = TRUE, showWarnings = FALSE)
on.exit_cleanup <- function() unlink(base, recursive = TRUE)
reject <- function(label, thunk) {
  result <- tryCatch({thunk(); NULL}, error = function(e) conditionMessage(e))
  need(!is.null(result), paste("Unexpected acceptance:", label))
  cat("REJECTED", label, ":", result, "\n")
}
rewrite_meta <- function(out, mutate = identity) {
  p <- file.path(out, "metadata.json")
  m <- read_json(p)
  for (nm in names(m$files)) m$files[[nm]] <- sha(file.path(out, nm))
  writeLines(json_text(mutate(m)), p, useBytes = TRUE)
}
copy_output <- function(label) {
  dst <- file.path(base, label)
  need(dir.create(dst), "Could not create mutation directory")
  file.copy(list.files("scratch/main", full.names = TRUE), dst, recursive = TRUE)
  dst
}
input <- "packet/synthetic/main.json"
for (name in c("main", "empty", "all-missing", "utf8", "reordered")) {
  validate_output(paste0("packet/synthetic/", name, ".json"), paste0("scratch/", name))
  cat("VALIDATED", name, "\n")
}
validate_output("packet/fixtures/sample.sas7bdat", "scratch/sample")
validate_output("packet/fixtures/missing.sas7bdat", "scratch/missing-no-catalog")
validate_output("packet/fixtures/missing.sas7bdat", "scratch/missing-catalog", "packet/fixtures/missing.sas7bcat")
cat("VALIDATED all three SAS configurations\n")
for (mode in c("archive", "analysis")) {
  for (change in c("value", "reorder", "schema")) {
    out <- copy_output(paste(mode, change, sep = "-"))
    path <- file.path(out, paste0(mode, ".parquet"))
    tab <- read_parquet(path, as_data_frame = FALSE)
    df <- as.data.frame(tab)
    if (change == "value") df$amount[1] <- 33
    if (change == "reorder") df <- df[rev(seq_len(nrow(df))), , drop = FALSE]
    if (change == "schema") {
      arrays <- lapply(seq_along(df), function(i) Array$create(df[[i]], type = if (names(df)[i] == "__row_index") int32() else tab$schema$fields[[i]]$type))
      tab <- do.call(Table$create, setNames(arrays, names(df)))$ReplaceSchemaMetadata(tab$schema$metadata)
    } else tab <- Table$create(df, schema = tab$schema)$ReplaceSchemaMetadata(tab$schema$metadata)
    write_parquet(tab, path, compression = "uncompressed")
    rewrite_meta(out)
    reject(paste(mode, change, "with updated hashes"), function() validate_output(input, out))
  }
}
out <- copy_output("tags")
tab <- read_parquet(file.path(out, "archive.parquet"), as_data_frame = FALSE)
df <- as.data.frame(tab); df$amount__sas_missing[df$amount__sas_missing != ""] <- "."
write_parquet(Table$create(df, schema = tab$schema)$ReplaceSchemaMetadata(tab$schema$metadata), file.path(out, "archive.parquet"))
rewrite_meta(out)
reject("collapsed tags with updated hash", function() validate_output(input, out))
out <- copy_output("dates")
tab <- read_parquet(file.path(out, "analysis.parquet"), as_data_frame = FALSE)
df <- as.data.frame(tab); df$day <- df$day + 3653
write_parquet(Table$create(df, schema = tab$schema)$ReplaceSchemaMetadata(tab$schema$metadata), file.path(out, "analysis.parquet"))
rewrite_meta(out)
reject("wrong date origin with updated hash", function() validate_output(input, out))
out <- copy_output("metadata")
rewrite_meta(out, function(m) {m$columns[[1]]$label <- "altered"; m})
reject("altered descriptor", function() validate_output(input, out))
out <- copy_output("stale")
file.copy("scratch/utf8/metadata.json", file.path(out, "metadata.json"), overwrite = TRUE)
reject("swapped sidecar", function() validate_output(input, out))
out <- copy_output("source")
cat(" ", file = file.path(out, "source", basename(input)), append = TRUE)
reject("modified retained source", function() validate_output(input, out))
dir.create(file.path(base, "external"))
external <- file.path(base, "external", "main.json")
z <- read_json(input); z$rows[[1]]$amount$value <- 44
writeLines(json_text(z), external)
reject("wrong external source with same basename", function() validate_output(external, "scratch/main"))
out <- copy_output("corruption")
writeBin(as.raw(c(1, 2, 3)), file.path(out, "archive.parquet"))
rewrite_meta(out)
reject("corrupt parquet with updated hash", function() validate_output(input, out))
original <- sha("scratch/main/metadata.json")
reject("existing destination", function() convert(input, "scratch/main"))
need(identical(sha("scratch/main/metadata.json"), original), "Existing output changed")
x <- read_json(input)
variants <- list(
  reserved = function(z) {z$columns[[1]]$name <- "__row_index"; z},
  duplicate = function(z) {z$columns[[2]]$name <- z$columns[[1]]$name; z},
  width = function(z) {z$rows[[1]][[z$columns[[1]]$name]]$hex <- "00"; z},
  hex = function(z) {z$rows[[1]][[z$columns[[1]]$name]]$hex <- toupper(z$rows[[1]][[z$columns[[1]]$name]]$hex); z$rows[[1]][[z$columns[[1]]$name]]$hex <- "zz"; z},
  missing = function(z) {z$rows[[1]]$amount <- list(missing = ".AA"); z},
  date = function(z) {z$rows[[1]]$day <- list(value = 0.5); z},
  absent_cell = function(z) {z$rows[[1]]$amount <- NULL; z}
)
for (name in names(variants)) {
  path <- file.path(base, paste0(name, ".json")); out <- file.path(base, paste0(name, "-output"))
  writeLines(json_text(variants[[name]](x)), path)
  reject(paste("invalid envelope", name), function() convert(path, out))
  need(!file.exists(out), "Invalid input created output")
}
# Exercise a legal source name that overlaps a writer API parameter.
z <- x; old <- z$columns[[1]]$name; z$columns[[1]]$name <- "schema"
for (i in seq_along(z$rows)) names(z$rows[[i]])[names(z$rows[[i]]) == old] <- "schema"
path <- file.path(base, "name-test.json"); writeLines(json_text(z), path)
convert(path, file.path(base, "name-output"))
validate_output(path, file.path(base, "name-output"))
cat("VALIDATED legal API-parameter source name\n")
# Verify validation does not change any existing output files.
paths <- list.files("scratch/main", recursive = TRUE, full.names = TRUE)
before <- vapply(paths, sha, "")
validate_output(input, "scratch/main")
need(identical(before, vapply(paths, sha, "")), "Validation changed output")
on.exit_cleanup()
cat("SELFTEST PASSED\n")
