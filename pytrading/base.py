import requests as _requests
import datetime as _datetime
import pandas as _pd

_pd.options.display.max_rows = 1000

"""
You use proxies for webscraping to prevent getting banned from the website.
Example proxy:
proxies = {
 “http”: “http://10.10.10.10:8000”,
 “https”: “http://10.10.10.10:8000”,
}
r = requests.get(“http://toscrape.com”, proxies=proxies)

Things to add:
For None values, if the value before and after are within a couple percent, fill na with average of two, else it's a suspension
https://stackoverflow.com/questions/44032771/fill-cell-containing-nan-with-average-of-value-before-and-after
df.val[:-1] = 
https://stackoverflow.com/questions/44111425/cannot-use-fillna-when-a-condition-is-introduced
"""
class Ticker:

	def __init__(self, ticker):
		# Could use 'https://query2.finance.yahoo.com/v8/finance/chart/' if query1 doesn't work
		self._base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'

		self.ticker = ticker.upper()

	def __repr__(self):
		return f'Pytrading stock object {self.ticker}'

	def get_data(self, interval='1m', period='1d', start=None, end=_datetime.datetime.today(), proxy=None):
		if start is None:
			# Valid ranges: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
			params = {'range': period}
		else:
			params = {'period1': start, 'period2': end}

		# Valid intervals: 
		params['interval'] = interval.lower()

		# Issue where Yahoo would return 60m interval when you wanted 30m interval
		if params['interval'] == '30m':
			params['interval'] == '15m'

		# Format proxy for requests
		if proxy is not None:
			if isinstance(proxy, dict) and 'https' in proxy:
				proxy = proxy['https']
			proxy = {'https': proxy}

		url = self._base_url + self.ticker
		data = _requests.get(url=url, params=params, proxies=proxy)
		data = data.json()

		if data['chart']['error']:
			url = 'https://query2.finance.yahoo.com/v8/finance/chart/' + self.ticker
			data = _requests.get(url=url, params=params, proxies=proxy)
			data = data.json()
			if data['chart']['error']:
				print(f'An error has occurred while accessing Yahoo\'s Finance api for {self.ticker}')
				return None

		df = _pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=data['chart']['result'][0]['timestamp'])
		df = df.round(decimals=2)
		if interval == '1d':
			df.index = list(map(lambda x: _datetime.datetime.fromtimestamp(x).date(), df.index))			
		else:
			df.index = list(map(lambda x: _datetime.datetime.fromtimestamp(x), df.index))
		df = df[['close', 'high', 'low', 'open', 'volume']]
		df.columns = list(map(lambda name: name.capitalize(), df.columns))

		return df


