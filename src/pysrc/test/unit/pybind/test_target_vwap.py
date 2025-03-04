import pytest
from pysrc import intern


def test_target_vwap() -> None:
    vf = intern.VWAPTarget()
    assert vf.compute_target([]) == 0.0
    assert vf.compute_target([(2, 1, False)]) == 2.0
    assert vf.compute_target([(1, 1, False)]) == 3.0 / 2
    assert vf.compute_target([(3, 2, False), (1, 1, True)]) == 2
    assert abs(vf.compute_target([(1, 5, False), (2, 1, True)]) - 17.0 / 11) < 1e-5
    assert abs(vf.compute_target([(2, 1, False), (1, 1, True)]) - 20.0 / 13) < 1e-5
    assert abs(vf.compute_target([(1, 1, False), (1, 1, True)]) - 10.0 / 7) < 1e-5
    assert abs(vf.compute_target([]) - 19.0 / 13) < 1e-5
