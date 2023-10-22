import talib
import pandas as pd
from datetime import datetime
# data = pd.DataFrame({
#     'high': [82.15, 81.89, 83.03, 83.30, 83.85, 83.90, 83.33, 84.30, 84.84, 85.00],
#     'low': [81.29, 80.64, 81.31, 82.65, 83.07, 83.11, 82.49, 83.80, 84.15, 84.66],
#     'close': [81.59, 81.06, 82.87, 83.00, 83.61, 82.25, 82.84, 84.15, 84.55, 84.36]
# })

# # 计算KDJ指标
# high = data['high'].values
# low = data['low'].values
# close = data['close'].values

# k, d = talib.STOCH(high, low, close)
# j = 3 * d - 2 * k

# # 打印KDJ值
# print('K:', k)
# print('D:', d)
# print('J:', j)
[1697964900000, '0.05960000', '0.05960000', '0.05950000', '0.05950000', '2498.40000000', 1697964959999, '148.79185000', 6, '1370.50000000', '81.68180000', '0']
print(type(float('29.36000000')))
print(datetime.fromtimestamp(1637719200000/1e3))
print(datetime.fromtimestamp(1697966100000/1e3))