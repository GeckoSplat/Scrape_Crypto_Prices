from requests import* 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Scraping tool for crypto coin prices from coinmarketcap.com API 

def coin_price(): # Connects to API and retrieves information

    print ('-----------------------------------------------------\nSource : CoinMarketCap.com\n-----------------------------------------------------')

    URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest" # Points to the API interface
    parameters = {
    'start':'1',
    'limit':'20', # change here to display more / less coins . Max 5000
    'convert':'GBP' # change 'GBP' to currency of your choice

    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.get("apikey"), # Gets your API key from your json file
    } 

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(URL, params=parameters,)
        data = json.loads(response.text)
        for entry in data ["data"]: # For each coin in scraped data do the below
            symbol = entry["symbol"]# symbol is BTC etc
            name = entry["name"] # Full string name ie : Bitcoin
            price = entry ["quote"] # quote holds all price info
            print(symbol ,name , '£',price[(list(price.keys())[0])]["price"],'\n') # selects first item in dict "quote" after
            #converting to a list. This displays only the price information required.

    except (ConnectionError, Timeout, TooManyRedirects) as e: # Error handling
        print(e)


if __name__ == "__main__":
    with open ('apidata.json') as apidata: # Load API key before connection
        config = json.load(apidata)
    
    coin_price()