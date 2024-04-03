from pprint import pprint

from assign import assign
from concordance import comprehensive_concordance, marginal_concordance
from credibility import outranking_credibility
from discordance import marginal_discordance
from outranking import outranking_relation


def electre_tri_b(data, types, q, p, v, weights, delta, profiles):
    acreds = []
    for b in profiles:
        ca = marginal_concordance(data, b, types, q, p)
        Ca = comprehensive_concordance(ca, weights)
        da = marginal_discordance(data, b, types, p, v)
        acreds.append(outranking_credibility(Ca, da))

    bcreds = []
    for a in data:
        cb = marginal_concordance(profiles, a, types, q, p)
        Cb = comprehensive_concordance(cb, weights)
        db = marginal_discordance(profiles, a, types, p, v)
        bcreds.append(outranking_credibility(Cb, db))

    relations = []
    for b in range(len(profiles)):
        acred = acreds[b]
        bcred = [row[b] for row in bcreds]
        relations.append(outranking_relation(acred, bcred, delta))

    relations = list(map(list, zip(*relations)))  # transpose
    pprint(relations)

    assignment = assign(relations, with_lower=True)
    return assignment
