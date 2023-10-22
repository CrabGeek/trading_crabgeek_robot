from clients.client import BaseClient
from multiprocessing.synchronize import Event
from enum import Enum
from typing import List
from strategies.result import Result

from threading import Event as threadingEvent
'''
    交易机器人基类
    
    nickname: 别名
    execute_event: 事件通知, 一旦robot被通知, 就会执行注册的策略
    client: 与Binance 
'''

class RobotStatus(str, Enum):
    RUNNING = 'RUNNING'
    STOP = 'STOP'

class BaseRobot:
    nickname: str = ''
    execute_event: Event = None
    client: BaseClient = None
    status: RobotStatus = RobotStatus.STOP
    compute_completed_event: threadingEvent
    
    def __init__(self, nickname: str, execute_event: Event, client: BaseClient) -> None:
        self.nickname = nickname
        self.execute_event = execute_event
        self.client = client
    
    def run(self):
        raise NotImplementedError("This method is abstract and not implemented yet")
    