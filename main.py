from clients.spot_client import Client
from utils.utils import init_executor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import datetime
import time
from multiprocessing import Event, Process, Manager
from schedular.task_schedular import schedular, init_glable_schedular
from management.manage import init_global_tasks_namespace
import asyncio
from asyncio import Future
import threading
from functools import partial


api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

client = Client(api_key=api_key, api_secret=api_secret, base_url='https://testnet.binance.vision')

async def print_date(event: Event):
    while True:
        event.wait()
        print(datetime.now())
        event.clear()
    
def main():
    try:
        manager = Manager()
        global_name_space = init_global_tasks_namespace(manager)
        init_glable_schedular(global_name_space)
        schedular.start()
        while True:
            time.sleep(5)
    except Exception as e:
        schedular.shutdown()

        
    

if __name__ == '__main__':
    main()