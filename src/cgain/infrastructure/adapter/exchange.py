import ccxt
from cgain.application import CurrencyPair, Exchange, OrderBook
from cgain.application.domain.entities import OrderBookItem


class BinanceExchange(Exchange):
    TIMEOUT = 10_000

    def __init__(self, api_key: str, secret_key: str) -> None:
        self._api_key = api_key
        self._secret_key = secret_key
        self._ccxt_config = {
            "apiKey": self._api_key,
            "secret": self._secret_key,
            "timeout": self.TIMEOUT,
            "enableRateLimit": True,
        }
        self._exchange = ccxt.binance(self._ccxt_config)
        assert self._exchange is not None, "Failed to initialize Binance"

        self._get_orderbook_supported = False
        if self._exchange.has.get("fetchOrderBook"):
            self._get_orderbook_supported = True

    def get_orderbook(self, pair: CurrencyPair) -> OrderBook:
        if self._exchange is None:
            raise EnvironmentError("not initialized")

        status = self._exchange.fetch_status()
        if status is None or status.get("status") != "ok":
            raise EnvironmentError("Exchange is not ready")

        if not self._get_orderbook_supported:
            raise EnvironmentError("fetch orderbook is not supported")
        orderbook = self._exchange.fetch_order_book(symbol=pair)
        assert orderbook is not None, "Failed to fetch orderbook"

        return OrderBook(
            pair=orderbook["symbol"],
            bids=[OrderBookItem(price=i[0], volume=i[1]) for i in orderbook["bids"]],
            asks=[OrderBookItem(price=i[0], volume=i[1]) for i in orderbook["asks"]],
        )
