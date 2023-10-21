from multiprocessing import Manager

manager = Manager()

global_tasks = manager.Namespace()


global_tasks.symbol_list = manager.list()

# global_tasks