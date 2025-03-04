from pysrc.utils.trade_types import Trade

import requests
import logging
from typing import Optional


class DataClient:
    def __init__(
        self,
        base_url: str = "https://api.gemini.com/v1",
        query: str = "/trades/btcusd",
        timestamp: Optional[int] = None,
        since_tid: Optional[int] = None,
        limit_trades: int = 50,
        with_timestamp: Optional[int] = None,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        self.base_url = base_url
        self.query = query
        self.timestamp = timestamp
        self.since_tid = since_tid
        self.limit_trades = limit_trades
        self.with_timestamp = with_timestamp

    def _query_api(self) -> list[dict]:
        params = {"limit_trades": self.limit_trades}
        if self.since_tid is not None:
            params["since_tid"] = self.since_tid
        elif self.timestamp is not None:
            params["timestamp"] = self.timestamp
        try:
            response = requests.get(self.base_url + self.query, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error("Request exception occurred: %s", e, exc_info=True)
            raise

        data: list[dict] = response.json()

        return data

    def _parse_message(self, message: list[dict]) -> list[Trade]:
        if not isinstance(message, list):
            self.logger.error(
                "Unexpected message format: expected list, got %s",
                type(message).__name__,
            )
            raise ValueError(
                f"Message is unusual. Was the request valid? Here is message: {message}"
            )

        trades: list[Trade] = []
        for item in message:
            if not isinstance(item, dict):
                self.logger.error("Trade is not a dict: %s", type(item).__name__)
                raise ValueError("Expected trade to be a dict")

            if self.with_timestamp and item["timestamp"] != self.with_timestamp:
                continue

            trade = Trade(
                price=float(item["price"]),
                volume=float(item["amount"]),
                side=item["type"] == "buy",
            )
            trades.append(trade)

        return trades

    def get_data(self) -> list[Trade]:
        message = self._query_api()
        trades = self._parse_message(message)
        return trades
