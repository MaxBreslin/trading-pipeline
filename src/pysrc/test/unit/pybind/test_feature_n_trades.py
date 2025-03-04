import pytest
from pysrc import intern


def test_feature_n_trades() -> None:
    ntf = intern.NTradesFeature()
    assert ntf.compute_feature([(1.0, 1.0, False)]) == 1.0
    assert ntf.compute_feature([(1, 1, False)]) == 1.0
    assert ntf.compute_feature([(2, 1, False), (2, 2, True)]) == 2.0
