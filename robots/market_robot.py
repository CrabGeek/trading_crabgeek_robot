from robot import BaseRobot
from multiprocessing.synchronize import Event
from clients.client import BaseClient
from concurrent.futures.thread import ThreadPoolExecutor
import concurrent.futures
from typing import Callable
from multiprocessing.managers import ListProxy


'''
    现货市场机器人
'''

class MarketRobot(BaseRobot):
    executor: ThreadPoolExecutor = None
    strategy: Callable = None
    data: ListProxy
    def __init__(self, 
                 event: Event, 
                 client: BaseClient, 
                 executor: ThreadPoolExecutor,
                 strategy: Callable,
                 data: ListProxy,
                 nickname:str='market_robot') -> None:
        super.__init__(nickname=nickname, execute_event = event, client = client)
        self.executor = executor
        self.strategy = strategy
        self.data = data
        
    
        
    def run(self):
        if self.executor is None:
            #TODO : need log
            return
        if self.data is None or len(self.data) == 0:
            #TODO : need log
            return
        if self.strategy is None:
            return
        
        while True:
            self.execute_event.wait()            
            tasks = [self.executor.submit(self.strategy, args=(symbol_data,)) for symbol_data in self.data]
            results = [task.result() for task in concurrent.futures.as_completed(tasks)]
            print(results)
            self.execute_event.clear()