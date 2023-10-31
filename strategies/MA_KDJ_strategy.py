import talib
import pandas as pd
import numpy as np

from strategies.result import Result, ResultEnum
from .strategy import BaseStrategy

'''
    EMA均线5, 20 + KDJ策略, 主要以EMA 均线为主
'''

class MAAndKDJStrategy(BaseStrategy):
    
    _fast_peroid: int = 5
    _slow_peroid: int = 20

    def __init__(self, strategy_name: str = 'MA_KDJ', fast_peroid: int = 5, slow_peroid: int = 20) -> None:
        super().__init__(strategy_name)
        self._fast_peroid = fast_peroid
        self._slow_peroid = slow_peroid
    
    def strategy(self, data: dict) -> Result:
        try:
            symbol = data['symbol']
            klines_data = data['value']

            high = []
            low = []
            close = []
                
            for kd in klines_data:
                high.append(float(kd[2]))
                low.append(float(kd[3]))
                close.append(float(kd[4]))

            
            # high:最高价, low: 最低价, close: 收盘价
            df = pd.DataFrame({
                'high': high,
                'low': low,
                'close': close
            })
            
            k, d = talib.STOCH(df['high'].values, 
                        df['low'].values, 
                        df['close'].values)
            j = 3*k - 2*d

            current_k_value = k[-1]
            current_d_value = d[-1]
            current_j_value = j[-1]

            ema_fast = talib.EMA(df['close'].values, self._fast_peroid)
            ema_slow = talib.EMA(df['close'].values, self._slow_peroid)

            current_ema_fast = ema_fast[-1]
            current_ema_slow = ema_slow[-1]

            pre_ema_fast = ema_fast[-2]
            pre_ema_slow = ema_slow[-2]

            # EMA5从下向上穿过EMA20, 买入或做多信号
            if pre_ema_fast <= pre_ema_slow and current_ema_fast > current_ema_slow:
                result_data = {
                    'KDJ:': f'K: {round(current_k_value, 5)}, D: {round(current_d_value, 5)}, J: {round(current_j_value, 5)}',
                    'EMA:': f'EMA_5: {round(current_ema_fast, 5)}, EMA_20: {round(current_ema_slow, 5)}'
                }

                return Result(symbol=symbol, strategy=self.strategy_name, data=result_data, result=ResultEnum.BUY_OR_GO_LONG)
            
            # EMA5 从上向下穿过EMA20, 卖出或做空
            elif pre_ema_fast >= pre_ema_slow and current_ema_fast < current_ema_slow:
                result_data = {
                    'KDJ:': f'K: {round(current_k_value, 5)}, D: {round(current_d_value, 5)}, J: {round(current_j_value, 5)}',
                    'EMA:': f'EMA_5: {round(current_ema_fast, 5)}, EMA_20: {round(current_ema_slow, 5)}'
                }
                return Result(symbol=symbol, strategy=self.strategy_name, data=result_data, result=ResultEnum.BUY_OR_GO_LONG)
            
            return None

        except Exception as e:
            # TODO: Need log
            print(e)
            return None