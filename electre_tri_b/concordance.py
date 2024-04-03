def comprehensive_concordance(marginal_concordance, criteria_weights):
    return [
        sum(w * g for (w, g) in zip(criteria_weights, row)) / sum(criteria_weights)
        for row in marginal_concordance
    ]
