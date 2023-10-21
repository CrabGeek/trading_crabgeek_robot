from typing import List
from robot import BaseRobot
from concurrent.futures import ProcessPoolExecutor
from utils.utils import singleton, init_executor
from robots.market_robot import MarketRobot

@singleton
class RobotsManager:
    _robots_list: List[BaseRobot] = None
    _robots_executor: ProcessPoolExecutor = None
    
    def __init__(self, executor:ProcessPoolExecutor) -> None:
        self._robots_executor = executor
        self._robots_list = []
    
    # TODO: 需要泛化，目前支持现货机器人
    def create(self, *args, **kwargs):
        robot = MarketRobot(*args, **kwargs)
        self._robots_list.append(robot)