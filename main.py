from clients.spot_client import Client
from utils.utils import init_processing_executor
import time
from multiprocessing import Manager
from schedular.task_schedular import schedular, init_glable_schedular
from management.manage import init_global_tasks_namespace, init_global_obj_namespace
from robots.robots_manager import RobotsManager
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from strategies.MA_KDJ_strategy import ma_kdj_strategy_callable
from datetime import datetime


from multiprocessing.synchronize import Event
import concurrent.futures

api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

client = Client(api_key=api_key, api_secret=api_secret, base_url='https://testnet.binance.vision')



def init_global_manager() -> tuple:
    manager = Manager()

    global_tasks_namespace = init_global_tasks_namespace(manager=manager)
    global_obj_namespace = init_global_obj_namespace(manger=manager)
    
    return global_tasks_namespace, global_obj_namespace
    

def print_datetime():
    # print('waiing')
    # event.wait()
    print(datetime.now())

class Foo:
    event: Event
    def __init__(self, event: Event) -> None:
        self.event = event
    def run(self):
        executor = ThreadPoolExecutor()
        while True:
            self.event.wait()
            tasks = [executor.submit(print_datetime) for i in range(0, 3)]
            concurrent.futures.wait(tasks)
            self.event.clear()
            
        
           

def main():
    try:
        namespace_tuple = init_global_manager()
        init_glable_schedular(namespace_tuple[0])
        schedular.start()
        
        # executor = ThreadPoolExecutor()
        # executor.submit(print_datetime, namespace_tuple[0].symbol_market_data_update_event)
        # foo = Foo(event=namespace_tuple[0].symbol_market_data_update_event)
        # executor = ThreadPoolExecutor()
        # executor.submit(foo.run)
            
        
        robotsManager = RobotsManager(executor=ThreadPoolExecutor())
        robotsManager.create(auto_run=True, 
                             event=namespace_tuple[0].symbol_market_data_update_event, 
                             client=client, 
                             executor=ThreadPoolExecutor(),
                             strategy=ma_kdj_strategy_callable,
                             data=namespace_tuple[0].symbol_market,
                             nickname='carbgeek'
                             )
        while True:
            time.sleep(5)
            # namespace_tuple[0].symbol_market_data_update_event.set()
        
        
        
        
    except Exception as e:
        print(e)
        schedular.shutdown()

        
    

if __name__ == '__main__':
    main()