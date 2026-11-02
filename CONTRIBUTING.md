# Contributing

Keep the toolkit useful through bounded workflows, traceable sources and checks
that can fail. The project scope is recorded in
[decision 0001](docs/decisions/0001-toolkit-scope.md).

## Reference collection

The original corpus now lives under `references/rosetta-code/`. Preserve its
headers and indexes. From the repository root:

```sh
python3 tools/fetch_rosetta_sas.py --check
python3 tools/fetch_rosetta_sas.py
python3 scripts/check_corpus_index.py
```

The first command checks upstream and writes nothing. The second refreshes the
collection and can remove files that left the upstream category. Review that
diff deliberately. It is a separate operation from relocating the collection.
See the [collection contribution guide](references/rosetta-code/CONTRIBUTING.md).
The original migration receipt is historical; later refreshes record their own
changes rather than overwriting that receipt.

## Resource catalog

Edit `catalog/resources.json`, then regenerate the human index:

```sh
python3 scripts/check_toolkit.py --write-index
python3 scripts/check_toolkit.py
```

Use stable resource IDs. Record where an item was found, the inspected revision,
and what was actually checked. Unknown upstream URLs stay null. Preserve dated
census counts as historical observations. An API license identifier is a lookup
result, not a review of every file or a grant to redistribute a tree.
Prefer links to imported copies; copying material requires a distinct provenance
and rights review. Do not add local account paths, private data or credentials.

## Skills

Create one folder per useful task with a `SKILL.md` containing `name` and
`description` frontmatter. Describe a precise trigger. Keep supporting references
inside the skill so it can be installed separately. Link to source evidence;
distinguish instructions, implemented behavior, and measured outcomes.

Do not turn a rulebook entry, teaching example or successful parse into an
equivalence claim. Use a realistic trial before promoting initial guidance to a
validated workflow. Record the input, environment, comparator, outcome and known
limits. Keep evaluation answers out of retrieval inputs for that evaluation.

## Checks

Run the four commands listed in the [README](README.md) before committing.
The governance workflow also checks the existing manifest schema. Add meaningful
negative controls when changing a validator or fragile preservation behavior.
The vendored linter's missing-status-frontmatter warning is expected for
`SKILL.md`: the skill format uses supported metadata and a body status line.
Do not edit the shared linter to silence that warning.
