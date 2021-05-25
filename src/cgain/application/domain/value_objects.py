from enum import Enum

CurrencyPair = str
Price = float
Volume = float

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
