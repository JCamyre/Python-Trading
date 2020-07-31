from pytrading import Portfolio
from pytrading.live_trading import trending_stocks, stock_tracker
from pytrading.download_tickers import load_biggest_movers, load_positions, pickle_biggest_movers, get_day_hot_stocks
from time import sleep

def live_stock_data(*positions):
	# Every 5-10 mins update hottest stocks
	pickle_biggest_movers(Portfolio(get_day_hot_stocks()))
	pickle_position(Portfolio(positions))
	i = 0
	try:
		while True:
			if i % 10 == 0:
				pickle_biggest_movers(Portfolio(get_day_hot_stocks()))
			trending_stocks(load_biggest_movers())
			stock_tracker(load_positions())
			sleep(45)
	except KeyboardInterrupt:
		return

