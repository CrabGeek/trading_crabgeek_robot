from strategies.result import Result
from .strategy import BaseStrategy
import pandas as pd
import talib
from .result import Result, ResultEnum
import json

'''
    KDJ RSI 混合策略
    KDJ 为主策略, RSI 为辅助策略
'''

class KDJAndRSIStrategy(BaseStrategy):
    
    # RSI 指标
    _lower_rsi: int = 20
    _upper_rsi: int = 80
    _rsi_window: int = 21
    
    # KDJ 指标
    _over_sell_signal: int = 20
    _over_buy_signal: int = 80
    
    def __init__(self, strategy_name: str = 'KDJ_RSI', lower_rsi: int = 20, 
                 upper_ris: int = 80, rsi_window: int = 21, 
                 over_sell_signal: int = 20, over_buy_signal: int = 80) -> None:
        super().__init__(strategy_name)
        
        self._lower_rsi = lower_rsi
        self._upper_rsi = upper_ris
        self._over_sell_signal = over_sell_signal
        self._over_buy_signal = over_buy_signal

    def strategy(self, data: dict) -> Result or None:
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
            
            
            rsi = talib.RSI(df['close'], self._rsi_window)
            
            
            current_k_value = k[-1]
            current_d_value = d[-1]
            current_j_value = j[-1]
            
            previous_k_value = k[-2]
            previous_d_value = d[-2]
            previous_j_value = j[-2]
            
            # 当D < 超卖线, K线和D线同时上升，且K线从下向上穿过D线时，买入/做多
            if current_d_value < self._over_sell_signal and \
                current_d_value > previous_d_value and \
                    current_k_value > previous_k_value and \
                        previous_k_value < previous_d_value and \
                            current_k_value > current_d_value:
                                
                result_data = {
                    'KDJ:': f'K: {round(current_k_value, 5)}, D: {round(current_d_value, 5)}, J: {round(current_j_value, 5)}',
                    'RSI:': f'{round(rsi.iloc[-1], 5) if len(rsi) > 0 else -1}'
                }
                return Result(symbol=symbol, strategy=self.strategy_name, data=result_data, result=ResultEnum.BUY_OR_GO_LONG)
                
            elif current_d_value > self._over_buy_signal and \
                current_d_value < previous_d_value and \
                    current_k_value < previous_k_value and \
                        previous_k_value > previous_d_value and \
                            current_k_value < current_d_value:
                result_data = {
                    'KDJ:': f'K: {round(current_k_value, 5)}, D: {round(current_d_value, 5)}, J: {round(current_j_value, 5)}',
                    'RSI:': f'{round(rsi.iloc[-1], 5) if len(rsi) > 0 else -1}'
                }
                return Result(symbol=symbol, strategy=self.strategy_name, data=result_data, result=ResultEnum.SELL_OR_GO_SHORT)
        
        except Exception as e:
            print(e)
            return None
        
        
        
        
