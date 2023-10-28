from enum import Enum
import json

class ResultEnum(str, Enum):
    BUY_OR_GO_LONG = 'buy/go_long'
    SELL_OR_GO_SHORT = 'sell/go_short'
    UNKNOWN = 'UNKNOWN'
    
class Result:
    symbol: str = ''
    strategy: str = ''
    data: dict = {}
    result: ResultEnum = ResultEnum.UNKNOWN
    
    def __init__(self, symbol: str, strategy: str, result: ResultEnum, data: dict = {}) -> None:
        self.symbol = symbol
        self.result = result
        self.strategy = strategy
        self.data = data
