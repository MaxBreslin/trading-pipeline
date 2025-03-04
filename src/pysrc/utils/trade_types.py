from typing import NamedTuple

SELL = False
BUY = True


class Trade(NamedTuple):
    price: float
    volume: float
    side: bool
