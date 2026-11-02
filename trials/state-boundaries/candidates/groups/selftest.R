# Direct API checks; expectations are independently derived hand rows.
source('output/converted.R')
have <- data.frame(row_id = c('0007', 'NA', '  text,"quoted"  '),
                   region = c(NA_real_, NA_real_, 2),
                   account = c(NA_real_, 7, 7), value = c(3, NA_real_, 4),
                   stringsAsFactors = FALSE)
before <- unserialize(serialize(have, NULL))
want <- data.frame(row_id = have$row_id, region = have$region,
                   account = have$account, value = have$value,
                   raw_prev = c(NA_real_, 3, NA_real_), prev = rep(NA_real_, 3),
                   total = c(103, 103, 104), first_region = c(1, 0, 1),
                   last_region = c(0, 1, 1), first_account = c(1, 1, 1),
                   last_account = c(1, 1, 1), stringsAsFactors = FALSE)
actual <- translate(list(have = have))
stopifnot(identical(actual, list(want = want)), identical(have, before))
empty <- have[FALSE, ]
empty_result <- translate(list(have = empty))$want
stopifnot(nrow(empty_result) == 0L, identical(names(empty_result), output_columns),
          is.character(empty_result$row_id),
          all(vapply(empty_result[-1L], is.numeric, logical(1))))
stopifnot(identical(translate(list(have = have)), actual))
actual$want$row_id[1] <- 'modified'
stopifnot(identical(have, before))
integer_input <- data.frame(row_id = 'i', region = 1L, account = NA_integer_, value = 0L)
stopifnot(translate(list(have = integer_input))$want$total == 100)
for (bad in list(have[3:1, ], transform(have, account = as.character(account)),
                 transform(have, value = c(NaN, 0, 1)))) {
  error <- tryCatch({translate(list(have = bad)); FALSE}, error = function(e) TRUE)
  stopifnot(error)
}
cat('PASS R API: hand trace, numeric schemas, fresh calls, input preservation, 3 rejection cases\n')
