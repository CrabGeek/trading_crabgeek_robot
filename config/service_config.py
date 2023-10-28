from .config import BaseConfig
from utils.utils import singleton

'''
    service相关配置类
'''
@singleton
class EmailSerivceConfig(BaseConfig):
    _section = 'email_service'
    
    def __init__(self, section_name: str = 'email_service') -> None:
        super().__init__()
        self._section = section_name
        
    def get_smtp_server_url(self):
        return self._configer.get(self._section, 'smtp_server_url')
    
    def get_smtp_port(self):
        return self._configer.getint(self._section, 'smtp_port')
    
    def get_sender_email(self):
        return self._configer.get(self._section, 'sender_email')
    
    def get_receiver_email(self):
        return self._configer.get(self._section, 'receiver_email')
    
    def get_username(self):
        return self._configer.get(self._section, 'username')
    
    def get_key(self):
        return self._configer.get(self._section, 'email_key')
    
        
    