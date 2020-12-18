from pytrading import Portfolio
for stock in Portfolio(['WHLM', 'ARLO']):
	print(stock.df['High'].iloc[-250:-100])
	print(stock.df['Close'].iloc[-250:-100].idxmax())

