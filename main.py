from clients.spot_client import Client
import time
from multiprocessing import Manager
from schedular.task_schedular import schedular, init_glable_schedular
from management.manage import init_global_tasks_namespace, init_global_obj_namespace
from robots.robots_manager import RobotsManager
from strategies.KDJ_strategy import KDJ_strategy_callable
from service.email_service import EmailService
from utils.utils import init_threading_executor, init_processing_executor
import os


# api_key='8ne2q3GEHrnk5HTd73LNinuvQ3yJRkFHOma3EHciwXiJpkUSOAXzBvdepo0Qp41j'
# api_secret='3yQvwYYq6nmBdkIJhogK2UMhLCT5f4ogEB3bVta7Q1XkU5V2eNdFq18169cImkzc'

api_key = 'Gj5NNvle8D1kckyrvwk32iehifGxGgrpppdqCDoEEjUNxQ0boDvmmg1AFpFQIybn'
api_secret='7sb3bTUkNPBhoDEQvNHuWqMHltdrsqhTKKJ4O0fLHfWV5Co919j2MUvV5jTS4mE5'

base_url='https://api.binance.com'
test_url='https://testnet.binance.vision'

smtp_server_url = 'smtp.qq.com'
smtp_port = 465
sender_email = '2573543975@qq.com'
receiver_email = '2573543975@qq.com'
username = '2573543975@qq.com'
email_key = 'hhlwxhvazjojdied'


client = Client(api_key=api_key, api_secret=api_secret, base_url=base_url)

email_service = EmailService(smtp_server_url=smtp_server_url,
                             smtp_port=smtp_port, 
                             sender_email=sender_email,
                             receiver_email=receiver_email,
                             username=username,
                             email_key=email_key)

threadingExecutor = init_threading_executor()
processingExecutor = init_processing_executor()

def init_global_manager() -> tuple:
    manager = Manager()

    global_tasks_namespace = init_global_tasks_namespace(manager=manager)
    global_obj_namespace = init_global_obj_namespace(manger=manager)
    
    return global_tasks_namespace, global_obj_namespace  
           

def main():
    try:
        namespace_tuple = init_global_manager()
        init_glable_schedular(namespace_tuple[0])
            
        robotsManager = RobotsManager(executor=threadingExecutor)
        robotsManager.create(auto_run=True, 
                                event=namespace_tuple[0].symbol_market_data_update_event, 
                                client=client, 
                                executor=processingExecutor,
                                strategy=KDJ_strategy_callable,
                                data=namespace_tuple[0].symbol_market,
                                nickname='carbgeek',
                                email_service = email_service,
                                email_enable = True
                                )
        schedular.start()
    except Exception as e:
        print(e)
        print('app cloing..')

if __name__ == '__main__':
        main()
    
    