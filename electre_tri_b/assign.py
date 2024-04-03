def assign(relation_matrix, optimistic=False, with_lower=False):
    """Assign class to each alternative, given a matrix of relations of each
    alternative to each class boundary profile. Given by >, <, | and ?
    if optimistic is set to True uses optimistic assignment otherwise pessimistic
    if with_lower is set the first column is lower boundary profile of first class
    """
    assign_func = assign_optimistic if optimistic else assign_pessimistic
    res = list(map(assign_func, relation_matrix))
    if with_lower:
        res = [x - 1 for x in res]
    return res


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
