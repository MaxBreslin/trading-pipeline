from pysrc.utils.circular_buffer import CircularBuffer

import pytest
import numpy as np


def test_push() -> None:
    cb = CircularBuffer(3)
    assert np.array_equal(cb.get_buffer(), np.array([]))
    assert len(cb) == 0

    cb.push(1.0)
    cb.push(2.0)
    assert np.array_equal(cb.get_buffer(), np.array([1.0, 2.0]))
    assert len(cb) == 2
    with pytest.raises(ValueError):
        cb.push([3.0, 4.0])

    cb.push(3.0)
    cb.push(4.0)
    assert np.array_equal(cb.get_buffer(), np.array([2.0, 3.0, 4.0]))
    assert len(cb) == 3

    cb = CircularBuffer(3, 2)
    assert np.array_equal(cb.get_buffer(), np.array([]).reshape((0, 2)))
    assert len(cb) == 0

    cb.push([1.0, 2.0])
    cb.push([3.0, 4.0])
    assert np.array_equal(cb.get_buffer(), np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert len(cb) == 2
    with pytest.raises(ValueError):
        cb.push([5.0, 6.0, 7.0])
    with pytest.raises(ValueError):
        cb.push(5.0)

    cb.push([5.0, 6.0])
    cb.push([7.0, 8.0])
    assert np.array_equal(
        cb.get_buffer(), np.array([[3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    )
    assert len(cb) == 3
