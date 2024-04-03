def outranking_credibility(concordances, marginal_discordance_matrix):
    credibilities = []
    for c, D in zip(concordances, marginal_discordance_matrix):
        credibility = 1
        for d in D:
            if d > c:
                credibility *= (1 - d) / (1 - c)
        credibilities.append(c * credibility)
    return credibilities
