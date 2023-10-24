from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from tasks import global_tasks
from multiprocessing.managers import Namespace


schedular = BlockingScheduler()

def init_glable_schedular(glabal_namespace: Namespace):

    # 应用启动时执行一次，之后每天零点执行一次，现货市场加密货币种类的更新的定时任务，based on usdt
    global_tasks.schedular_get_symbols(glabal_namespace.symbol_list)
    schedular.add_job(global_tasks.schedular_get_symbols, 'cron', hour=0, minute=0, second=0, args=[glabal_namespace.symbol_list])
    
    #请求现货市场上所有已知加密货币的k线图，每15分钟执行一次
    global_tasks.schedular_get_market_condition_each_symbol(glabal_namespace.symbol_list, 
                            glabal_namespace.symbol_market,
                            glabal_namespace.symbol_market_data_update_event)
    schedular.add_job(global_tasks.schedular_get_market_condition_each_symbol,
                      'cron', 
                      minute='*/15', 
                      args=[glabal_namespace.symbol_list, 
                            glabal_namespace.symbol_market,
                            glabal_namespace.symbol_market_data_update_event])
    

