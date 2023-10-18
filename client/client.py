import requests
from typing import Optional, Any, List, Tuple
from datetime import datetime
from enum import Enum
import hmac
import hashlib

"""
    Binance 客户端类
    用于连接Binance API平台, 执行操作

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

class Client:
    api_key:str = None
    api_secret:str = None
    base_url = 'https://api.binance.com'
    health_status:Health_Status = Health_Status.UNKNOWN
    health_check = True
    health_check_freq = 30
    session = None

    def __init__(self, api_key: str, 
                 api_secret: str, 
                 base_url: Optional[str] = None, 
                 health_check: Optional[bool] = None,
                 health_check_freq: Optional[int] = None) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.health_check = health_check
        self.health_check_freq = health_check_freq
        self.session = self._init_session()

    # 初始化session    
    def _init_session(self) -> requests.Session:
        session = requests.session()
        headers = {
            'Accept': 'application/json',
            'X-MBX-APIKEY': self.api_key
        }
        session.headers.update(headers)
        return session
    
    def _generate_timestamp(self) -> int:
        return round(datetime.now().timestamp() * 1000)
    
    def _signature_params(self, params_str: str) -> str:
        return hmac.new(self.api_secret.encode('utf-8'), 
                        params_str.encode('utf-8'), 
                        hashlib.sha256).hexdigest()
    
    
    def _generate_get_params(params: dict) -> str:
        pass

    def get_account(self):
        timestamp = self._generate_timestamp()

    def _get_account(self):
        timestamp = self._generate_timestamp()
        self.session.get()