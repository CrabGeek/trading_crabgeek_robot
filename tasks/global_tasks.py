from clients.spot_client import Client

def schedular_get_symbols():
    client = Client()
    client.exchange_info()
    print(client.base_url)
    
