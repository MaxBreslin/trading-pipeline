from pysrc.prediction.lasso_model_predictor import LassoModelPredictor
from pysrc.utils.trade_types import Trade, BUY, SELL

import pytest
import numpy as np


def test_update_features() -> None:
    lmp = LassoModelPredictor()

    data = [Trade(1, 1, BUY), Trade(1, 1, SELL)]
    lmp.features.push(lmp._compute_features(data))
    assert np.array_equal(lmp.features.get_buffer(), np.array([[2.0, 0.5, 0.5, 2.0]]))

    data = [Trade(1, 1, SELL), Trade(1, 2, SELL), Trade(1, 1, SELL), Trade(1, 1, BUY)]
    lmp.features.push(lmp._compute_features(data))
    assert np.array_equal(
        lmp.features.get_buffer(),
        np.array([[2.0, 0.5, 0.5, 2.0], [4.0, 0.25, 0.75, 7.0]]),
    )

    data = [Trade(1, 1, SELL)]
    for _ in range(9):
        lmp.features.push(lmp._compute_features(data))
    assert np.array_equal(
        lmp.features.get_buffer(),
        np.array(
            [
                [4.0, 0.25, 0.75, 7.0],
                [1.0, 0.0, 1.0, 8.0],
                [1.0, 0.0, 1.0, 9.0],
                [1.0, 0.0, 1.0, 10.0],
                [1.0, 0.0, 1.0, 9.0],
                [1.0, 0.0, 1.0, 5.0],
                [1.0, 0.0, 1.0, 5.0],
                [1.0, 0.0, 1.0, 5.0],
                [1.0, 0.0, 1.0, 5.0],
                [1.0, 0.0, 1.0, 5.0],
            ]
        ),
    )


def test_update_targets() -> None:
    lmp = LassoModelPredictor()

    data = [Trade(1, 1, BUY), Trade(1, 1, SELL)]
    lmp.targets.push(lmp._compute_target(data))
    assert np.array_equal(lmp.targets.get_buffer(), np.array([0.0]))

    data = [Trade(3, 1, SELL), Trade(2, 1, SELL), Trade(4, 1, SELL)]
    lmp.targets.push(lmp._compute_target(data))
    assert np.array_equal(
        lmp.targets.get_buffer(),
        np.array([0.0, 2.0]),
    )

    data = [Trade(1, 1, SELL)]
    for _ in range(9):
        lmp.targets.push(lmp._compute_target(data))
    assert np.array_equal(
        lmp.targets.get_buffer(),
        np.array([2.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    )


def test_on_tick() -> None:
    lmp = LassoModelPredictor()

    data = [Trade(1, 1, BUY), Trade(1, 1, SELL)]
    prediction = lmp.on_tick(data)
    assert len(lmp.features) == len(lmp.targets) == 1
    assert prediction is None

    data = [Trade(3, 1, SELL), Trade(2, 1, SELL), Trade(4, 1, SELL), Trade(1, 1, BUY)]
    prediction = lmp.on_tick(data)
    assert len(lmp.features) == len(lmp.targets) == 2
    assert prediction is None

    data = [Trade(1, 1, SELL)]
    for _ in range(8):
        prediction = lmp.on_tick(data)
        assert prediction is None

    data = [Trade(1, 1, BUY), Trade(1, 1, SELL)]
    prediction = lmp.on_tick(data)
    assert len(lmp.features) == len(lmp.targets) == 10
    assert prediction is not None
