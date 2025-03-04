import pytest
from pysrc import intern


def test_feature_pct_buy_trades() -> None:
    ptf = intern.PercentBuyFeature()
    assert ptf.compute_feature([(1, 1, False)]) == 0.0
    assert ptf.compute_feature([(1, 1, False), (1, 1, True)]) == 0.5
    assert ptf.compute_feature([(1, 1, True)]) == 1.0
    assert (
        abs(
            ptf.compute_feature(
                [
                    (1, 1, False),
                    (1, 1, True),
                    (1, 1, False),
                    (1, 1, False),
                    (1, 1, True),
                ]
            )
            - 0.4
        )
        < 1e-5
    )
