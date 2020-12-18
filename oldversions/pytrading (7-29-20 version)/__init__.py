'''This package contains modules with functions that assist day traders by aiding them in keeping track of their positions 
and trending stocks, to hopefully make money on a day trade.'''
from datetime import date 
import yfinance as yf 

class Portfolio:
	# Maybe do a DataFrame? Easier to display, can sort. Columns for tickers, change_percentage, last_updated_price
	# Pass in stocks with their target values, like this: (stock, target_prices)
	def __init__(self, stocks=None):
		# print(stocks[0], isinstance(stocks[0], str))
		if type(stocks[0]) == str:
			self.stocks = [Stock(stock) for stock in sorted(stocks)]
		else:
			self.stocks = sorted(stocks, key=lambda x: x.ticker)

	def sort_by(self, sort='name'):
		if sort == 'name':
			pass
		elif sort == 'change_percentage':
			pass
		elif sort == 'price':
			pass
		else:
			raise Exception('Please enter one of the following sorting methods: name, price, or change_percentage')

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

	def __init__(self, ticker, target_prices=None, price_invested=None):
		self.ticker = ticker
		self.df = get_intra_day_data(self.ticker)
		self.df_month = get_month_data(self.ticker)
		try:
			self._last_updated_price = self.df.iloc[-1]['Close']
		except:
			print(f'{ticker} is a bad stock.')
		self.target_prices = target_prices
		self.price_invested = price_invested

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


def get_intra_day_data(ticker, interval='1m', today=True):
	if today:
		today = date.today()
		ticker = yf.Ticker(ticker).history(period='1d', interval=interval, prepost=True, actions=False).loc[today.strftime('20' + '%y-%m-%d') + ' 09:30:00-04:00':]
	else:
		ticker = yf.Ticker(ticker).history(period='3d', interval=interval, prepost=True, actions=False)
	for i in range(9, ticker.shape[0]):
		ticker.loc[ticker.index[i], '9_sma'] = sum([float(i) for i in ticker.iloc[i-9:i]['Close']])/9
	for i in range(20, ticker.shape[0]):
		ticker.loc[ticker.index[i], '20_sma'] = sum([float(i) for i in ticker.iloc[i-20:i]['Close']])/20

	# ticker['13_sma'] = ticker['Close'].iloc[12:].apply(lambda close: close.iloc[-13:].mean(axis=1))
	ticker = ticker.drop(columns=['Open', 'High'])
	ticker = ticker['Close', 'Low', '2_sma', '9_sma', 'Volume']
	return ticker

def get_month_data(ticker, interval='1d'):
	ticker = yf.Ticker(ticker).history(period='1mo', interval=interval, prepost=True, actions=False)
	return ticker


print('Welcome to the greatest Python trading module on Earth!')

if __name__ == '__main__':
	# You can use this to test code out without it being imported/ran 
	from download_tickers import get_todays_biggest_movers
	print('Welcome to the greatest Python trading module on Earth! Again.')

# put classes/methods in here

