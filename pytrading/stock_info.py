from datetime import date
import requests
import yfinance as yf 

# notify when near support/resistance levels
# Change resolution: 1, 5, 15, 30, 60, D, W, M
# Either just put all the functions in here, or can make a class where you put in a ticker then you get all the methods for that ticker


# Functions/Classes I prob won't use/update

# class StockTechnicals:

# 	def __init__(self, ticker, initial_price=None, shares=None):
# 		self.ticker = ticker
# 		self.api_key = 'bs2a4ffrh5rc90r54hm0'
# 		self.initial_price = initial_price
# 		self.shares = shares

# 	def get_aggregate_indicators(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/scan/technical-indicator?symbol={self.ticker}&resolution=D&token={self.api_key}')
# 		response = r.json()['technicalAnalysis']
# 		return response

# 	def get_all_methods(self):
# 		# Could so self.get_aggregate_indictators.__name__, but that is extra
# 		return ['get_aggregate_indicators', 'get_company_news', 'get_live_price', 'get_news_sentiment', 'get_patterns', 
# 		'get_price_target', 'get_support_resistance', 'get_technical_indictator']

# 	def get_current_price(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={self.ticker}&from={start_date}&to={end_date}&token={self.api_key}')
# 		response = r.json()
# 		return response['c']

# 	def get_company_news(self, start_date, end_date):
# 		r = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={self.ticker}&from={start_date}&to={end_date}&token={self.api_key}')
# 		response = r.json()
# 		return response

# 	def get_live_price(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={self.ticker}&token={self.api_key}')
# 		response = r.json()
# 		return f"Current Price: ${response['c']}, Change %: {((response['c'] - response['pc'])/response['pc'])*100:.2f}%, High: ${response['h']}, Low: ${response['l']}, Open: ${response['o']}"
	
# 	def get_news_sentiment(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/news-sentiment?symbol={self.ticker}&token={self.api_key}')
# 		response = r.json()
# 		return response

# 	def get_patterns(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/scan/pattern?symbol={self.ticker}&resolution=D&token={self.api_key}')
# 		response = r.json()
# 		return response

# 	def get_price_target(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/stock/price-target?symbol={self.ticker}&token={self.api_key}')
# 		response = r.json()
# 		return response

# 	def get_profit(self):
# 		initial_capital = self.initial_price * self.shares
# 		current_capital = self.get_current_price() * self.shares
# 		return current_capital - initial_capital

# 	def get_support_resistance(self):
# 		r = requests.get(f'https://finnhub.io/api/v1/scan/support-resistance?symbol={self.ticker}&resolution=D&token={self.api_key}')
# 		response = r.json()
# 		return response

# 	def get_technical_indictator(self, ticker, indicator):
# 		r = requests.get(f'https://finnhub.io/api/v1/indicator?symbol={self.ticker}&resolution=D&from=1583098857&to=1584308457&indicator={indicator}&timeperiod=3&token={self.api_key}')
# 		response = r.json()
# 		return response


# def check_basing(df):
# 	for i in range(5, df.shape[0]):
# 		prices = sorted(df.iloc[i-5:i]['Close'])
# 		change_percentage = ((prices[-1] - prices[0]) / prices[0])*100
# 		# Should I use the variance thing
# 		if change_percentage < 1.5:
# 			# df.iloc[i-5:i]
# 			print(f'{change_percentage:.2f}% High: {prices[0]:.2f} Low: {prices[-1]:.2f}', df.iloc[i])

# def get_support_levels(df):
# 	# Look at lows 10 mins late, so you can see if it is a real low or not
# 	for i in range(20, df.shape[0]):
# 		if len([price for price in df.iloc[i-20:i]['Low'] if price >= df.iloc[i-10]['Low']]) == 20:
# 			print('Support level', df.iloc[i-10])

# def get_current_trades(ticker):

# 	def on_message(ws, message):
# 	    print(message)

# 	def on_error(ws, error):
# 	    print(error)

# 	def on_close(ws):
# 	    print("### closed ###")

