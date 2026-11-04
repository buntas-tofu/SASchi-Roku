# Trial-only Base Julia implementation; CSV parser supports only this frozen,
# simple comma-delimited fixture. It rejects quoted/complex records.
# This candidate never reads the frozen expected.json oracle.

function read_simple_csv(path::String, expected_header::Vector{String})
    isfile(path) || error("Input does not exist: " * path)
    lines = readlines(path)
    !isempty(lines) || error("Empty input")
    first = split(lines[1], ','; keepempty=true)
    first == expected_header || error("Unexpected schema")
    records = Vector{Vector{String}}()
    for line in lines[2:end]
        occursin('"', line) && error("Quoted CSV outside bounded parser")
        fields = String.(split(line, ','; keepempty=true))
        length(fields) == length(expected_header) || error("Invalid field count")
        push!(records, fields)
    end
    return records
end

valid_key(s::AbstractString) = occursin(r"^[0-9]{4}$", s)

function run(customers_path::String, orders_path::String, out_path::String)
    ispath(out_path) && error("Destination already exists")
    cs = read_simple_csv(customers_path, ["customer_id", "segment"])
    os = read_simple_csv(orders_path, ["order_id", "customer_id", "order_date", "amount_cents", "code"])
    lookup = Dict{String, String}()
    for c in cs
        key, segment = c
        valid_key(key) || error("Invalid customer key")
        haskey(lookup, key) && error("Duplicate customer key")
        isempty(segment) && error("Missing customer segment")
        lookup[key] = segment
    end
    grouped = Dict{String, NTuple{3, Int64}}()
    for o in os
        oid, customer_key, day, amount_raw, code = o
        valid_key(customer_key) || error("Invalid order customer key")
        isempty(oid) && error("Missing order ID")
        amount = isempty(amount_raw) ? missing : parse(Int64, amount_raw)
        segment = get(lookup, customer_key, "<UNMATCHED>")
        row_count, non_null, total = get(grouped, segment, (Int64(0), Int64(0), Int64(0)))
        if ismissing(amount)
            grouped[segment] = (row_count + 1, non_null, total)
        else
            grouped[segment] = (row_count + 1, non_null + 1, Base.checked_add(total, amount))
        end
    end
    open(out_path, "w") do io
        println(io, "segment\trow_count\tnon_null_amounts\tsum_cents")
        for group in sort(collect(keys(grouped)))
            n, present, value = grouped[group]
            print(io, group, '\t', n, '\t', present, '\t')
            println(io, present == 0 ? "NULL" : string(value))
        end
    end
    println("Base Julia candidate complete; groups=", length(grouped), "; julia=", VERSION)
end

length(ARGS) == 3 || error("Usage: candidate_base.jl CUSTOMERS ORDERS OUTPUT")
run(ARGS[1], ARGS[2], ARGS[3])
