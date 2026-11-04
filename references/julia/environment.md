# Approved Julia runtime discovery

Status: read-only operator guidance, not evidence of an installed enterprise Julia runtime.

Only if Julia is already authorized and installed, use the approved executable for:

```sh
julia --version
julia --startup-file=no -e 'using Pkg; println(VERSION); Pkg.status()'
```

The second command inspects package state. Do not run `Pkg.add`, `Pkg.update` or `Pkg.instantiate` without authorization. Such actions can change the environment or access external registries.

Capture the Julia version, OS and architecture, active `Project.toml`, available `Manifest.toml`, their hashes, package versions, registry/depot policy, exact command, output hashes and all skipped or failed cases. Project records declared dependencies; Manifest records resolved versions.

Official upstream releases on 2026-11-04: stable 1.13.3, LTS 1.10.13. They do not imply what is available in a managed client. Missing Julia or a missing package is **not executed**, not passing.
