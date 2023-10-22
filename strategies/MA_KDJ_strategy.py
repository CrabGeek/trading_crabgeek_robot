import talib as ta
import pandas as pd
import numpy as np

'''
    均线密集 + KDJ策略 
'''

def ma_kdj_strategy_callable(data: dict):
    symbol = data['symbol']
    klins_data = data['value']
    
    