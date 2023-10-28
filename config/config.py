import configparser
from utils.utils import singleton

'''
    配置读取基类
'''
class BaseConfig:
    _configer: configparser.ConfigParser = configparser.ConfigParser()
    
    def __init__(self) -> None:
        self._configer.read('./config.ini')
        
    