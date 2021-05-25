from typing import List

from cgain.application.domain.value_objects import CurrencyPair, Price, Volume
from pydantic import BaseModel


class OrderBookItem(BaseModel):
    price: Price
    volume: Volume


class OrderBook(BaseModel):
    pair: CurrencyPair
    bids: List[OrderBookItem]
    asks: List[OrderBookItem]

    @property
    def best_bid(self) -> OrderBookItem:
        return self.bids[0]

    @property
    def best_ask(self) -> OrderBookItem:
        return self.asks[0]
