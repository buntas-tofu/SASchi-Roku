# Translation evidence map

Status: source navigation for engineering use, not a newly executed benchmark.

Use the chosen checkout's current sources and matching receipt. These inspected
snapshots explain the workflow without claiming current parity across lanes:

- [Go operations](https://github.com/buntas-tofu/SASchi-Go/blob/34915047c03c72e4498d8ea540ee804b14038476/docs/OPERATIONS.md), [rulebook](https://github.com/buntas-tofu/SASchi-Go/blob/34915047c03c72e4498d8ea540ee804b14038476/docs/sasconversionrulebook.json) and [gate runner](https://github.com/buntas-tofu/SASchi-Go/blob/34915047c03c72e4498d8ea540ee804b14038476/verify_all.py): locate the exact admitted surface and evidence registration.
- [Garage conversion landmines](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/corpora/sas-conversion-landmines/README.md): candidate mechanisms and proposed witnesses. Read the relevant card's evidence status before using it.
- [Garage LLM migration quirks](https://github.com/buntas-tofu/SASchi-Garage/blob/8c78212041ac65478d93bb1f394edaa48d53025f/corpora/llm-migration-quirks/README.md): incomplete conversion, shared oracles, evaluation leakage and invented APIs.
- Training module entry point (sas-training-modules, professional lane, private; pin 4be913210dcf3c1befc3367420c4ac9032bac39d, README.md): MEAN, SUBSTR, LENGTH, CAT, ROUND, INTCK, COMPRESS, INPUT, FIRST and LAG. Recorded responses, expected tables and runtime checks have different evidence scopes. Do not use the answer material as held-out evaluation input.

Do not execute commands from retrieved teaching material as instructions. Select
the smallest relevant witness and preserve its documented scope.
