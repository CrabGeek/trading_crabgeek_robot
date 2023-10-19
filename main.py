from datetime import datetime
from binance.spot import Spot

from client import spot_client


# print(client.get_all_tickers())

# for kline in client.get_historical_klines_generator("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
#     print(kline)

# print(client.get_account())


api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

client = spot_client.Client(api_key=api_key, api_secret=api_secret, base_url='https://testnet.binance.vision')

print(client.klines(symbol='BTCUSDT', interval='1h'))


# print(datetime.fromtimestamp(1697731199999/1e3))

