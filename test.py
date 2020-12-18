import pytrading

def format_stock_info(*tickers):
	stocks = []
	for stock_ticker in pytrading.Portfolio(tickers):
		stock = {}
		cur_stats = stock_ticker.df_month.iloc[-1]
		prev_stats = stock_ticker.df_month.iloc[-2]
		stock['stock_ticker'] = stock_ticker.ticker
		stock['current_price'] = cur_stats['Close']
		stock['current_percentage'] = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100
		stock['high_percentage'] = ((cur_stats['High'] - prev_stats['Close'])/prev_stats['Close'])*100
		stock['low_percentage'] = ((cur_stats['Low'] - prev_stats['Close'])/prev_stats['Close'])*100
		stocks.append(stock)
	return stocks

print([stock.ticker for stock in pytrading.Portfolio(['CBAY', 'OPGN'])])
print(format_stock_info(['CBAY', 'OPGN']))