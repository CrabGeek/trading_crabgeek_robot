import requests
from typing import Optional, Any, List, Tuple
from datetime import datetime
from enum import Enum
import hmac
import hashlib
from binance.spot import Spot
from utils.utils import singleton
from .client import BaseClient

"""
    Binance 现货类客户端类
    用于连接Binance API现货平台, 执行操作

    api_key: 必填, 在Binance API管理页面自行生成
    api_secret: 必填, 在Binance API 管理页面自行生成
    base_url: 非必填, 测试网URL为https://testnet.binance.vision,
    health_check: 非必填, 是否开启健康检查
    health_Check: 非必填, 健康检查频率, 单位seconds


"""

class Health_Status(str, Enum):
    UNKNOWN = "UNKNOWN"
    GREEN = "GREEN"
    RED = "RED"

@singleton
class Client(BaseClient):
    api_key:str = None
    api_secret:str = None
    base_url = 'https://api.binance.com'
    health_status:Health_Status = Health_Status.UNKNOWN
    health_check = True
    health_check_freq = 30
    session = None
    spot_client = None
    test_data = 0

    def __init__(self, api_key: str, 
                 api_secret: str, 
                 base_url: Optional[str] = None, 
                 health_check: Optional[bool] = None,
                 health_check_freq: Optional[int] = None) -> None:
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.health_check = health_check
        self.health_check_freq = health_check_freq
        self.session = self._init_session()
        self.spot_client = self._init_spot_client()
        

    # 初始化session    
    def _init_session(self) -> requests.Session:
        session = requests.session()
        headers = {
            'Accept': 'application/json',
            'X-MBX-APIKEY': self.api_key
        }
        session.headers.update(headers)
        return session

    # Binance 官方客户端初始化
    def _init_spot_client(self):
        return Spot(api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url)

    def _generate_timestamp(self) -> int:
        return round(datetime.now().timestamp() * 1000)
    
    def _signature_params(self, params_str: str) -> str:
        return hmac.new(self.api_secret.encode('utf-8'), 
                        params_str.encode('utf-8'), 
                        hashlib.sha256).hexdigest()
    
    
    def _generate_get_params(params: dict) -> str:
        pass

    def account(self) -> dict or None:
        try:
            return self.spot_client.account()
        except Exception as e:
            # TODO: need log
            print(e)
            return None
        
    async def async_account(self):
        async def __asyncify():
            return self.account()
        return await __asyncify()
        
    def klines(self, symbol: str, start_time: float = None, end_time: float = None, interval:str = '1h', limit: str = 800) -> dict or None:
        try:
            if start_time is None or end_time is None:
                return {'symbol': symbol, 
                        'value': self.spot_client.klines(symbol=symbol, interval=interval, limit=limit)}
            else:
                return {'symbol': symbol,
                        'value': self.spot_client.klines(symbol=symbol, interval=interval, limit=limit, startTime=start_time, endTime=end_time)}
        except Exception as e:
            # TODO: need Log
            print(e)
            return None
        
    async def async_klins(self, *args, **kwargs):
        async def __asyncify():
            return self.klines(*args, **kwargs)
        return await __asyncify()
                
    def exchange_info(self):
        try:
            return self.spot_client.exchange_info()
        except Exception as e:
            # TODO: need log
            return None
    
    async def async_exchange_info(self):
        async def __asyncify():
            return self.exchange_info()
        return await __asyncify()