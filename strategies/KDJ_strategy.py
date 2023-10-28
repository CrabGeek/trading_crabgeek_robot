import talib
import pandas as pd
import numpy as np
from datetime import datetime
from .result import Result, ResultEnum
'''
    KDJ 指标交易策略
    
    over_sell_signal: 超卖信号
    over_buy_signal: 超买信号
    
    计算KDJ指标的过程如下:

    计算N日内的最低价 (Lowest Low)和最高价(Highest High):
    首先, 需要确定计算KDJ指标所使用的时间周期N。在这个周期内, 需要找出最低价的最低值和最高价的最高值。

    计算当日的RSV值 (Raw Stochastic Value): 
    RSV是根据当日收盘价 (Close) 在N日内最低价和最高价的位置计算得出的百分比。RSV的计算公式如下: 
    RSV = (Close - Lowest Low) / (Highest High - Lowest Low) * 100

    计算当日的K值 (K-line): 
    K值是根据前一日的K值和当日的RSV值计算得出的平滑值。K值的计算公式如下: 
    K = a * 前一日K值 + (1 - a) * 当日RSV
    其中, a为平滑系数, 一般取2 / (N + 1)。

    计算当日的D值 (D-line)
    D值是根据前一日的D值和当日的K值计算得出的平滑值。D值的计算公式如下: 
    D = a * 前一日D值 + (1 - a) * 当日K值

    计算当日的J值 (J-line):
    J值是K值和D值的加权平均值,常用的加权系数为3。J值的计算公式如下:
    J = 3 * 当日K值 - 2 * 当日D值
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
        
        return Result(symbol=symbol, result=ResultEnum.BUY_OR_GO_LONG)
        
    elif current_d_value > over_buy_signal and \
        current_d_value < previous_d_value and \
            current_k_value < previous_k_value and \
                previous_k_value > previous_d_value and \
                    current_k_value < current_d_value:

        return Result(symbol=symbol, result=ResultEnum.SELL_OR_GO_SHORT)
        
    return None
    