import smtplib
from email.mime.text import MIMEText
from email.header import Header
from utils.utils import singleton
import json
from datetime import datetime
from strategies.result import Result
from typing import List

'''
    邮箱服务类
'''
@singleton
class EmailService:
    _server: smtplib.SMTP_SSL = None
    _running: bool = False
    _default_header: str = 'Crabgeek auto 筛选'
    smtp_server_url: str = ''
    smtp_port: int = 0
    sender_email: str = ''
    receiver_email: str = ''
    username: str = ''
    email_key: str = ''
    test: bool = False
    
    def __init__(self, smtp_server_url: str, 
                 smtp_port: int, 
                 sender_email: str,
                 receiver_email: str,
                 username: str,
                 email_key: str, test: bool = False) -> None:
        self.smtp_server_url = smtp_server_url
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.username = username
        self.email_key = email_key
        self.test = test
        
        self._server = smtplib.SMTP_SSL(self.smtp_server_url, self.smtp_port)
    
    def _connect(self):
        self._server.connect(self.smtp_server_url, self.smtp_port)
    
    def _login(self):
        try:
            self._server.login(self.username, self.email_key)
            self._running = True
        except Exception as e:
            # TODO: need log
            print(e)
            self._running = False
    def quit(self):
        self._server.quit()
        self._running = False
        
    
        
    def send(self, data: List[Result]):
        msg = self._build_msg(data=data)
        if msg is None:
            return
        try:
            self._send(msg=msg)
        except Exception as e:
            # TODO: need log
            print(e)
            
    async def async_send(self, data: List[Result]):
        msg = self._build_msg(data=data)
        if msg is None:
            return
        try:
            await self._async_send(msg=msg)
        except Exception as e:
            # TODO: need log
            print(e)
        
        
        
    def _send(self, msg: str):
        self._connect()
        self._login()
        self._server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
        self._server.quit()
        
    async def _async_send(self, msg: str):
        self._send(msg=msg)
    
        
    def _build_msg(self, data: List[Result]) -> MIMEText or None:
        if data is None or len(data) == 0:
            # TODO: need log
            return None
        json_str = json.dumps([ob.__dict__ for ob in data], indent=4)
        print(json_str)
        msg = MIMEText(json_str, 'plain', 'utf-8')
        header_str = f'{self._default_header} - {datetime.now()}' if self.test == False else f'Test - {datetime.now()}'
        msg['Subject'] = Header(header_str, 'utf-8')
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        
        return msg
        


