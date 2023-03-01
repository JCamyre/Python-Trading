import requests as _requests
import os
import pandas as pd
from datetime import datetime
import time
import dotenv


# I think I would need a server to have alphavantagekey or users can supply their own
dotenv.load_dotenv('./.env')
key = os.environ.get('ALPHA_VANTAGE_KEY')  # os.getenv()


def _get_json(url: str):
    request = _requests.get(url)
    json = request.json()
    return json


class Ticker:
    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def get_data(self):
        # Quicker version? url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'
        # Can access more data but will cost a lot of time
        json = _get_json(
            f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&apikey={key}')
        while not json:
            try:
                json = _get_json(
                    f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&apikey={key}')['Time Series (Daily)']
                break
            except:
                time.sleep(3)

        # data = json['Time Series (Daily)']
        json = json['Time Series (Daily)']
            
        # Convert the JSON response from API to a Pandas DataFrame
        df = pd.DataFrame([[datetime.strptime(date, '%Y-%m-%d'), json[date]['4. close'], json[date]['2. high'], json[date]['3. low'], json[date]['1. open'], json[date]['6. volume']] for date in json.keys()],
                          columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
        df = df.set_index('Date')

        return df.iloc[:90]

    # maybe do &outputsize=full, idk what to use for.
    def get_intra_day_data(self):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.symbol}&interval=5min&apikey={key}'
        json = _get_json(url)
        while not json:
            try:
                json = _get_json(url)
                break
            except:
                time.sleep(3)

        df = pd.DataFrame([[datetime.strptime(date, '%Y-%m-%d'), json[date]['4. close'], json[date]['2. high'], json[date]['3. low'], json[date]['1. open'], json[date]['6. volume']] for date in json.keys()],
                          columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
        df = df.set_index('Date')
        return df

    def get_company_info(self):
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={key}'
        json = _get_json(url)
        while not json:
            try:
                json = _get_json(url)
                break
            except:
                time.sleep(3)

        df = pd.DataFrame([[datetime.strptime(date, '%Y-%m-%d'), json[date]['4. close'], json[date]['2. high'], json[date]['3. low'], json[date]['1. open'], json[date]['6. volume']] for date in json.keys()],
                          columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
        df = df.set_index('Date')
        return df
