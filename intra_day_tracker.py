from pytrading import Portfolio
from pytrading.live_trading import trending_stocks, stock_tracker
from pytrading.download_tickers import load_biggest_movers, load_positions, pickle_biggest_movers, pickle_positions, get_day_hot_stocks
from time import sleep, time

# Have option input() for which signals they want enabled
# 2000 calls/hour. 50 stocks + num of stocks that were tracked
# I could also get the actual time it takes to track the stocks then use that data from how many calls a second
# Assume 2.8 calls a seconds. (2000 / (50+x)/2.8) + time for pickling every 5 periods
# Add more signals

# Double bottom and double top shouldn't be that hard
# Time per stock varies greatly when a lot of stocks are having movement
# Maybe when one period away from 2k and under an hour, calculate how long you will have to wait

# What if the live_stock_data had a bunch of methods inside of it, and just use if statements with all the signals you add as arguments
# How much run time does calling a function add vs doing an extra if statement

# with very minimal logic, 4.23 stocks/second
# Take the 3600s/(2000/(number of stocks)) THEN WAIT that amount of time every loop 

def live_stock_data():
	user_signals = input('Please enter the signals you want to be tracked, with spaces in between. The current available signals are: \
		1ma, 2ma, 9ma_cross, double_bottom, double_top, basing: ').split()
	user_positions = input('Please enter the tickers of the stocks you want to track independently, with spaces in between: ').split()
	pickle_biggest_movers(Portfolio(get_day_hot_stocks()[:51]))
	pickle_positions(Portfolio(user_positions))
	delay = 3600/(2000/(50 + len(user_positions)))
	i = 0
	try:
		while True:
			t1 = time()
			if i % 5 == 0:
				pickle_biggest_movers(Portfolio(get_day_hot_stocks()[:51]))
			trending_stocks(load_biggest_movers(), user_signals)
			print(end='\n'*2)
			stock_tracker(load_positions())
			time_elapsed = time() - t1
			# print(f'Time elapsed: {time_elapsed:.2f}s')
			# stocks_per_second = (len(load_biggest_movers()) + len(load_positions()))/time_elapsed
			# print(f'Stocks per second: {stocks_per_second:.2f} stocks/s')
			sleep(delay-time_elapsed)
			print(f'{time()-t1:.2f}s')
	except KeyboardInterrupt:
		return
