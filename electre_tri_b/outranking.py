def outranking_relation(acred, bcred, delta):
    func = lambda a: a >= delta
    acred = map(func, acred)
    bcred = map(func, bcred)
    res = []
    for a, b in zip(acred, bcred):
        if a and not b:
            res.append(">")
        elif not a and b:
            res.append("<")
        elif a and b:
            res.append("|")
        else:
            res.append("?")
    return res
