import sys
# Used to access local module outside of its folder
sys.path.append('C:/Users/JWcam/Desktop/All_projects/Python-Trading')
from pytrading import Portfolio, get_intra_day_data, get_month_data, Stock
import pytrading.live_trading
from pytrading.live_trading import trending_stocks, stock_tracker
from pytrading.download_tickers import load_biggest_movers, pickle_biggest_movers, get_day_hot_stocks
import pandas as pd
from time import sleep
from pathlib import Path

# print(Path(__file__).parents[1])
pickle_biggest_movers(get_day_hot_stocks())
# try:
# 	while True:
# 		trending_stocks(load_biggest_movers())
# 		print(end='\n' * 5)
# 		# print(stock_tracker(Portfolio(['SONN', 'TLSA'])))
# 		print(end='\n' * 5)
# 		sleep(60)
# except KeyboardInterrupt:
# 	pass


# print(taop.reset_index())
# bottom = taop[40:140].nsmallest(10, ['Low'])['Low'].sort_values(ascending=True)
# print(bottom)
# print([price for price in bottom[1:] if bottom[0]*1.01 >= price])

# Penants at 12:00 to 12:30 and 12:31 to 13:31
# Indexes: 129 to 159 and 160 to 220
# Basically just look at the past 50 mins split into 4 sections
# first, second, third, last = taop.iloc[110:123], taop.iloc[123:135], taop.iloc[135:147], taop.iloc[147:160]
# delta_first, delta_second, delta_third, delta_last = first.max()['High'] - first.min()['Low'], second.max()['High'] - second.min()['Low'], third.max()['High'] - third.min()['Low'], last.max()['High'] - last.min()['Low']
# print(delta_first, delta_second, delta_third, delta_last)

# first, second, third, last = taop.iloc[160:175], taop.iloc[175:190], taop.iloc[190:205], taop.iloc[205:220]
# delta_first, delta_second, delta_third, delta_last = first.max()['High'] - first.min()['Low'], second.max()['High'] - second.min()['Low'], third.max()['High'] - third.min()['Low'], last.max()['High'] - last.min()['Low']
# print(delta_first, delta_second, delta_third, delta_last)



