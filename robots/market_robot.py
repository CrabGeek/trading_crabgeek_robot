from clients.client import BaseClient
from .robot import BaseRobot
from multiprocessing.synchronize import Event
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, List
from multiprocessing.managers import ListProxy
from .robot import RobotStatus
from service.email_service import EmailService
import asyncio
from strategies.result import Result
from strategies.strategy import BaseStrategy
import json

'''
    现货市场机器人
'''

class MarketRobot(BaseRobot):
    executor: ThreadPoolExecutor = None
    strategy_obj: BaseStrategy = None
    data: ListProxy
    email_enable: bool = False
    email_service: EmailService = None
    result_list: List[Result]
    def __init__(self, 
                 event: Event, 
                 client: BaseClient,
                 executor: ProcessPoolExecutor,
                 strategy_obj: BaseStrategy,
                 data: ListProxy,
                 email_service: EmailService,
                 nickname: str='market_robot',
                 email_enable: bool = False) -> None:
        super().__init__(nickname=nickname, execute_event = event, client = client)
        self.executor = executor
        self.strategy_obj = strategy_obj
        self.data = data
        self.email_enable = email_enable
        self.email_service = email_service
        self.result_list = []
    
    def run(self):
        if self.executor is None:
            print('executor is none')
            #TODO : need log
            return
        if self.data is None:
            #TODO : need log
            print('data is none')
            return
        if self.strategy_obj is None:
            print('strategry is none')
            return
        self.status = RobotStatus.RUNNING
        
        while True:
            try:
                self.execute_event.wait()
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                tasks = [loop.run_in_executor(self.executor, self.strategy_obj.strategy, symbol_data) for symbol_data in self.data]
                done_tasks, _ = loop.run_until_complete(asyncio.wait(tasks, timeout=300))
                self.result_list.clear()
                for task in done_tasks:
                    result = task.result()
                    if result is not None:
                        json_str = json.dumps(result.__dict__, indent=4)
                        print(json_str)
                        self.result_list.append(result)
                if self.email_service is not None and self.email_enable == True:
                    asyncio.run(self.email_service.async_send(self.result_list))
                self.execute_event.clear()
            except Exception as e:
                print(e)
                self.execute_event.clear()
                self.result_list.clear()
                break