# 	def on_open(ws):
# 	    ws.send('{"type":"subscribe","symbol":"BILI"}')

# 	if __name__ == "__main__":
# 	    websocket.enableTrace(True)
# 	    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={api_key}",
# 	                              on_message = on_message,
# 	                              on_error = on_error,
# 	                              on_close = on_close)
# 	    ws.on_open = on_open
# 	    ws.run_forever()


# def get_rsi_levels(portfolio):
# 	for stock in portfolio:
# 		up_moves = []
# 		down_moves = []
# 		prices_14 = stock.df_month.iloc[-15:]
# 		for i in range(len(prices_14))[1:]:
# 			price_mvmt = prices_14.iloc[i]['Close'] - prices_14.iloc[i-1]['Close']
# 			if price_mvmt >= 0:
# 				up_moves.append(price_mvmt)
# 			else:
# 				down_moves.append(price_mvmt)
# 		try:
# 			up_avg = sum(up_moves)/len(up_moves)
# 			down_avg = abs(sum(down_moves)/len(down_moves))
# 		except:
# 			print('RSI of 0 or 100')
# 			continue
# 		rs = up_avg/down_avg
# 		print(stock.ticker, up_avg, down_avg, rs)
# 		rsi = 100 - 100/(1 + rs)
# 		print(stock.ticker, rsi)
		
# def double_bottom(df):
# 	current_low = df.iloc[0]['Low']
# 	for i in range(1, df.shape[0]):
# 		last_low =  df.iloc[i]['Low']
# 		prev_low = df.iloc[i-1]['Low']
# 		if last_low < current_low*1.005:
# 			if last_low > current_low*0.995:
# 				print('Double bottom', df.iloc[i])
# 			else:
# 				current_low = last_low
# 			print('New low', current_low, df.iloc[i])


# def dip_detector(df):
# 	falling = (False, None)
# 	for i in range(1, df.shape[0]):
# 		last_close =  last_close
# 		prev_close = df.iloc[i-1]['Close']
# 		if last_close < prev_close:
# 			falling = (True, prev_close)
# 		elif last_close > prev_close:
# 			if df.iloc[i] >= falling[1]:
# 				falling = (False, None)
# 			elif falling:
# 				print('Basing')
# 				falling = (False, falling[1])
# 			print(df.iloc[i], df.iloc[i-1])


# def sma_cross(df):
# 	for i in range(14, df.shape[0]):
# 		if (df.iloc[i-1]['8_sma'] < df.iloc[i-1]['13_sma']) and (df.iloc[i]['8_sma'] > df.iloc[i]['13_sma']):
# 			print('8 SMA CROSSED 13 SMA!!!', df.iloc[i-1]['8_sma'], df.iloc[i-1]['13_sma'], df.iloc[i]['8_sma'], df.iloc[i]['13_sma'])
# 			print(df.iloc[i])	
# 		elif (df.iloc[i-1]['8_sma'] > df.iloc[i-1]['13_sma']) and (df.iloc[i]['8_sma'] < df.iloc[i]['13_sma']):
# 			print('13 SMA CROSSED 8 SMA!!!', df.iloc[i-1]['8_sma'], df.iloc[i-1]['13_sma'], df.iloc[i]['8_sma'], df.iloc[i]['13_sma'])
# 			print(df.iloc[i])
# 		if df.iloc[i]['8_sma'] > df.iloc[i]['Close']:
# 			print(df.iloc[i])


# def support(df):
# 	support_prices = []
# 	for i in range(1, df.shape[0]):
# 		cur_low, last_low = get_lows(df)
		# If the somewhere in the next 10 mins the price is 1-2% higher than here, counts as low. And currently lower than the last_low
		# if cur_low < last_low and all([price for price in df.iloc[i:i+5] if price > next_low or not ]):


# Check if webull charts agree with how much it crosses, maybe I need to make error larger?
# Dip detector. Counts as a dip when every 1m close is lower, but then once the next close is higher, that's the bottom
# What if I made a machine learning algorithm where I fed it stock prices during a dip. It comes up with a parabolic function?

