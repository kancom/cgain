import cgain.restapi.api as api_pkg
import pytest
from cgain.application import OrderBook, OrderBookItem
from cgain.deps import Container


@pytest.fixture
def dep_container():
    container = Container()
    container.wire(packages=[api_pkg])
    yield container

@pytest.fixture
def pair():
    return "BTC/USDT"
    
@pytest.fixture
def static_obook(pair):
    return OrderBook(pair=pair,
                     asks=[
                         OrderBookItem(price=110, volume=10),
                         OrderBookItem(price=112, volume=8),
                         OrderBookItem(price=114, volume=18),
                         OrderBookItem(price=116, volume=10),
                     ],
                     bids=[
                         OrderBookItem(price=108, volume=10),
                         OrderBookItem(price=106, volume=8),
                         OrderBookItem(price=104, volume=18),
                         OrderBookItem(price=102, volume=10),
                     ])
