from requests import *
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# TODO: this is not a scraping tool. It uses an API key to fetch data
# Scraping tool for crypto coin prices from coinmarketcap.com API


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
        # TODO: Lazy error handling. Can split into individual exceptions
        raise Exception(e)

    return data


def print_prices(query_data: dict):
    # For each coin / token
    for entry in query_data:

        # Symbol e.g BTC
        symbol = entry.get("symbol", None)

        # Full string name i.e : Bitcoin
        name = entry.get("name", None)

        # Quote holds all price info
        quote = entry.get("quote", None)

        if quote is None:
            print(f"Could not retrieve price info for: {name} ({symbol})")
            continue

        # TODO: Lazy. Assuming these always exist from here on. Update currency to param
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

    if API_KEY is None:
        # TODO: check if correct error type
        raise TypeError("Could not retrieve API_KEY")

    # Points to the API interface
    URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    # TODO: consider having a configuration file or converting to a command line script which takes
    #       these as optional arguments which replace the defaults here
    parameters = {
        "start": "1",
        "limit": "20",  # change here to display more / less coins . Max 5000
        "convert": "GBP",  # change 'GBP' to currency of your choice
    }
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}

    data = query_prices(parameters, headers, URL)

    # None inside get() is the default but being explicit for learning purposes
    if data.get("data", None) is not None:
        print(f"{50*'-'}\nSource : CoinMarketCap.com\n{50*'-'}")
        print_prices(data.get("data"))
    else:
        print("Failed to retrieve data")
