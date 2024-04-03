import pytest

from discordance import marginal_discordance


def test_marginal_concordance():
    A = [[90, 5], [40, 15], [70, 10]]
    b = [86, 0]
    types = [0, 1]
    P = [7, 5]
    V = [20, 15]
    expected = [[0, 0], [1, 1], [0.69, 0.5]]
    res = marginal_discordance(A, b, types, P, V)
    assert pytest.approx(res[0]) == expected[0]
    assert res[1] == expected[1]
