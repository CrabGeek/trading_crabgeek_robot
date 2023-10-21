from clients.spot_client import Client
from multiprocessing.managers import ListProxy
from multiprocessing.synchronize import Event
import asyncio
from datetime import datetime


def schedular_get_symbols(symbol_list: ListProxy):
    # TODO: need LOG
    client = Client()
    exchange_info = asyncio.run(client.async_exchange_info())
    quote_asset_usdt_list = list(filter(lambda x: x['quoteAsset'] == 'USDT', exchange_info['symbols']))
    symbol_list[:] = list(map(lambda x : x['symbol'], quote_asset_usdt_list))
    

def schedular_get_market_condition_each_symbol(symbol_list: ListProxy, symbol_market: ListProxy, symbol_kline_data_event: Event):
    # TODO: need log
    client = Client()
    end_time= round(datetime.now().timestamp() * 1000) 
    start_time = end_time - 3600 * 1000
    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(client.async_klins(symbol=symbol, start_time=start_time, end_time=end_time, interval='1m', limit=1000)) for symbol in symbol_list]
    
    try:
        done_tasks, _ = loop.run_until_complete(asyncio.wait_for(tasks, timeout=120))
        # 更新symbol_list
        symbol_list[:] = []
        for done_task in done_tasks:
            symbol_market.append(done_task.result())
        symbol_kline_data_event.set()
    except asyncio.TimeoutError as e:
        # TODO: need log
        #  异步请求k线数据任务超时
        print(e)
    