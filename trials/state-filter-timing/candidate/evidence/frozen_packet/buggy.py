import copy

def translate(rows):
    selected = [row for row in rows if row["eligible"] == 1]
    total = 10
    previous = None
    output = []
    for row in selected:
        value = row["value"]
        if value is not None:
            total += value
        output.append({"row_id": row["row_id"], "value": value,
                       "prev": previous, "total": total})
        previous = value
    return {"where_path": output, "if_path": copy.deepcopy(output)}
