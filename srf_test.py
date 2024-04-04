import pytest

from srf import srf

CARD = -1


def test_srf():
    groups = [[3], [2], [1], [0]]
    cards = [3, 0, 1]
    exp = [0.4, 0.3, 0.25, 0.05]
    Z = 8
    assert srf(groups, cards, Z) == exp


def test_srf2():
    groups = [[0], [5, 7], [4], [1, 2, 6], [3]]
    cards = [2, 0, 3, 1]
    Z = 10
    res = srf(groups, cards, Z)
    exp = [0.021, 0.172, 0.172, 0.210, 0.096, 0.077, 0.172, 0.077]
    assert pytest.approx(res, 0.01) == exp
