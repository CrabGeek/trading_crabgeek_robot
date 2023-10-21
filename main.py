from clients.spot_client import Client
from utils.utils import init_executor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import datetime
import time
from multiprocessing import Event, Process, Manager
from tasks import global_tasks
from schedular.task_schedular import schedular
import asyncio
from concurrent.futures import ProcessPoolExecutor as pool

api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

client = Client(api_key=api_key, api_secret=api_secret, base_url='https://testnet.binance.vision')

executor = ProcessPoolExecutor()

# schedular = BackgroundScheduler()
# schedular.add_executor(executor)


# print(client.klines(symbol='BTCUSDT', interval='1h'))
# print(datetime.fromtimestamp(1697731199999/1e3))


# test_list = list(filter(lambda x: x['quoteAsset'] == 'USDT', client.exchange_info()['symbols']))
# print(test_list[0])

# print(executor)

async def print_date(task: str):
    print(f'Task: {task}: {datetime.now()}')
    
async def async_run_print_date(task: str):
    await asyncio.sleep(5)
    await print_date(task)

def event_trigger(event: Event):
    event.set()

def event_receiver(event: Event):
    while True:
        event.wait()
        print(datetime.now())
        event.clear()
        

if __name__ == '__main__':
    # try:
    #     # manager = Manager()
    #     # event = manager.Event()
    #     # schedular.add_job(event_trigger, 'cron', second='*/5', args=[event])
    #     # p = Process(target=event_receiver, args=(event, ))
    #     # p.start()
    #     schedular.start()
    #     while True:
    #         time.sleep(5)
    # except Exception as e:
    #     schedular.shutdown()
    # print(datetime.now())
    # loop = asyncio.get_event_loop()
    
    # tasks = [loop.create_task(client.async_exchange_info())]
    
    # loop.run_until_complete(asyncio.wait(tasks))
    
    data = asyncio.run(client.async_exchange_info())
    print(data)
    # print(datetime.now())