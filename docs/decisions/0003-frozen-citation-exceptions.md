# 0003: Preserve two frozen citations with exact content exceptions

Status: engineering implementation of the principal's 2026-11-02 instruction to
complete the proposed PR 5 governance resolution and continue interchange trials.
Maintainers may review this bounded exception. It is not permission to disclose
new private material or to change evaluated inputs.

The preceding plan identified two choices: a narrowly documented exception for
historical citations, or fresh evaluations using sanitized inputs. The principal
approved proceeding. The exact implementation here is an engineering choice:
preserve the already published, frozen merge and widths packets, whose receipts
would be invalidated by editing their citation links.

Each exception names one complete path and one token pattern, and includes the
SHA-256 of the exact historical file. The sanitization gate verifies that hash
before accepting the exception. A changed byte, a copied file at another path,
or a different forbidden token is still rejected. Existing declarations retain
their previous behavior; no new directory exemption is introduced.

Tests exercise acceptance of both exact files and rejection after byte changes,
relocation, and introduction of another forbidden token. Trial inputs, candidates,
expected results and receipts remain byte-identical. The existing starter-packet
declaration and its previously pending broader ruling are outside this decision.

New evaluation packets use current sanitized skill references. No historical
receipt will be rewritten to represent those new inputs as the original trial.
