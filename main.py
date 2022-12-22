from requests import *
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

"""This is a tool to get crypto coin prices from Coinmarketcap.com using an API key to fetch data."""

def query_prices(parameters: dict, headers: dict, URL: str) -> dict:
    """Connects to API and retrieves information"""

    session = Session()

    # Data retrieved from query to API
    data = {}

    try:
        session.headers.update(headers)
        response = session.get(URL, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise Exception(e)

    return data


def print_prices(query_data: dict):
    # For each coin / token
    for entry in query_data:

        # Symbol e.g BTC
        symbol = entry.get("symbol", None)

        # Full string name e.g : Bitcoin
        name = entry.get("name", None)

        # Quote holds all price info
        quote = entry.get("quote", None)

        if quote is None:
            print(f"Could not retrieve price info for: {name} ({symbol})")
            continue

        price = quote["GBP"]["price"]
        percentage_change = quote["GBP"]["percent_change_24h"]

        # Assume 3 decimal places for price, can be configurable
        # £ sign can also be configurable based on parameters
        print(
            f"Name: {name}\nSymbol: {symbol}\nPrice: £{price:.3f}\n24h Change (%): {percentage_change}\n"
        )


if __name__ == "__main__":

    API_KEY: str

    with open("apidata.json", "r") as file:  # Load API key before connection
        config = json.load(file)
        API_KEY = config.get("apikey", None)


    # Points to the API interface
    URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {
        "start": "1",
        "limit": "20",  # change here to display more / less coins . Max 5000
        "convert": "GBP",  # change 'GBP' to currency of your choice
    }
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}

    data = query_prices(parameters, headers, URL)

    if data.get("data", None) is not None:
        print(f"{50*'-'}\nSource : CoinMarketCap.com\n{50*'-'}")
        print_prices(data.get("data"))
    else:
        print("Failed to retrieve data")
