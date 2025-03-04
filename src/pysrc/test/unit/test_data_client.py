from pysrc.data_handlers.data_client import DataClient
from pysrc.utils.trade_types import Trade, BUY, SELL

import pytest
from unittest.mock import MagicMock, patch


def test_parse_message() -> None:
    message = [
        {
            "timestamp": 1234567890,
            "timestampms": 1234567890123,
            "tid": 1234567890123456,
            "price": "10000.00",
            "amount": "100.000",
            "exchange": "gemini",
            "type": "sell",
        },
        {
            "timestamp": 2345678901,
            "timestampms": 2345678901234,
            "tid": 2345678901234567,
            "price": "10000.50",
            "amount": "100.005",
            "exchange": "gemini",
            "type": "buy",
        },
        {
            "timestamp": 3456789012,
            "timestampms": 3456789012345,
            "tid": 3456789012345678,
            "price": "10001.50",
            "amount": "101.055",
            "exchange": "gemini",
            "type": "buy",
        },
    ]
    expected_trades = [
        Trade(
            price=float("10000.00"),
            volume=float("100.000"),
            side=SELL,
        ),
        Trade(
            price=float("10000.50"),
            volume=float("100.005"),
            side=BUY,
        ),
        Trade(
            price=float("10001.50"),
            volume=float("101.055"),
            side=BUY,
        ),
    ]

    dc = DataClient()
    trades = dc._parse_message(message)
    assert trades == expected_trades


@patch("pysrc.data_handlers.data_client.requests.get")
def test_get_data(mock_get: MagicMock) -> None:
    query_data = [
        {
            "timestamp": 1234567890,
            "timestampms": 1234567890123,
            "tid": 1234567890123456,
            "price": "10000.00",
            "amount": "100.000",
            "exchange": "gemini",
            "type": "sell",
        },
        {
            "timestamp": 2345678901,
            "timestampms": 2345678901234,
            "tid": 2345678901234567,
            "price": "10000.50",
            "amount": "100.005",
            "exchange": "gemini",
            "type": "buy",
        },
        {
            "timestamp": 3456789012,
            "timestampms": 3456789012345,
            "tid": 3456789012345678,
            "price": "10001.50",
            "amount": "101.055",
            "exchange": "gemini",
            "type": "buy",
        },
    ]
    mock_response = MagicMock()
    mock_response.json.return_value = query_data
    mock_get.return_value = mock_response
    expected_data = [
        Trade(
            price=float("10000.00"),
            volume=float("100.000"),
            side=SELL,
        ),
        Trade(
            price=float("10000.50"),
            volume=float("100.005"),
            side=BUY,
        ),
        Trade(
            price=float("10001.50"),
            volume=float("101.055"),
            side=BUY,
        ),
    ]

    dc = DataClient(
        base_url="https://api.gemini.com/v1",
        query="/trades/btcusd",
        timestamp=None,
        since_tid=0,
        limit_trades=3,
    )
    data = dc.get_data()

    mock_get.assert_called_once_with(
        "https://api.gemini.com/v1/trades/btcusd",
        params={"since_tid": 0, "limit_trades": 3},
    )
    assert data == expected_data
