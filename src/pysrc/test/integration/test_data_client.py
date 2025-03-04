from pysrc.data_handlers.data_client import DataClient

import pytest
import time
from requests.exceptions import HTTPError


def test_get_data() -> None:
    dc = DataClient()
    data = dc.get_data()
    assert len(data) == dc.limit_trades

    dc = DataClient(limit_trades=3)
    data = dc.get_data()
    assert len(data) == 3

    dc = DataClient(since_tid=9999999999999999)
    data = dc.get_data()
    assert len(data) == 0

    dc = DataClient(timestamp=9999999999999999)
    data = dc.get_data()
    assert len(data) == 0

    dc = DataClient(timestamp=1)
    with pytest.raises(HTTPError):
        dc.get_data()
