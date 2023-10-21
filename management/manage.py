from multiprocessing import Manager
from multiprocessing.managers import Namespace

def init_global_tasks_namespace(manager: Manager) -> Namespace:

    global_tasks_namespace = manager.Namespace()

    global_tasks_namespace.symbol_list = manager.list()
    global_tasks_namespace.symbol_market = manager.list()
    
    global_tasks_namespace.symbol_market_data_update_event = manager.Event()
    
    return global_tasks_namespace
    
