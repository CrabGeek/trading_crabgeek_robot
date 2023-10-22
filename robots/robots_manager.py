from .robot import BaseRobot
from typing import List
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.managers import ListProxy
from utils.utils import singleton
from robots.market_robot import MarketRobot

@singleton
class RobotsManager:
    _robots_list: List[BaseRobot] = None
    _robots_executor: ThreadPoolExecutor = None
    
    def __init__(self, executor: ThreadPoolExecutor) -> None:
        self._robots_executor = executor
        self._robots_list = []
    
    # TODO: 需要泛化，目前仅支持现货机器人
    def create(self, auto_run:bool = False, *args, **kwargs):
        robot = MarketRobot(*args, **kwargs)
        if auto_run:
            print(robot is None)
            self._robots_executor.submit(robot.run)
        self._robots_list.append(robot)
        
    def get_all_robots(self):
        return self._robots_list
    
    