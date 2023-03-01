import pytrading.py_trading as py_trd

# def format_stock_info(*tickers):
# 	stocks = []
# 	for stock_ticker in tickers:
# 		stock = {}
# 		cur_stats = stock_ticker.df_month.iloc[-1]
# 		prev_stats = stock_ticker.df_month.iloc[-2]
# 		stock['stock_ticker'] = stock_ticker.ticker
# 		stock['current_price'] = cur_stats['Close']
# 		stock['low_percentage'] = ((cur_stats['Low'] - prev_stats['Close'])/prev_stats['Close'])*100
# 		stocks.append(stock)
# 	return stocks

stonks = py_trd.Portfolio(['CBAY', 'OPGN'])
print(stonks[0].daily_high_change_percentage())
# print(format_stock_info(['CBAY', 'OPGN']))