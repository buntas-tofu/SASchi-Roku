# 0006: First bounded Julia runtime trial

Status: engineering implementation of the principal's 2026-11-04 direction to proceed with evaluation, proposed for maintainer review. Not a merge authorization or Julia-equivalence certification.

Freeze the existing synthetic eight-order fixture by blob identity. Do not edit expected.json, recalculate truth from the candidate, or copy the inputs into a new reference collection. Use a Base Julia implementation and a separate DataFrames/CSV candidate. An independent Python comparator must verify exact grouped results and reject incorrect result mutations. The Julia candidates must reject duplicate parent keys and malformed string identifiers without writing output.

Use isolated hosted Julia 1.10.13 LTS, exact direct package constraints and saved resolved Manifest, rather than modify the managed enterprise runtime. Add a dedicated narrowly scoped trial workflow with read-only repo access and pinned actions; leave the original governance checks unchanged. No source SAS interpreter or SAS-to-Julia correctness is implied.

Preserve original failures and repair attempts separately if execution detects a defect. Keep the repository's unresolved original-software licensing decision separate from this evaluation artifact, which is not a standalone package release.
