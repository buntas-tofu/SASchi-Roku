# LQ-006: Matching a keyword does not establish a relevant SAS construct

Status: candidate reference for migration practitioners; not an agency finding.
Evidence class: Project-derived failure pattern; local provenance is retained outside ingestion.
Runtime status: no model experiment or SAS execution performed for this card.
Family: retrieval.

## Evidence and limits

Project-derived risk: searches for masking can retrieve training-label masks, UI escaping, or namespace masking rather than macro quoting. The public macro reference defines the intended mechanism; it does not measure our retrieval accuracy.

## SAS migration scenario (illustrative)

A candidate with the word mask is promoted as evidence about %SUPERQ even though its code is part of a model-training pipeline.

## Recommended control (inference)

Require the exact SAS token, source location, operation, and a relevance disposition. No relevant construct is a valid result, not a failed extraction.

## Proposed evaluation, not a measured result

Mix true macro-quoting passages with unrelated uses of masking. Score relevance separately from whether the emitted record parses.

Keep new evaluation inputs and answers outside the retrieved teaching corpus.
Model name, revision, prompt, retrieved content, tool environment, and generation
settings must accompany any later empirical result.

## Sources

- S25: [SAS macro quoting](https://support.sas.com/documentation/cdl/en/mcrolref/62978/HTML/default/n0o0rjikrg6iezn1ltra79iamibr.htm). Scope: SAS 9.3 macro reference. Consulted 2026-09-15.
