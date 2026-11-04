# Julia relational fixture: first bounded runtime evaluation

Status: candidate trial submitted for maintainer and hosted execution review, 2026-11-04. No Julia execution or SAS equivalence is claimed until a linked run succeeds.

## Source and frozen oracle

The user authorized Julia evaluation after merging PR 13. This first batch reuses the pre-existing [Python reference fixture](../../references/python-libraries/fixtures/README.md) and its independent [expected.json](../../references/python-libraries/fixtures/expected.json). The source is **not** a native SAS execution. [freeze.json](freeze.json) records the Git blob IDs at main commit 0721f317.

The oracle includes five customers, eight orders, leading-zero identifiers, an orphan foreign key, two null measures, a genuine zero, a negative amount, total 4350 integer cents and an all-null group that must remain null.

## Two bounded Julia implementations

- [candidate_base.jl](candidate_base.jl): Base Julia implementation using an intentionally limited parser for the fixture's simple unquoted CSV. This is not general CSV functionality.
- [candidate_dataframes.jl](candidate_dataframes.jl): independent DataFrames.jl and CSV.jl implementation with typed string keys and explicit missing-policy handling.
- [Project.toml](Project.toml): Julia 1.10 compatibility, exact direct CSV 0.10.16 and DataFrames 1.8.2 constraints. No committed Manifest is claimed; CI retains the resolved Manifest artifact.
- [verify.py](verify.py): independent Python standard-library comparator that reads existing expected.json but is never imported by the Julia candidates.
- [test_refusals.py](test_refusals.py): two malformed input cases per candidate, requiring a nonzero exit and no output file.

Eight mutated-output negative controls test the comparator's sensitivity. The tests specifically target row omission, incorrect negative arithmetic, zero/null confusion, incorrect counts, ordering and duplicate group output.

## What success would establish

One passing hosted job establishes the candidate's observed behavior on the frozen fixture, at that runner's exact Julia and package versions, with the recorded checks. It does not establish SAS DATA-step queue state, general BY merge semantics, original SAS metadata fidelity, statistical inference, full language support or enterprise installation.

The candidates were deliberately authored with knowledge of the fixture; this is not a blinded independent agent evaluation. The frozen JSON oracle remains separate and unchanged, but matching it does not make a general SAS correctness claim.

## Executing and preserving evidence

The dedicated [Julia workflow](../../.github/workflows/julia-fixture-evaluation.yml) runs two isolated GitHub-hosted jobs with Julia 1.10.13 LTS. The workflow pins checkout, setup-julia and artifact-upload actions to commit SHAs, constrains direct Julia package versions, and retains outputs, comparator receipt and environment manifest in short-lived run artifacts.

For an already approved Julia environment, the Base candidate interface is:

    julia --startup-file=no trials/julia-fixture/candidate_base.jl references/python-libraries/fixtures/customers.csv references/python-libraries/fixtures/orders.csv /tmp/julia-base.tsv
    python3 trials/julia-fixture/verify.py /tmp/julia-base.tsv

DataFrames uses the equivalent candidate with --project=trials/julia-fixture. The comparator refuses to overwrite an existing receipt. Do not run Pkg.instantiate on a managed client without authorization.

This landing leaves the original ten-job governance workflow, source corpus, stamped KB, external discovery catalog, existing trials, MCP and original software licensing decision unchanged. It adds a trial-only workflow, not a general translation service.
