from .config import BaseConfig
from utils.utils import singleton

'''
    现货相关配置类
'''

'''
    现货客户端配置类
'''
@singleton
class MarketClientConfig(BaseConfig):
    _section = 'market_client'
    
    def __init__(self, section_name: str = 'market_client') -> None:
        super().__init__()
        self._section = section_name
        
    def get_base_url(self):
        return self._configer.get(self._section, 'base_url')
    
    def get_api_key(self):
        return self._configer.get(self._section, 'api_key')
    
    def get_api_secret(self):
        return self._configer.get(self._section, 'api_secret')
    
    def get_market_kline_interval(self):
        return self._configer.get(self._section, 'kline_interval')
    
    def get_market_kline_limit(self):
        return self._configer.getint(self._section, 'kline_limit')
    
    