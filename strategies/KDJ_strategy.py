import talib
import pandas as pd
import numpy as np
from datetime import datetime

def KDJ_strategy_callable(data: dict):
    symbol = data['symbol']
    klines_data = data['value']
    print(f'length: {len(klines_data)}')
    
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
    
    k_last = k[-1]
    d_last = d[-1]
    j_last = j[-1]
    
    k_minus_d_abs = abs(k_last - d_last)
    k_minus_j_abs = abs(k_last - j_last)
    d_minus_j_abs = abs(d_last - j_last)
    
    print(f'{symbol}: k: {k_last}, d: {d_last}, j: {j_last}, k-d abs: {k_minus_d_abs}, last kline: {klines_data[0][0]} {klines_data[-1][0]}')
    if k_minus_d_abs <= 5 and k_minus_j_abs <= 5 and d_minus_j_abs:
        print('--------')
        print(f'{symbol} is time')
        print('--------')
    