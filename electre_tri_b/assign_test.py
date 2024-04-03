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

ASSIGNMENT1P = [3, 1, 3, 2, 1, 2, 1]
ASSIGNMENT1O = [3, 2, 3, 2, 1, 2, 2]


def test_assign_pessimistic():
    res = assign(RELATION_MATRIX1)
    assert res == ASSIGNMENT1P


def test_assign_optimistic():
    res = assign(RELATION_MATRIX1, optimistic=True)
    assert res == ASSIGNMENT1O


RELATION_MATRIX2 = [
    [">", ">", ">", "<", "<", "<", "<"],
    [">", ">", "<", "<", "<", "<", "<"],
    [">", ">", ">", "|", "<", "<", "<"],
    [">", ">", "|", "|", "|", "<", "<"],
    ["|", "<", "<", "<", "<", "<", "<"],
    [">", ">", ">", ">", ">", "?", "<"],
    [">", ">", "?", "?", "<", "<", "<"],
    [">", "?", "?", "?", "?", "<", "<"],
]

ASSIGNMENT2P = [3, 2, 4, 5, 1, 5, 2, 1]
ASSIGNMENT2O = [3, 2, 4, 5, 1, 6, 4, 5]


def test_assign_pessimistic2_with_lower():
    res = assign(RELATION_MATRIX2, with_lower=True)
    assert res == ASSIGNMENT2P


def test_assign_optimistic2_with_lower():
    res = assign(RELATION_MATRIX2, optimistic=True, with_lower=True)
    assert res == ASSIGNMENT2O
