from pytrading import Portfolio
import pytrading.live_trading
from pytrading.live_trading import trending_stocks
from pytrading.download_tickers import load_todays_biggest_movers, pickle_biggest_movers, get_biggest_movers
from time import sleep

# try:
# 	while True:
# 		trending_stocks(load_todays_biggest_movers()[:60])
# 		print(end='\n' * 20)
# 		sleep(45)
# except KeyboardInterrupt:
# 	pass

