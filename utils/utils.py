import concurrent.futures
import sys
import signal

# 单例模式 装饰器
def singleton(cls):
    instances = {}
    def wapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wapper

# 初始化全局进程池
# TODO: 需要可配置
def init_processing_executor():
    def signal_handler(signum, frame):
        sys.exit(0)

    def process_pool_initializer():
        signal.signal(signal.SIGINT, signal_handler)
    
    return concurrent.futures.ProcessPoolExecutor(max_workers=10)

def init_threading_executor():
    return concurrent.futures.ThreadPoolExecutor(max_workers=20)