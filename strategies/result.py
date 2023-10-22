from enum import Enum
import json

class ResultEnum(str, Enum):
    BUY_OR_GO_LONG = 'buy/go_long'
    SELL_OR_GO_SHORT = 'sell/go_short'
    UNKNOWN = 'UNKNOWN'
    
class Result:
    symbol: str = ''
    result: ResultEnum = ResultEnum.UNKNOWN
    
    def __init__(self, symbol: str, result: ResultEnum) -> None:
        self.symbol = symbol
        self.result = result
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)