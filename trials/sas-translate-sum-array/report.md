# SAS translation trial

Status: engineering candidate for the principal's review. One supplied program
was executed in Python and checked against independently derived hand truth.
This is not a live SAS comparison or a claim of general SAS equivalence.

## Source and provenance

- Source: `/tmp/roku-skill-trial-20261101/source.sas`.
- Source SHA-256: `06eca942365b06dec7e0f99b077856b4b33391e8addee0b39a44c0170987ea1a`.
- Candidate: `/tmp/roku-skill-trial-20261101/candidate/converted.py`.
- Candidate SHA-256: `248dfb3e6e33d22180f516eedbaa21efc22f26c3319f802f60b7400ef38e13df`.
- Guidance read: `/tmp/roku-skill-trial-20261101/skill/SKILL.md` and its
  `references/evidence.md`.

The supplied source attributes the program to the Rosetta Code task
[Sum and product of an array](https://rosettacode.org/wiki/Sum_and_product_of_an_array),
page revision 408601, GFDL 1.2 (Rosetta_Code:Copyrights), retrieved
2026-09-08T14:05:31Z. These provenance claims are retained from the source and
were not independently verified. The source and language documentation are
candidate-tier evidence under the supplied contract.

## Behavior and comparison policy

Source inspection found one self-contained DATA _NULL_ step, no external inputs,
includes, macro dependencies, or output data sets. It fills 100 numeric array
elements with the squares of 1 through 100, computes their sum into `b`, and
executes `put b c;`. There is no product calculation or assignment to `c`.

Documentation-supported interpretation, still unproved against SAS execution:
`c` remains ordinary numeric missing and the step emits one logical PUT record.
SAS documents [initial missing values for DATA-step variables](https://support.sas.com/documentation/cdl/en/lrcon/62955/HTML/default/a001291423.htm)
and [list PUT output with periods for numeric missing values](https://support.sas.com/documentation/cdl/en/lestmtsref/63323/HTML/default/p0jcwhe1ofmb49n1xf1q2kc44b0v.htm).

The Python candidate fills the array using numeric floating-point values and
an inclusive loop, then sums it. Every element is assigned before summation,
so this source does not require a general missing-aware SUM implementation.
`math.nan` represents the unassigned numeric `c` internally; output maps it to
the requested period. There are no third-party dependencies.

Before implementation, the comparison contract was fixed as one logical record
containing the exact sum followed by ordinary numeric missing. The independent
arithmetic witness is `100 * 101 * 201 // 6 = 338350`, derived from the closed-form
sum-of-squares identity rather than the candidate's array loop. No numeric
tolerance is needed: all squares and partial sums are exactly representable at
this scale. The missing field is checked separately from the sum.

For this conversion, canonical stdout must be exactly `338350 .\n`, with one
space and one terminating newline. Field order, record count, missingness, and
absence of additional stdout are part of the check. Exact physical SAS log
layout and diagnostic notes are excluded by the task. No row or data-set schema
comparison applies because DATA _NULL_ creates no output data set.

## Checks actually run

Environment: CPython 3.12.3 on Linux x86_64, glibc 2.39. Python 3.11 itself was
not run. No packages were installed and no SAS process was executed.

1. Python `compile()` accepted the candidate source.
2. Calling `execute_data_step()` returned a float equal to the independently
   calculated 338350 and a float satisfying `math.isnan(c)`.
3. A separate Python process exited 0 with stdout `'338350 .\n'` and empty stderr.
4. The exact comparator rejected three deliberately incorrect record strings:
   `'338350\n'` (omitted `c`), `'338350 0\n'` (missing coerced to zero), and
   `'328350 .\n'` (100 squared omitted). These were comparator controls, not
   separately executed mutated programs.
5. A mechanical character scan checked both deliverables for forbidden em-dash
   and ellipsis sequences. The repository's linter was not run because reading
   repository tooling was outside the isolated trial's allowed inputs.

Reproduce the conversion from the candidate directory:

```sh
python3 converted.py
```

Reproduce the numerical and output checks with the standard library:

```sh
python3 - <<'PY'
import math
from pathlib import Path
import subprocess
import sys
from converted import execute_data_step

compile(Path('converted.py').read_text(), 'converted.py', 'exec')
n = 100
expected_sum = n * (n + 1) * (2 * n + 1) // 6
b, c = execute_data_step()
assert isinstance(b, float) and b == expected_sum
assert isinstance(c, float) and math.isnan(c)
expected = f'{expected_sum} .\n'
result = subprocess.run(
    [sys.executable, 'converted.py'], capture_output=True, text=True
)
assert result.returncode == 0 and result.stderr == ''
assert result.stdout == expected
for wrong in (f'{expected_sum}\n', f'{expected_sum} 0\n',
              f'{expected_sum - n*n} .\n'):
    assert wrong != expected
for path in (Path('converted.py'), Path('report.md')):
    text = path.read_text()
    assert '\u2014' not in text
    assert '\u2026' not in text
    assert chr(46) * 3 not in text
print('PASS: bounded hand-truth checks')
PY
```

## Verdict and remaining limits

The candidate passed the stated checks for this complete supplied program.
The numerical witness is independent of its implementation. The SAS missing
behavior is supported by documentation and source interpretation, not an
observed SAS baseline. A captured SAS logical record under the specified output
policy would resolve that remaining execution boundary.

No hidden evaluation material, sibling implementations, or prior expected
outputs were inspected. The evidence map's repository and teaching links were
not opened. Only primary SAS language references were used to support semantics.
The candidate is intentionally scoped to this source: its numeric formatting
and NaN representation are not general emulations of SAS formats, special
missing values, missing arithmetic, or other programs.
