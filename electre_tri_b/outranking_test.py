from outranking import outranking_relation


def test_outranking_relation():
    acred = [0.95, 0, 1, 0.75, 0.5, 0.75, 0.75, 0]
    bcred = [0, 0, 0, 0.09, 1, 0.65, 0, 0.6]
    credibility_threshold = 0.65  # delta
    res = outranking_relation(acred, bcred, delta=credibility_threshold)
    exp = [">", "?", ">", ">", "<", "|", ">", "?"]
    assert res == exp
