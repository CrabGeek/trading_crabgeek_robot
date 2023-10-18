from datetime import datetime
import http.client
import hmac
import hashlib


# print(client.get_all_tickers())

# for kline in client.get_historical_klines_generator("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
#     print(kline)

# print(client.get_account())


api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

time = round(datetime.now().timestamp() * 1000)
query_string = f'timestamp={time}'

m = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()



conn = http.client.HTTPSConnection("testnet.binance.vision")
# conn = http.client.HTTPSConnection("api.binance.com")
payload = ''
headers = {
  'X-MBX-APIKEY': api_key
}
conn.request("GET", f"/api/v3/account?signature={m}&{query_string}", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# print('&'.join([f"{d[0]}={d[1]}" for d in [('timestamp', '1234'), ('user', 'charlie')]]))