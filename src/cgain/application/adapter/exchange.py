import abc

from ..domain.entities import OrderBook
from ..domain.value_objects import CurrencyPair, Price


class Exchange(metaclass=abc.ABCMeta):
    """Describes exchange interface"""

    @abc.abstractmethod
    def get_orderbook(self, pair: CurrencyPair) -> OrderBook:
        """gets orderbook snapshot for a currency pair"""
        pass
