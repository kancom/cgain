import enum
from math import isclose
from typing import Optional

from cgain.application import CurrencyPair, Exchange
from cgain.deps import Container
from cgain.restapi.dto.dto import Side, SpendRespDTO
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

router = APIRouter()


@router.get("/spendings", response_model=SpendRespDTO)
@inject
def rules(
    amount: float,
    side: Side = Query(..., enum=["SELL", "BUY"]),
    pair: Optional[str] = Query("BTC-USDT", min_length=3, max_length=20),
    exchange=Depends(Provide[Container.exchange]),
):
    try:
        orderbook = exchange.get_orderbook(pair=CurrencyPair(pair))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    if side == Side.BUY:
        best = orderbook.best_ask
        if best.volume >= amount:
            return SpendRespDTO(amount=best.price * amount)
        else:
            result = 0
            for offer in orderbook.asks:
                vol_pie = min([offer.volume, amount])
                result += offer.price * vol_pie
                amount -= vol_pie
                if isclose(amount, 0.0):
                    break
            assert isclose(amount, 0.0), "Full amount can't be bought"
            return SpendRespDTO(amount=result, is_averaged=True)
    else:
        best = orderbook.best_bid
        if best.volume >= amount:
            return SpendRespDTO(amount=best.price * amount)
        else:
            result = 0
            for demand in orderbook.bids:
                vol_pie = min([demand.volume, amount])
                result += demand.price * vol_pie
                amount -= vol_pie
                if isclose(amount, 0.0):
                    break
            assert isclose(amount, 0.0), "Full amount can't be sold"
            return SpendRespDTO(amount=result, is_averaged=True)
