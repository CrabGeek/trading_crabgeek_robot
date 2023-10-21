import concurrent.futures
import multiprocessing
# 单例模式 装饰器
def singleton(cls):
    instances = {}
    def wapper(*arg, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*arg, **kwargs)
        return instances[cls]
    return wapper

# 初始化全局进程池
# TODO: 需要可配置
def init_executor():
    return concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())
