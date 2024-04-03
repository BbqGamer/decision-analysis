from assign import assign

RELATION_MATRIX1 = [
    [">", "|"],
    ["?", "<"],
    [">", ">"],
    [">", "<"],
    ["<", "<"],
    ["|", "<"],
    ["?", "<"],
]


def test_assign_pessimistic():
    res = assign(RELATION_MATRIX1)
    assert res == [3, 1, 3, 2, 1, 2, 1]


def test_assign_optimistic():
    res = assign(RELATION_MATRIX1, optimistic=True)
    assert res == [3, 2, 3, 2, 1, 2, 2]
