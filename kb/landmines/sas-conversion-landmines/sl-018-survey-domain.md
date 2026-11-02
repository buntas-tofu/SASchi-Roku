# SL-018: Subsetting raw rows is not generally equivalent to domain analysis

Status: candidate migration research reference; not an agency finding.
Evidence: published contract plus original witness design, not a live-SAS receipt.
Scope: cited product/version only; target-runtime behavior must be checked.
Priority: P1, an engineering judgment, not an observed frequency.
Related rulebook entries: SV-002; SV-001, SV-003 adjacent.
Coverage assessment: Existing survey routing; verify variance design explicitly. An entry's existence is not an equivalence proof.

## Failure mechanism

Survey-domain estimation retains the sampling-design context. Dropping records before constructing the design can preserve a point estimate while changing its uncertainty.

## Witness to build (not executed here)

Use a multi-stratum clustered sample with a domain absent from some clusters. Compare raw-data filtering with domain estimation on the full design and examine standard errors and degrees of freedom.

## Preservation contract and mitigation (recommendation)

Build the complete survey design first and use its domain operation. Pin strata, clusters, finite-population corrections, replicate scaling, and singleton handling rather than replacing the analysis with weighted means.

## Promotion requirement

Record source and input hashes, SAS product/version and options, target lockfile,
observed output, comparator, and verdict. Confirm both the correct implementation
and a deliberately wrong alternative. Do not use this ingested witness description
as a held-out retrieval evaluation question.

## Sources

- S18: [SURVEYMEANS domain analysis](https://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/statug_surveymeans_examples02.htm). Scope: SAS/STAT 14.1 example. Consulted 2026-09-15.
- S19: [Considerations and Techniques for Analyzing Domains of Complex Survey Data](https://support.sas.com/resources/papers/proceedings13/449-2013.pdf). Scope: SAS Global Forum 2013; relevant domain-analysis section. Consulted 2026-09-15.
