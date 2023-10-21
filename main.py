from clients.spot_client import Client
from utils.utils import init_executor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import datetime
import time


api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

client = Client(api_key=api_key, api_secret=api_secret, base_url='https://testnet.binance.vision')

executor = init_executor()

schedular = BackgroundScheduler()
schedular.add_executor(ProcessPoolExecutor())

# print(client.klines(symbol='BTCUSDT', interval='1h'))
# print(datetime.fromtimestamp(1697731199999/1e3))


# test_list = list(filter(lambda x: x['quoteAsset'] == 'USDT', client.exchange_info()['symbols']))
# print(test_list[0])

# print(executor)

def print_date():
    print(datetime.now())

if __name__ == '__main__':
    schedular.add_job(print_date, 'cron', second='*/5')
    schedular.start()
    while True:
        time.sleep(5)