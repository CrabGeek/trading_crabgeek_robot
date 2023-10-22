import talib
import pandas as pd
import numpy as np
from datetime import datetime
from .result import Result, ResultEnum
'''
    KDJ 指标交易策略
    
    over_sell_signal: 超卖信号
    over_buy_signal: 超买信号
'''
# TODO: need config
over_sell_signal = 20
over_buy_signal = 80

def KDJ_strategy_callable(data: dict) -> Result or None:
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
    
    previous_k_value = k[-2]
    previous_d_value = d[-2]
    previous_j_value = j[-2]
    
    # 当D < 超卖线, K线和D线同时上升，且K线从下向上穿过D线时，买入/做多
    if current_d_value < over_sell_signal and \
        current_d_value > previous_d_value and \
            current_k_value > previous_k_value and \
                previous_k_value < previous_d_value and \
                    current_k_value > current_d_value:
        print('++++++++++++')
        print(f'{symbol} is time to buy/go_long')
        print('++++++++++++')
        return Result(symbol=symbol, result=ResultEnum.BUY_OR_GO_LONG)
        
    elif current_d_value > over_buy_signal and \
        current_d_value < previous_d_value and \
            current_k_value < previous_k_value and \
                previous_k_value > previous_d_value and \
                    current_k_value < current_d_value:
        print('++++++++++++')
        print(f'{symbol} is time to sell/go_short')
        print('++++++++++++')
        return Result(symbol=symbol, result=ResultEnum.SELL_OR_GO_SHORT)
        
    return None
    