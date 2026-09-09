# Rosetta Code SAS Corpus

A clean, provenance-pinned harvest of every SAS solution currently on
[Rosetta Code](https://rosettacode.org/wiki/Category:SAS) (56 tasks, 100% of
the category as of 2026-09-08).

The same task solved in many languages is the whole point of Rosetta Code,
and this corpus keeps the SAS side: real-world SAS written by community
contributors, from the classics (FizzBuzz, Fibonacci, N-queens, Sudoku) to
genuinely statistical material (Welch's t-test, QR decomposition,
P-value correction, cumulative standard deviation, merge-and-aggregate).

## Layout

- `corpus/` : one `.sas` file per task, named by a slug of the task title.
  Every file opens with a provenance header: source URL, page revision ID,
  license note, retrieval time.

## Provenance and license

- Source: https://rosettacode.org/wiki/Category:SAS
- License: GFDL 1.2, per Rosetta_Code:Copyrights (contributors may also
  grant more permissive terms; page history is the authority).
- Every file pins its task URL and page revision ID; the revision ID makes
  any file reproducible against the exact wikitext it was extracted from.

## Refresh

The harvest is reproducible: query the category member list, fetch each
task's wikitext via the MediaWiki API, extract the `{{header|SAS}}`
sections. The upstream category grows; re-run the same extraction whenever
a fresh snapshot is wanted.

## Notes

- Multiple examples per task are kept in one file, separated by numbered
  comment banners.
- Code blocks inside a SAS header section are captured regardless of the
  block's language label; Rosetta labels are not always reliable (PROC IML
  has shipped as `lang=text`, PROC SQL as `lang=sql`).
- This is community probe material, not verified gold: nothing here is a
  correctness claim until it has been executed and checked.
