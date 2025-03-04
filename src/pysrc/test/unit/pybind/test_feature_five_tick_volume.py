import pytest
from pysrc import intern


def test_feature_five_tick_volume() -> None:
    vf = intern.FiveTickVolumeFeature()
    assert vf.compute_feature([(2, 1, False)]) == 1.0
    assert vf.compute_feature([(1, 1, False)]) == 2.0
    assert vf.compute_feature([(1, 1, False), (1, 1, True)]) == 4.0
    assert vf.compute_feature([(1, 1, False), (1, 1, True)]) == 6.0
    assert vf.compute_feature([(2, 1, False), (1, 1, True)]) == 8.0
    assert vf.compute_feature([(1, 1, False), (1, 1, True)]) == 9.0
    assert vf.compute_feature([(2, 1, False), (1, 1, True)]) == 10.0
