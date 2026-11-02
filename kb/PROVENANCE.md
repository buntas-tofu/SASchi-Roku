# Collection provenance

Status: migration record, not a new semantic validation result.

These authored collections were extracted from the originating Bedrock workspace
at commit 49e2f7626eb4d0b41ced06ae241567304eb44b12. The macro collection originated
in commit 44060bb5faafa372df09b48be8b69ac2caa78a1e; the LLM and SAS expansion
originated in commit 49e2f7626eb4d0b41ced06ae241567304eb44b12. Those original
commits remain in that repository's history.

Only the selected corpora and public research were imported. Internal review
notes, environment captures, repository history, deployment configuration, and
unrelated content were not imported. This avoids publishing the originating
workspace's private history with its public teaching material.

The teaching cards and research files are byte-preserved at import. Collection
README files were adapted to the new ownership and consumer boundary.
IMPORT_MANIFEST.json records both the original and imported hashes, making those
changes explicit. It is a historical receipt, not a requirement that content
never evolve. Future changes belong in this repository's own Git history.

The collection dates and evidence labels retain their original meaning. Moving
files does not promote documentation to a passing test. Source URLs are scoped
references, not archived copies of third-party publications.
