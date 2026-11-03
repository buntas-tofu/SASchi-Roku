# Command, failure and repair history

Status: local execution record for maintainers evaluating this Python submission. This is not a parent-evaluator verdict or live-SAS proof. Commands ran only in `/tmp/roku-parquet-evaluation-mzmr7dqs/python`. No other evaluation outputs, repository code or expected answers were read.

## Discovery and reader probe

1. `pwd && rg --files packet . | head -80` listed the isolated packet. Exit 0.
2. `cat packet/AGENTS.md packet/request.txt packet/CONTRACT.md packet/FIXTURES.json packet/skills/sas-define-interchange/SKILL.md packet/skills/sas-define-interchange/references/representations.md packet/skills/sas-to-parquet/SKILL.md packet/skills/sas-to-parquet/references/preservation.md` read all assigned authority and both skills/references. Exit 0.
3. `cat packet/synthetic/*.json` read all five admitted envelopes. Exit 0.
4. Initial exploratory command, exit 1:

```python
# Executed using /tmp/roku-interchange-runtime/bin/python -
import inspect, pyreadstat, pyarrow, pandas
print(pyreadstat.__version__, pyarrow.__version__, pandas.__version__)
print(pyreadstat.read_sas7bdat.__doc__)
print(pyreadstat.read_sas7bcat.__doc__)
for path in ['packet/fixtures/sample.sas7bdat','packet/fixtures/missing.sas7bdat']:
    for cat in [None]+(['packet/fixtures/missing.sas7bcat'] if 'missing' in path else []):
        d,m=pyreadstat.read_sas7bdat(path,catalog_file=cat,user_missing=True,
            disable_datetime_conversion=True,apply_value_formats=False)
        print(path,cat); print(d.to_dict(orient='list')); print(vars(m))
```

Observed versions were 1.3.7, 25.0.1, 3.1.0. The first read failed with `TypeError: read_sas7bdat() got an unexpected keyword argument 'apply_value_formats'`. This was exploratory misuse, not a conversion pass. Installed documentation states direct catalogs replace codes. Repair: remove the unsupported argument and read data without a catalog, then parse catalogs separately.

5. Repaired exploratory command, exit 0:

```python
# Executed using /tmp/roku-interchange-runtime/bin/python -
import pyreadstat
for path in ['packet/fixtures/sample.sas7bdat','packet/fixtures/missing.sas7bdat']:
    d,m=pyreadstat.read_sas7bdat(path,user_missing=True,
        disable_datetime_conversion=True,output_format='dict')
    print(path); print({k:list(v) for k,v in d.items()}); print(vars(m))
_,m=pyreadstat.read_sas7bcat('packet/fixtures/missing.sas7bcat')
print('CATALOG',vars(m))
```

Observed sample rows: 5. Observed missing-data rows: 1. Reader exposed source widths, formats, informats and UTF-8 data encoding. Catalog exposed WINDOWS-1252 encoding and a value-label mapping for a special missing tag. No input files changed.

6. Primary-document web searches: `site.pyreadstat.readthedocs.io read_sas7bdat user_missing disable_datetime_conversion` and `site.arrow.apache.org docs python parquet schema metadata timestamp date32`. Opened the documented source pages listed in the report. `https://ofajardo.github.io/pyreadstat_documentation/_build/html/index.html` failed with UnexpectedStatusCode. `https://arrow.apache.org/docs/python/parquet.html` returned 404. Repair: read the official repository documentation and `https://arrow.apache.org/docs/python/parquet/index.html`.

## Implementation and first execution

`mkdir -p output`, then a heredoc wrote `output/convert.py`. The exact implementation is the delivered file. First execution:

```text
/tmp/roku-interchange-runtime/bin/python output/convert.py convert packet/synthetic/main.json trial-main
```

Exit 0: `convert: complete source-derived check, 5 rows`.

Code review before the full test found that filename suffixes should not determine source behavior. Repair: sniff JSON object/array content; use the SAS reader otherwise. Metadata comparison was tightened to distinguish JSON boolean values from integers through canonical serialization. Both were pre-delivery changes.

A heredoc wrote `output/selftest.py`. The delivered source retains the complete command construction and assertions; all outputs it creates are temporary.

## Self-test run 1 and consumer repair

```text
/tmp/roku-interchange-runtime/bin/python output/selftest.py > selftest.log 2>&1
cat selftest.log
```

The test process failed, exit 1. The surrounding shell ended with `cat`, exit 0; that shell result did not indicate a test pass. Five envelope conversions/validations, three SAS conversions/validations and two renamed-input conversions had succeeded. The R schema-introspection assertion then failed:

