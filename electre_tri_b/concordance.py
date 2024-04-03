GAIN = 0
COST = 1


def marginal_concordance(alternatives, boundary_profile, types, q, p):
    res = []
    for row in alternatives:
        clist = []
        for ga, ctype, gb, qi, pi in zip(row, types, boundary_profile, q, p):
            if ctype == GAIN:
                if ga - gb >= -qi:
                    c = 1
                elif ga - gb < -pi:
                    c = 0
                else:
                    c = (pi - (gb - ga)) / (pi - qi)
            else:
                if ga - gb <= qi:
                    c = 1
                elif ga - gb > pi:
                    c = 0
                else:
                    c = (pi - (ga - gb)) / (pi - qi)
            clist.append(c)
        res.append(clist)
    return res


def comprehensive_concordance(marginal_concordance, criteria_weights):
    return [
        sum(w * g for (w, g) in zip(criteria_weights, row)) / sum(criteria_weights)
        for row in marginal_concordance
    ]
