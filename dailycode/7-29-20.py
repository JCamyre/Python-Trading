from pytrading import Portfolio, get_intra_day_data, get_month_data
import pytrading.live_trading
from pytrading.live_trading import trending_stocks
from pytrading.download_tickers import load_todays_biggest_movers, pickle_biggest_movers, get_biggest_movers
import pandas as pd
# for stock in Portfolio(['ARLO']):
# 	print(stock.df)

pickle_biggest_movers(pytrading.Portfolio(get_biggest_movers()))
print(load_todays_biggest_movers())
esda = get_intra_day_data('EDSA')
print(esda.reset_index())
print(esda[240:360].nsmallest(5, ['Low'])['Close'])
for i in esda[240:360].nsmallest(5, ['Low'])['Close']:
	print(i)
print(get_month_data('EDSA'))
