from datetime import date 
from .base import Ticker
import pandas as pd 

class Portfolio:
	# Maybe do a DataFrame? Easier to display, can sort. Columns for tickers, change_percentage, last_updated_price
	# Pass in stocks with their target values, like this: (stock, target_prices)
	def __init__(self, stocks, interval='1m', period='1d'):
		# if type(stocks) == tuple:
		# 	self.stocks = stocks[0]

		# if type(stocks[0]) != str:
		# 	while stocks[0] != str:
		# 		stocks = stocks[0]
		# 		print(stocks)
		self.stocks = [Stock(stock, interval=interval, period=period) for stock in sorted(stocks)]

	def clean_stocks(self):
		for stock in self.stocks:
			if 'trash' in stock.ticker:
				self.stocks.remove(stock)

	def get_biggest_movers(self):
		print("These are today's biggest movers: ")
		for stock in self.stocks:
			if stock.daily_change_percentage > 10.0:
				print(stock.ticker)

	def get_highest_rel_volume(self):
		print("These are today's most relatively active stocks: ")
		for stock in self.stocks:
			if stock.get_relative_volume() > 3.0:
				print(stock.ticker)
		# return [stock.ticker for stock in self.stocks if stock.get_relative_volume() > 3.0]

	def get_stocks(self):
		return [stock.ticker for stock in self.stocks]

	def get_stocks_daily(self):
		return [stock.df_month for stock in self.stocks]

	def get_stocks_intra(self):
		return [stock.df for stock in self.stocks]

	def sort_by(self, sort='name'):
		if sort == 'name':
			pass
		elif sort == 'change_percentage':
			pass
		elif sort == 'price':
			pass
		else:
			raise Exception('Please enter one of the following sorting methods: name, price, or change_percentage')

	def update_price_change(self):
		print("These stocks' prices have changed significantly.")
		for stock in self.stocks:
			if (stock.df.iloc[0]['Close'] - stock.get_last_updated())/(stock.get_last_updated())*100 > 5.0:
				stock.set_last_updated(stock.df.iloc[0]['Close'])
				print(stock.ticker)

	def __iter__(self):
		return iter(self.stocks)

	def __getitem__(self, i):
		return self.stocks[i]

	def __len__(self):
		return len(self.stocks)

	def __repr__(self):
		return 'A portfolio of #winning stocks.'

class Stock:

	def __init__(self, ticker, interval='1m', period='1d', target_prices=None, price_invested=None):
		self.ticker = ticker
		self.df = Ticker(ticker).get_data(interval, period)
		self.prev_close = Ticker(ticker).get_data('1d', '2d').iloc[0]['Close']
		try:
			self._last_updated_price = self.df.iloc[-1]['Close']
		except:
			pass
		self.target_prices = target_prices
		self.price_invested = price_invested

	def get_month_data(self, num=1):
		df = Ticker(self.ticker).get_data('1d', f'{num}mo')
		df.index = pd.to_datetime(df.index)
		return df

	def add_target_prices(self, new_target_prices):
		self.target_prices = new_target_prices

	def daily_change_percentage(self):
		return ((self.df.iloc[-1]['Close'] - self.df.iloc[-2]['Close'])/self.df.iloc[-2]['Close'])*100

	def daily_high_change_percentage(self):
		return ((self.df.iloc[-1]['High'] - self.df.iloc[-2]['Close'])/self.df.iloc[-2]['Close'])*100

	def daily_stats(self):
		return self.df.iloc[-1]['Close'], self.df.iloc[-1]['High'], self.df.iloc[-1]['Low']

	def get_relative_volume(self):
		avg_volume = sum(self.df['Volume'])/len(self.df)
		return self.df.iloc[-1]/avg_volume

	def get_last_updated(self):
		return self._last_updated_price

	def set_last_updated(self, price):
		self._last_updated_price = price

	def update_stock(self):
		self.df = get_intra_day_data(self.ticker)
		self.df_month = get_month_data(self.ticker)

	def __str__(self):
		return self.ticker


# 	for i in range(2, ticker.shape[0]):
# 		ticker.loc[ticker.index[i], '2_sma'] = sum([float(i) for i in ticker.iloc[i-2:i]['Close']])/2
# 	for i in range(9, ticker.shape[0]):
# 		ticker.loc[ticker.index[i], '9_sma'] = sum([float(i) for i in ticker.iloc[i-9:i]['Close']])/9
# 	try:
# 		ticker = ticker[['Close', 'High', 'Low', '2_sma', '9_sma', 'Volume']]
# 	except:
# 		pass

print('Welcome to PyTrading!')

if __name__ == '__main__':
	# You can use this to test code out without it being imported/ran 
	pass
