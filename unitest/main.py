import concurrent.futures
import asyncio
import time
from datetime import datetime
import signal
import os
import sys

def print_date():
    # await asyncio.sleep(15)
    time.sleep(30)
    print(datetime.now())


def signal_handler(signum, frame):
    print(f'PID: {os.getpid()}')
    sys.exit(0)

def process_pool_initializer():
    signal.signal(signal.SIGINT, signal_handler)


def main():
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=10, initializer=process_pool_initializer)
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, print_date) for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt as e:
#         print('ctrl + c')