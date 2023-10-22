from clients.client import BaseClient
from .robot import BaseRobot
from multiprocessing.synchronize import Event
from concurrent.futures.thread import ThreadPoolExecutor
import concurrent.futures
from typing import Callable
from multiprocessing.managers import ListProxy
from .robot import RobotStatus

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
                 nickname: str='market_robot') -> None:
        super().__init__(nickname=nickname, execute_event = event, client = client)
        self.executor = executor
        self.strategy = strategy
        self.data = data
        
    
    def run(self):
        if self.executor is None:
            print('executor is none')
            #TODO : need log
            return
        if self.data is None:
            #TODO : need log
            print('data is none')
            return
        if self.strategy is None:
            print('strategry is none')
            return
        self.status = RobotStatus.RUNNING
        
        while True:
            print('waiting')
            self.execute_event.wait()
            print('execute')
            tasks = [self.executor.submit(self.strategy, symbol_data) for symbol_data in self.data]
            results = [task.result() for task in concurrent.futures.as_completed(tasks)]
            self.execute_event.clear()