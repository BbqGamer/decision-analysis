import pytest

from concordance import comprehensive_concordance


def test_comprehensive_concordance():
    MC = [[0, 0, 0, 0], [1, 1, 1, 1], [0.5, 1, 0, 0], [1, 0.4, 1, 0]]
    W = [0.4, 0.3, 0.25, 0.05]
    res = comprehensive_concordance(marginal_concordance=MC, criteria_weights=W)
    assert [0, 1, 0.5, 0.77] == pytest.approx(res, 0.2)
