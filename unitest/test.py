import talib
import pandas as pd
from datetime import datetime
from threading import Event
from concurrent.futures import ThreadPoolExecutor
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# # data = pd.DataFrame({
# #     'high': [82.15, 81.89, 83.03, 83.30, 83.85, 83.90, 83.33, 84.30, 84.84, 85.00],
# #     'low': [81.29, 80.64, 81.31, 82.65, 83.07, 83.11, 82.49, 83.80, 84.15, 84.66],
# #     'close': [81.59, 81.06, 82.87, 83.00, 83.61, 82.25, 82.84, 84.15, 84.55, 84.36]
# # })

# # # 计算KDJ指标
# # high = data['high'].values
# # low = data['low'].values
# # close = data['close'].values

# # k, d = talib.STOCH(high, low, close)
# # j = 3 * d - 2 * k

# # # 打印KDJ值
# # print('K:', k)
# # print('D:', d)
# # print('J:', j)
# [1697964900000, '0.05960000', '0.05960000', '0.05950000', '0.05950000', '2498.40000000', 1697964959999, '148.79185000', 6, '1370.50000000', '81.68180000', '0']
# print(type(float('29.36000000')))
# print(datetime.fromtimestamp(1637719200000/1e3))
# print(datetime.fromtimestamp(1697966100000/1e3))

# import json
# import asyncio

# from strategies.result import Result, ResultEnum
# from typing import List

# l: List[Result] = []

# r = Result(symbol='r', result=ResultEnum.BUY_OR_GO_LONG)
# k = Result(symbol='k', result=ResultEnum.BUY_OR_GO_LONG)

# l.append(r)
# l.append(k)

# print(json.dumps([ob.__dict__ for ob in l], indent=4))
# async def print_date():
#     print('hhhahahah')
    

# async def asyn_print():
#     await asyncio.sleep(5)
#     await print_date()
#     return 'hhh'
    
# asyncio.run(asyn_print())

# print(datetime.now())

# # loop = asyncio.get_event_loop()

# # task = [loop.create_task(asyn_print()) for i in range(0, 5)]

# # loop.run_until_complete(asyncio.wait(task))

# asyncio.gather(asyn_print())

# print(datetime.now())




# # 原始的JSON字符串
# json_str = '{"name": "John Doe", "age": 30, "email": "johndoe@example.com"}'

# # 将JSON字符串解析为Python对象
# json_data = json.loads(json_str)

# # 将Python对象转换回美化的JSON字符串
# formatted_json_str = json.dumps(json_data, indent=4)

# print(formatted_json_str)

# event = Event()

# def print_d(event: Event):
#     while True:
#         print('waiting')
#         event.wait()
#         print('dddd')
#         event.clear()
        
# with ThreadPoolExecutor() as executor:
#     executor.submit(print_d, event)

# print('000000') 
# while True:
#     time.sleep(3)
#     event.set()
# my_list = [1, 2, "three", {"four": 4, "five": 5}]

# # 将list对象转换为JSON字符串
# json_str = json.dumps(my_list, indent=4)

# print(json_str)

# smtp_server = 'smtp.qq.com'
# smtp_port = 465

# sender_email = '2573543975@qq.com'
# receiver_email = '2573543975@qq.com'

# subject = 'Crabgeek 自动化筛选'

# message = '测试正文'

# # 创建一个MIMEText对象
# msg = MIMEText(message, 'plain', 'utf-8')


# msg['Subject'] = Header(subject, 'utf-8')
# msg['From'] = sender_email
# msg['To'] = receiver_email

# # 在这里输入你的QQ邮箱账号和授权码
# username = '2573543975@qq.com'
# password = 'hhlwxhvazjojdied'

# # 连接到QQ邮箱的SMTP服务器
# server = smtplib.SMTP_SSL(smtp_server, smtp_port)

# # 登录到QQ邮箱账号
# server.login(username, password)

# # 发送邮件
# server.sendmail(sender_email, receiver_email, msg.as_string())

# # 断开与服务器的连接
# server.quit()
