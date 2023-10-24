import concurrent.futures
import sys
import signal
import os

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

def signal_handler(signum, frame):
        print(f'PID: {os.getpid()}')
        sys.exit(0)
        
def process_pool_initializer():
    signal.signal(signal.SIGINT, signal_handler)

def init_processing_executor():
    return concurrent.futures.ProcessPoolExecutor(max_workers=10, initializer=process_pool_initializer)

def init_threading_executor():
    return concurrent.futures.ThreadPoolExecutor(max_workers=20)