# Julia language semantics

Status: curated candidate reference. Sources JL-001 through JL-005.

Julia uses typed values, multiple dispatch, 1-indexed arrays, explicit loops and broadcasting. Explicit procedural state is possible, but a vector shift does not automatically reproduce a SAS LAG queue.

- `missing` is a singleton statistical missing value; `nothing` denotes a different absence concept, while `NaN` is a numeric floating value.
- Ordinary arithmetic with `missing` often propagates it. `sum(skipmissing(v))` deliberately drops missing values; that can accidentally turn an all-missing group into zero. Require a nonmissing-count guard when the oracle expects missing.
- Ordinary comparison with `missing` may itself yield `missing`. Use `ismissing`, `isequal`, or another explicit policy for predicates.
- Julia `Date` and `DateTime` are not SAS numeric day/second values. `Date(1960,1,1) + Day(n)` is a candidate for ordinary SAS day count; it does not cover all formats, timezone, missing or interval-alignment rules.
- Julia `length(s)` and `ncodeunits(s)` measure different aspects of Unicode strings. SAS declared widths, padding and truncation require physical-byte tests.
- `Statistics.std` defaults to corrected sample standard deviation; statistical SAS procedure outputs require independently specified estimators, sample definitions, grouping and weights.

Illustrative Julia syntax only, not a recorded execution:

```julia
values = Union{Missing, Int64}[1250, 2300, missing, -400, 0, 500, 700, missing]
total = sum(skipmissing(values))
@assert total == 4350
```

The separate [SAS-to-Julia guide](../../docs/targets/sas-to-julia.md) defines source-specific hazards. The [source register](SOURCES.json) links documented language behavior.
