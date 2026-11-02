# mcp/ : the SASchi-Roku knowledge and skills MCP

Status: active. Phase 1 of the design (branch `design/conversion-reference`),
built 2026-11-02 under operator rulings Q1 (stdio first, transport flag
ready) and Q5 (distribution `sas-ref-mcp`, import package `sas_ref`).

A FastMCP stdio server over the kb/ knowledge base: the rulebook, the
capability manifest, the semantics mirror, the Rosetta corpus, the landmine
cards, the conversion guides, the census, and the synced evidence docs. Twelve
tools, nine resources, three workflow prompts. Advisory by doctrine: the
server explains, drafts, and interprets; acceptance belongs to the gates in
the campaign lane.

## Run

From a repository checkout, no install:

```
PYTHONPATH=mcp SAS_REF_KB=kb python3 -m sas_ref.mcp.server
```

Installed (the export shape):

```
pip install ./mcp            # or from a git URL, see below
sas-ref-mcp                  # stdio
sas-ref-mcp --transport http --port 8765   # flag-ready, not hosted
```

The repository root carries `.mcp.json` for clients that read it.

## Environment

- `SAS_REF_KB`: direct path to a kb/ directory (first precedence).
- `SAS_REF_ROOT`: path to a repository root containing kb/.
- Neither set: the server discovers the root by walking up from the working
  directory, then from the installed package location.

That resolution order is the exportability contract: the same server runs
from a checkout, from an install, and from the sister repository, with no
private state and no hardcoded paths.

## Export

```
pip install "git+<repo-url>#subdirectory=mcp"
```

The sister repository (public lane) installs identically; the only per-copy
differences are the sync pointer behind kb/ and the tree's allowed identity,
exactly as the design's section 8 requires.

## Verify

```
python3 -m sas_ref.mcp.selftest
```

Direct asserts over the real kb/ plus a protocol pass through an in-memory
client (tools/list, real calls, a resource read, a prompt fetch). The
governance workflow runs it on every push.
