GAIN = 0
COST = 1


def marginal_discordance(alternatives, boundary_profile, types, p, v):
    res = []
    for row in alternatives:
        dlist = []
        for ga, ctype, gb, pi, vi in zip(row, types, boundary_profile, p, v):
            if ctype == GAIN:
                if ga - gb <= -vi:
                    d = 1
                elif ga - gb >= -pi:
                    d = 0
                else:
                    d = ((gb - ga) - pi) / (vi - pi)
            else:
                if ga - gb >= vi:
                    d = 1
                elif ga - gb <= pi:
                    d = 0
                else:
                    d = ((ga - gb) - pi) / (vi - pi)
            dlist.append(d)
        res.append(dlist)
    return res
