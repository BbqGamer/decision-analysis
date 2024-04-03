def assign(relation_matrix, optimistic=False):
    assign_func = assign_optimistic if optimistic else assign_pessimistic
    return list(map(assign_func, relation_matrix))


def assign_pessimistic(row):
    for i, e in enumerate(reversed([">"] + row)):
        if e in [">", "|"]:
            break
    return len(row) + 1 - i


def assign_optimistic(row):
    for i, e in enumerate(row + ["<"]):
        if e == "<":
            break
    return i + 1
