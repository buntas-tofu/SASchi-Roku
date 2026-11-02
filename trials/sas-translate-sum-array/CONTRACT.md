# Translation skill trial: sum and product source

Status: bounded evaluation contract recorded before candidate generation on
2026-11-01. Maintainers may use this trial to assess one skill invocation, not
as a general conversion benchmark or live-SAS equivalence claim.

## Source and scope

Use the complete unchanged Rosetta Code SAS program at
`references/rosetta-code/corpus/sum_and_product_of_an_array.sas`, SHA-256
`06eca942365b06dec7e0f99b077856b4b33391e8addee0b39a44c0170987ea1a`.
Use the initial `sas-translate` skill from Roku commit
`03fc5b3916b7423619b5e4308604215feb6b2c96`.
Target: Python 3.11+ standard library, standalone execution, no input datasets.

## Comparison policy (engineering decision)

Compare one logical PUT record containing two ordered fields. Numeric values
are compared exactly with decimal parsing for this bounded calculation; equivalent
numeric spellings are allowed. Preserve ordinary numeric missingness
as a period token. Normalize spacing between fields only; do not ignore extra
records or fields. Physical SAS log layout, diagnostic notes, BEST formatting,
platform state and live-SAS execution are outside this trial's acceptance claim.
No produced dataset is expected from DATA _NULL_. Preserve the source behavior,
including any discrepancy between its title and the actual statements.

The independent oracle is derived from a closed-form arithmetic identity and
published SAS initialization semantics. It is not computed by calling candidate
helpers or the Go implementation. Preserve a separately written oracle and
predeclare the comparator before inspecting candidate output. Exercise that same
comparator with plausible incorrect outputs and require their rejection.

## Evaluation boundary

A fresh agent receives only the skill bundle, complete source, neutral request,
and access to primary language documentation. It must not read the parent trial
artifacts, sibling implementations, prior expected outputs or tests. It writes
candidate code and an explanation in an isolated temporary folder. The parent
then inspects those files and executes the candidate independently.

This is one exploratory invocation. The task was deliberately selected by the
maintainer-facing agent for a useful semantic boundary, not randomly sampled.
The parent already knew the source from prior project context. The evaluation
agent receives no parent history or oracle, but that is not a claim of training
set novelty or a population success rate.
