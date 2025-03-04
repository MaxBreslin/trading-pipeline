import pytest
from pysrc import intern


def test_target_return_1s() -> None:
    r1 = intern.ReturnOneS()
    assert r1.compute_target([]) == 0.0
    assert r1.compute_target([(2, 1, False)]) == 0.0
    assert r1.compute_target([(1, 1, False)]) == -1.0
    assert r1.compute_target([(3, 2, False), (1, 1, True)]) == 1.0
    assert r1.compute_target([(2, 5, False), (2, 1, True)]) == 0.0
    assert r1.compute_target([(2, 1, False), (1, 1, True)]) == -0.5
    assert r1.compute_target([(1, 1, False), (1, 1, True)]) == -0.5
    assert r1.compute_target([]) == 0.0