```text
Error in as.vector(x, "character") :
  cannot coerce type 'environment' to vector of type 'character'
Calls: stopifnot -> as.character -> as.character.default
Execution halted
AssertionError
```

This failure was in the R self-test's conversion of a DataType environment, not a written Parquet schema failure. Direct inspection used:

```r
# /tmp/roku-interchange-runtime/bin/Rscript -
library(arrow)
a <- read_parquet('trial-main/analysis.parquet', as_data_frame=FALSE)
print(a$schema$GetFieldByName('day')$type$ToString())
print(a$schema$GetFieldByName('__row_index')$type$ToString())
print(a$schema$metadata)
```

Exit 0, observing `date32[day]`, `int64` and expected analysis bindings. Repair: replace R `as.character(type)` assertions with `type$ToString()` in the test. Converter unchanged.

## Self-test run 2

```text
/tmp/roku-interchange-runtime/bin/python output/selftest.py > selftest-second.log 2>&1
```

Exit 0. Result: 47 CLI assertions, eight R-consumed output pairs, all temporary self-test data removed. All expected negative cases were rejected. No conversion repair followed this run.

First unchanged linter run:

```text
python3 inertia-drift-lint output
```

Exit 0: `clean: no drift caught`.

## Final self-test expansion and run 3

Expanded only the self-test with descriptor format/catalog label assertions and a generated matrix covering every single-byte CP1252 value and all 28 numeric missing markers. Converter unchanged.

```text
/tmp/roku-interchange-runtime/bin/python output/selftest.py > selftest-third.log 2>&1
```

Exit 0. Exact CLI command/outcome log follows. Temporary path names are historical and do not denote delivered artifacts.

```text
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/all-missing.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case0 => 0 convert: complete source-derived check, 1 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/all-missing.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case0 => 0 validate: complete source-derived check, 1 rows
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/all-missing.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case0 => 1 ERROR: destination already exists
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/empty.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case1 => 0 convert: complete source-derived check, 0 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/empty.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case1 => 0 validate: complete source-derived check, 0 rows
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/empty.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case1 => 1 ERROR: destination already exists
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case2 => 0 convert: complete source-derived check, 5 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case2 => 0 validate: complete source-derived check, 5 rows
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case2 => 1 ERROR: destination already exists
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/reordered.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case3 => 0 convert: complete source-derived check, 3 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/reordered.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case3 => 0 validate: complete source-derived check, 3 rows
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/reordered.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case3 => 1 ERROR: destination already exists
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/utf8.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case4 => 0 convert: complete source-derived check, 2 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/utf8.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case4 => 0 validate: complete source-derived check, 2 rows
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/utf8.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/case4 => 1 ERROR: destination already exists
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/sample.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas5 => 0 convert: complete source-derived check, 5 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/sample.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas5 => 0 validate: complete source-derived check, 5 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas6 => 0 convert: complete source-derived check, 1 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas6 => 0 validate: complete source-derived check, 1 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas7 --catalog /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bcat => 0 convert: complete source-derived check, 1 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas7 --catalog /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bcat => 0 validate: complete source-derived check, 1 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/byte-matrix.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/byte-matrix-out => 0 convert: complete source-derived check, 256 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/byte-matrix.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/byte-matrix-out => 0 validate: complete source-derived check, 256 rows
BYTE MATRIX PASS: 256 CP1252 byte cells; all 28 canonical missing tags
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/renamed2.opaque /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/renamed-out2 => 0 convert: complete source-derived check, 5 rows
PASS /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/renamed5.opaque /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/renamed-out5 => 0 convert: complete source-derived check, 5 rows
R COMMAND /tmp/roku-interchange-runtime/bin/Rscript /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/consumer.R [eight output directories] => 0
R consumer PASS case0 rows 1 
R consumer PASS case1 rows 0 
R consumer PASS case2 rows 5 
R consumer PASS case3 rows 3 
R consumer PASS case4 rows 2 
R consumer PASS sas5 rows 5 
R consumer PASS sas6 rows 1 
R consumer PASS sas7 rows 1 
 
Attaching package: ‘arrow’

The following object is masked from ‘package:utils’:

    timestamp


REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-changed-rehashed => 1 ERROR: complete typed value mismatch: analysis.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-tags-rehashed => 1 ERROR: complete typed value mismatch: archive.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-date-rehashed => 1 ERROR: complete typed value mismatch: analysis.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-reordered-rehashed => 1 ERROR: complete typed value mismatch: analysis.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-corrupt => 1 ERROR: Could not open Parquet input source '/tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-corrupt/archive.parquet': Parquet file size is 7 bytes, smaller than the minimum file footer (8 bytes)
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-source-copy => 1 ERROR: retained source bytes changed
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/reordered.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-wrong-external => 1 ERROR: schema or binding mismatch: archive.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-swapped-sidecar => 1 ERROR: metadata disagrees with source-derived contract or output identity
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-stale-descriptor => 1 ERROR: metadata disagrees with source-derived contract or output identity
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-missing-events => 1 ERROR: metadata disagrees with source-derived contract or output identity
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/synthetic/main.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/attack-schema-binding => 1 ERROR: schema or binding mismatch: analysis.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas7 => 1 ERROR: schema or binding mismatch: archive.parquet
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py validate /tmp/roku-parquet-evaluation-mzmr7dqs/python/packet/fixtures/missing.sas7bdat /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/sas7 --catalog /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/wrong-catalog => 1 ERROR: Unable to read from file
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-reserved.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-reserved => 1 ERROR: reserved column name: __row_index
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-suffix.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-suffix => 1 ERROR: reserved column name: id__sas_missing
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-duplicate.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-duplicate => 1 ERROR: duplicate column name: id
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-uppercase-hex.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-uppercase-hex => 1 ERROR: hex must be lowercase byte pairs
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-odd-hex.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-odd-hex => 1 ERROR: hex must be lowercase byte pairs
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-width.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-width => 1 ERROR: physical byte width mismatch
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-bad-tag.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-bad-tag => 1 ERROR: invalid SAS missing marker
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-boolean.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-boolean => 1 ERROR: numeric requires finite value or canonical missing
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-ambiguous.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-ambiguous => 1 ERROR: numeric requires finite value or canonical missing
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-fractional-date.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-fractional-date => 1 ERROR: fractional SAS date cannot be represented exactly as date32
REJECT /tmp/roku-interchange-runtime/bin/python /tmp/roku-parquet-evaluation-mzmr7dqs/python/output/convert.py convert /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-codec.json /tmp/roku-parquet-evaluation-mzmr7dqs/python/selftest-f9ewcleg/bad-out-codec => 1 ERROR: unknown encoding: nonexistent-codec
SELFTEST COMPLETE: 49 CLI assertions; 8 R-consumed projections pairs; temporary artifacts removed
```

