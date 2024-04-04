def srf(groups, cards, Z):
    """
    Calculates weights for criteria using SRF (Simos-Roy-Figueira) procedure,
    aka the method of cards. Takes list of groups of indices of criteria in the order
    of increasing importance (example [[1], [0,2], [4]] if criteria 1 is less important
    than 0,2 and 4 but 0, 2 are on the same level).
    Cards which contain the list of numbers of cards between each group ([1,0])
    Z is ratio between performance of the best and the worst group
    """

    R = dict()

    cards = [0] + cards
    C = 0
    for i, G in enumerate(groups):
        C += cards[i]
        rank = i + 1 + C
        for g in G:
            R[g] = rank

    max_rank = max(R.values())
    for i in range(len(R)):
        R[i] = 1 + (Z - 1) * ((R[i] - 1) / (max_rank - 1))

    sumed = sum(R.values())
    res = [v / sumed for _, v in sorted(R.items(), key=lambda a: a[0])]
    return res
