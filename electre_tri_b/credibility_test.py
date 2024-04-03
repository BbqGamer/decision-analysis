import pytest

from credibility import outranking_credibility


def test_outranking_credibility():
    C = [0.5, 0.65, 0.0, 0.25, 1.0, 0.65, 0.65, 0.6]
    D = [[1, 1], [0, 1], [1, 1], [0.57, 0.52], [0, 0], [0, 0.31], [0, 1], [0, 0]]
    exp = [0, 0, 0, 0.09, 1, 0.65, 0, 0.6]
    res = outranking_credibility(C, D)
    assert exp == pytest.approx(res, 0.02)
