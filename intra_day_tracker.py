from pytrading import Portfolio
from pytrading.live_trading import trending_stocks, stock_tracker
from pytrading.download_tickers import load_biggest_movers, load_positions, pickle_biggest_movers, pickle_positions, get_day_hot_stocks
from time import sleep

def live_stock_data(*positions):
	pickle_biggest_movers(Portfolio(get_day_hot_stocks()[:51]))
	pickle_positions(Portfolio(positions))
	i = 0
	try:
		while True:
			if i % 15 == 0:
				pickle_biggest_movers(Portfolio(get_day_hot_stocks()[:51]))
			trending_stocks(load_biggest_movers())
			print(end='\n'*2)
			stock_tracker(load_positions())
			sleep(52)
	except KeyboardInterrupt:
		return