## Identity, environment and final delivery checks

An installed-runtime Python probe printed `sys.version` and recomputed every `packet/FIXTURES.json` SHA-256 using `hashlib.sha256(p.read_bytes()).hexdigest()` for `Path('packet/fixtures') / item['filename']`. Exit 0. Python was 3.12.16, build GCC 15.3.0. All four identities matched:

```text
LICENSE 07487bc4080297d9c65ffa3f66e3c405f9fd08e4af990cd54212d373eb28debc
sample.sas7bdat 007425379a0504f5c54a7c0bb8f9776670a2456d3692f37907d38e080ac4b07b
missing.sas7bdat 620f8eac41710b7ea4293a5ab4a0fb8d1fbc886fa5fa2d0d2165f45a7a10865c
missing.sas7bcat d1fc24e992e8fbd921d614615ff7281fec58d6b705e2de227e813bd6867c8c91
```

The exact environment probe command for R was:

```text
/tmp/roku-interchange-runtime/bin/Rscript -e 'cat(R.version.string,"; arrow",as.character(packageVersion("arrow")),"; jsonlite",as.character(packageVersion("jsonlite")),"; haven",as.character(packageVersion("haven")),"\n")'
```

Exit 0: R 4.4.3, arrow 25.0.1, jsonlite 2.0.0, haven 2.5.5.

A heredoc wrote `output/report.md`, and a Python script created this history from the recorded final run. No parent files or expected answers were read. The unchanged linter then ran on all four delivered files:

```text
python3 inertia-drift-lint output
```

Exit 0: `clean: no drift caught`.

Cleanup removed `trial-main`, `selftest.log`, `selftest-second.log` and `selftest-third.log` after preserving execution evidence here. All three self-test contexts had already removed their temporary input/output data. The delivered directory contains only `convert.py`, `selftest.py`, `report.md` and `history.md`, with no generated data, copied packet, cache, package or symlink.

Final repeat after this history append: `python3 inertia-drift-lint output`, exit 0, `clean: no drift caught`. The final tool output is the external receipt for this statement. No linter edits were made.
