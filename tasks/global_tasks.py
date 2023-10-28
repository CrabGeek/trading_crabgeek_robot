from clients.spot_client import Client
from multiprocessing.managers import ListProxy
from multiprocessing.synchronize import Event
import asyncio
from datetime import datetime


def schedular_get_symbols(symbol_list: ListProxy):
    try:
        # TODO: need LOG
        client = Client()
        exchange_info = asyncio.run(client.async_exchange_info())
        quote_asset_usdt_list = list(filter(lambda x: x['quoteAsset'] == 'USDT', exchange_info['symbols']))
        symbol_list[:] = list(map(lambda x : x['symbol'], quote_asset_usdt_list))
    except Exception as e:
        print(e)
    

def schedular_get_market_condition_each_symbol(symbol_list: ListProxy, symbol_market: ListProxy, symbol_kline_data_event: Event, 
                                               interval: str ='15', limit: int = 192):
    # TODO: need log
    try:
        client = Client()
        # end_time= round(datetime.now().timestamp() * 1000) 
        # start_time = end_time - 3600 * 1000
        
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        # start_time=start_time, end_time=end_time,
        tasks = [loop.create_task(client.async_klins(symbol=symbol, interval=interval, limit=limit)) for symbol in symbol_list]
        done_tasks, _ = loop.run_until_complete(asyncio.wait(tasks, timeout=120))
        # 更新symbol_list
        symbol_market[:] = []
        for done_task in done_tasks:
            symbol_market.append(done_task.result())
        #通知Robot数据已更新好，执行相应策略
        symbol_kline_data_event.set()
    except asyncio.TimeoutError as e:
        # TODO: need log
        #  异步请求k线数据任务超时
        print(e)
    