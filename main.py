from clients.spot_client import Client
from config.market_config import MarketClientConfig
from config.service_config import EmailSerivceConfig
from multiprocessing import Manager
from schedular.task_schedular import schedular, init_glable_schedular
from management.manage import init_global_tasks_namespace, init_global_obj_namespace
from robots.robots_manager import RobotsManager
from service.email_service import EmailService
from utils.utils import init_threading_executor, init_processing_executor
from strategies.KDJ_RSI_strategy import KDJAndRSIStrategy


marketClientConfig = MarketClientConfig()
emailClientConfig = EmailSerivceConfig()

client = Client(api_key=marketClientConfig.get_api_key(), 
                api_secret=marketClientConfig.get_api_secret(), 
                base_url=marketClientConfig.get_base_url())

email_service = EmailService(smtp_server_url=emailClientConfig.get_smtp_server_url(),
                             smtp_port=emailClientConfig.get_smtp_port(), 
                             sender_email=emailClientConfig.get_sender_email(),
                             receiver_email=emailClientConfig.get_receiver_email(),
                             username=emailClientConfig.get_username(),
                             email_key=emailClientConfig.get_key(),
                             test=False)

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
        init_glable_schedular(namespace_tuple[0], marketClientConfig)
            
        robotsManager = RobotsManager(executor=threadingExecutor)
        robotsManager.create(auto_run=True, 
                                event=namespace_tuple[0].symbol_market_data_update_event, 
                                client=client, 
                                executor=processingExecutor,
                                strategy_obj=KDJAndRSIStrategy(),
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
    
    