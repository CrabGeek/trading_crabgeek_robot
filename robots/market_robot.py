from clients.client import BaseClient
from .robot import BaseRobot
from multiprocessing.synchronize import Event
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures 
from typing import Callable, List
from multiprocessing.managers import ListProxy
from .robot import RobotStatus
from service.email_service import EmailService
import asyncio
from strategies.result import Result


'''
    现货市场机器人
'''

class MarketRobot(BaseRobot):
    executor: ThreadPoolExecutor = None
    strategy: Callable = None
    data: ListProxy
    email_enable: bool = False
    email_service: EmailService = None
    result_list: List[Result]
    def __init__(self, 
                 event: Event, 
                 client: BaseClient, 
                #  executor: ThreadPoolExecutor,
                 executor: ProcessPoolExecutor,
                 strategy: Callable,
                 data: ListProxy,
                 email_service: EmailService,
                 nickname: str='market_robot',
                 email_enable: bool = False) -> None:
        super().__init__(nickname=nickname, execute_event = event, client = client)
        self.executor = executor
        self.strategy = strategy
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
        if self.strategy is None:
            print('strategry is none')
            return
        self.status = RobotStatus.RUNNING
        
        while True:
            try:
                print('waiting')
                self.execute_event.wait()
                print('execute')
                print(len(self.data))
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                # tasks = [self.executor.submit(self.strategy, symbol_data) for symbol_data in self.data]
                # results = [task.result() for task in concurrent.futures.as_completed(tasks)]
                # for result in results:
                #     if result is not None:
                #         self.result_list.append(result)
                tasks = [loop.run_in_executor(self.executor, self.strategy, symbol_data) for symbol_data in self.data]
                done_tasks, _ = loop.run_until_complete(asyncio.wait(tasks, timeout=180))
                for task in done_tasks:
                    result = task.result()
                    if result is not None:
                        self.result_list.append(result)
                print('complete and read to send')
                if self.email_service is not None and self.email_enable == True:
                    asyncio.run(self.email_service.async_send(self.result_list))
                self.execute_event.clear()
                self.result_list.clear()
            except Exception as e:
                print(e)
                self.execute_event.clear()
                self.result_list.clear()
                break