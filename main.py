from requests import* 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



def coin_price():

    print ('-----------------------------------------------------\nSource : CoinMarketCap.com\n-----------------------------------------------------')

    URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
    'start':'1',
    'limit':'20',
    'convert':'GBP'

    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.get("apikey"),
    } 

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(URL, params=parameters,)
        data = json.loads(response.text)
        for entry in data ["data"]:
            symbol = entry["symbol"]
            name = entry["name"]
            price = entry ["quote"]
            print(symbol ,name , '£',price[(list(price.keys())[0])]["price"],'\n') 

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


if __name__ == "__main__":
    with open ('apidata.json') as apidata:
        config = json.load(apidata)
    
    coin_price()