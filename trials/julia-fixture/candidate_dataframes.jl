# Trial-only DataFrames.jl + CSV.jl candidate.
# Reads only the frozen fixture inputs; never loads the independent oracle.

using CSV
using DataFrames

valid_key(s) = s isa AbstractString && occursin(r"^[0-9]{4}$", s)

function run(customers_path::String, orders_path::String, out_path::String)
    ispath(out_path) && error("Destination already exists")
    customers = CSV.read(customers_path, DataFrame;
        types=Dict(:customer_id => String, :segment => String), missingstring="")
    orders = CSV.read(orders_path, DataFrame;
        types=Dict(:order_id => String, :customer_id => String,
                   :order_date => String, :amount_cents => Int64, :code => String),
        missingstring="")
    all(valid_key, customers.customer_id) || error("Invalid customer key")
    all(valid_key, orders.customer_id) || error("Invalid order customer key")
    length(unique(customers.customer_id)) == nrow(customers) || error("Duplicate customer key")
    any(ismissing, customers.segment) && error("Missing customer segment")
    any(ismissing, orders.order_id) && error("Missing order ID")
    all(x -> ismissing(x) || x isa Int64, orders.amount_cents) ||
        error("Noninteger monetary amount")

    joined = leftjoin(orders, customers; on=:customer_id,
                      validate=(false, true), matchmissing=:error, order=:left)
    labels = [ismissing(x) ? "<UNMATCHED>" : String(x) for x in joined.segment]
    grouped = groupby(DataFrame(segment=labels, amount_cents=joined.amount_cents), :segment)
    result = combine(grouped,
        nrow => :row_count,
        :amount_cents => (v -> count(x -> !ismissing(x), v)) => :non_null_amounts,
        :amount_cents => (v -> all(ismissing, v) ? missing : sum(skipmissing(v))) => :sum_cents)
    sort!(result, :segment)

    open(out_path, "w") do io
        println(io, "segment\trow_count\tnon_null_amounts\tsum_cents")
        for row in eachrow(result)
            amount_text = ismissing(row.sum_cents) ? "NULL" : string(row.sum_cents)
            println(io, row.segment, '\t', row.row_count, '\t',
                    row.non_null_amounts, '\t', amount_text)
        end
    end
    println("DataFrames candidate complete; groups=", nrow(result), "; julia=", VERSION)
end

length(ARGS) == 3 || error("Usage: candidate_dataframes.jl CUSTOMERS ORDERS OUTPUT")
run(ARGS[1], ARGS[2], ARGS[3])
