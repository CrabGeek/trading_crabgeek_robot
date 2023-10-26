import numpy as np
import talib
from .strategy import BaseStrategy
from .result import Result, ResultEnum
'''
    RSI 策略
'''

class RSIStrategy(BaseStrategy):
    _lower_rsi: int = 20
    _upper_rsi: int = 80
    _rsi_window: int = 21

    def __init__(self, lower_rsi: int = 20, upper_rsi: int = 80, rsi_window: int = 21) -> None:
        super().__init__("RSI")
        self._lower_rsi = lower_rsi
        self._upper_rsi = upper_rsi
        self._rsi_window = rsi_window

    def strategy(self, data: dict) -> Result or None:
        symbol = data['symbol']
        close_prices = np.array([float(kd[4]) for kd in data['value']])

        rsi = talib.RSI(close_prices, self._rsi_window)

        # result = 

        # 进入超买区间, 可以考虑卖出
        if rsi > self._upper_rsi:
            return Result(symbol=symbol, strategy=self.strategy_name, data=f'RSI: {rsi}', result=ResultEnum.SELL_OR_GO_SHORT)
        # 进入超卖区间, 可以考虑买入
        elif rsi < self._lower_rsi:
            return Result(symbol=symbol, strategy=self.strategy_name, data=f'RSI: {rsi}', result=ResultEnum.BUY_OR_GO_LONG)