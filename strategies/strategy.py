
from .result import Result

class BaseStrategy:
    strategy_name:str = ''

    def __init__(self, strategy_name: str) -> None:
        self.strategy_name = strategy_name

    def strategy(self, data: dict) -> Result or None:
        raise NotImplementedError()