import cgain.restapi.api_main as api
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(api.api_router)

client = TestClient(app)


@pytest.mark.parametrize(
    "side,amount,resp_amount",
    [
        ("BUY", 1, 110),
        ("BUY", 12, 110 * 10 + 112 * 2),
        ("SELL", 10.0, 108 * 10),
        ("SELL", 19, 108 * 10 + 106 * 8 + 104 * 1),
    ],
)
def test_spendings(
    side, amount, resp_amount, mocker, dep_container, static_obook, pair
):
    orderbook = mocker.MagicMock()
    orderbook.get_orderbook.return_value = static_obook
    with dep_container.exchange.override(orderbook):
        params = {"side": side, "amount": amount, "pair": pair}
        response = client.get("/info/spendings", params=params)
        assert response.status_code == 200
        assert response.json()["amount"] == resp_amount


@pytest.mark.parametrize(
    "side,amount,symbol",
    [
        ("aaa", 1, "aaa"),
        ("SELL", "a", "aaa"),
        ("SELL", 1.0, "dddddddddddddddddddfdslkfjdlskfjsdlkfjsdddddddddd"),
        ("SELL", 1.0, "d"),
        ("SELL", 1.0, 1),
    ],
)
def test_spendings_validation(
    side, amount, symbol, mocker, dep_container, static_obook, pair
):
    orderbook = mocker.MagicMock()
    orderbook.get_orderbook.return_value = static_obook
    with dep_container.exchange.override(orderbook):
        params = {"side": side, "amount": amount, "pair": symbol}
        response = client.get("/info/spendings", params=params)
        assert response.status_code == 422
