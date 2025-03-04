import pytest
from pysrc import intern


def test_feature_pct_sell_trades() -> None:
    psf = intern.PercentSellFeature()
    assert psf.compute_feature([(1, 1, False)]) == 1.0
    assert psf.compute_feature([(1, 1, False), (1, 1, True)]) == 0.5
    assert psf.compute_feature([(1, 1, True)]) == 0.0
    assert (
        abs(psf.compute_feature([(1, 1, False), (1, 1, True), (1, 1, False)]) - 0.67)
        < 1e-2
    )
