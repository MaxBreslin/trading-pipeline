import numpy as np
from numpy.typing import ArrayLike


class CircularBuffer:
    def __init__(self, capacity: int, item_size: int = 1) -> None:
        self.capacity = capacity
        self.item_size = item_size
        self.buffer = (
            np.empty((self.capacity, item_size), dtype=float)
            if item_size > 1
            else np.empty((self.capacity,), dtype=float)
        )
        self.index = 0
        self.size = 0

    def push(self, item: ArrayLike) -> None:
        item = np.asarray(item)
        try:
            assert item.size == self.item_size
        except AssertionError:
            raise ValueError(
                f"Item has size {item.size} but should have size {self.item_size}"
            )

        self.buffer[self.index] = item
        self.index = (self.index + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def get_buffer(self) -> np.ndarray:
        if self.size < self.capacity:
            return self.buffer[: self.size].copy()
        return np.concat((self.buffer[self.index :], self.buffer[: self.index]))

    def __len__(self) -> int:
        return self.size

    def __array__(self) -> np.ndarray:
        return self.get_buffer()
