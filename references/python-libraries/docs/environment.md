# Approved Python runtime inventory

Status: read-only operator guidance, not a record of installed versions.

The user reports Faker is available in the managed enterprise client. This does not establish NumPy, Polars, or DuckDB availability. Use only the approved Python invocation:

```sh
python --version
python -m pip show Faker numpy polars duckdb
```

`pip show` reads metadata, it does not install. Use the managed inventory if it is the official version source. Do not install/upgrade packages, switch channels, use external extensions or contact remote services.

Log interpreter, package versions, command, input hashes, schema, seed/locale if applicable, expected result, observed result and all skipped checks. Missing packages must be labeled **not executed**, never passed.
