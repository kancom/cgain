from cgain.application.domain.value_objects import Side
from pydantic import BaseModel, Field


class SpendQueryDTO(BaseModel):
    side: Side
    amount: float
    pair: str = Field(
        default="BTC-USDT",
        min_length=2,
        max_length=20,
        description="an instrument to query about",
        example="BTC-USDT",
    )


class SpendRespDTO(BaseModel):
    amount: float
    is_averaged: bool = Field(default=False)
