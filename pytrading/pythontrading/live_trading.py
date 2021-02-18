from datetime import date, datetime
import pandas as pd 
# from pygame import mixer
from time import sleep, strftime, localtime, time

# At the start of the day, get the top earners of the day, pickle it, and keep running the searching thing every 90 seconds (meaning time.sleep(15))

# mixer.init()

pd.options.display.max_rows = 1200
pd.options.display.max_columns = 10


def alert_sound():
	regular_instrumental = mixer.music.load("C:/Users/JWcam/Desktop/NCT 127 - Regular (Instrumental).mp3")
	mixer.music.set_volume(0.7)
	mixer.music.play()
	sleep(6.85)
	mixer.music.stop()


def stock_tracker(portfolio):
	"""Input which stocks you want to track, and the function will display the current price, low, highest change percentage, and
	current change percentage."""
	t1 = time()
	info = [f"Time: {strftime('%I:%M:%S', localtime())}"]
	print('Time ' + strftime('%I:%M:%S', localtime()))
	print([(stock.ticker, stock.df) for stock in portfolio])
	for stock in portfolio:

		# alert_sound() Do sound if within 5% of price target. Or do it if stock up 10% from price you bought it at. 
		try:
			stock.update_stock()
			cur_stats = stock.df_month.iloc[-1]
			prev_stats = stock.df_month.iloc[-2]
			intra_day_stats = stock.df
			m1, m5, m15, m30 = intra_day_stats.iloc[-1:][['Volume', 'Close']], intra_day_stats.iloc[-5:][['Volume', 'Close']]/5, intra_day_stats.iloc[-15:][['Volume', 'Close']]/5, intra_day_stats.iloc[-30:][['Volume', 'Close']]/5
			delta_volume = cur_stats['Volume']/sum(stock.df_month.iloc[-30:]['Volume'])
		except:
			continue
		
		# print(sum(m5['Volume'])/5, 1.25 * sum(m30['Volume'])/30, sum(m5['Close'])/5, 1.05 * sum(m30['Close'])/30)
		current_percentage = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100
		high_percentage = ((cur_stats['High'] - prev_stats['Close'])/prev_stats['Close'])*100
		low_percentage = ((cur_stats['Low'] - prev_stats['Close'])/prev_stats['Close'])*100
		# info.append(f"{stock.ticker}: Current: ${cur_stats['Close']:.2f}, High: ${cur_stats['High']:.2f}, Low: ${cur_stats['Low']:.2f}"
		# 	+ '\n' + f"Current: {change_percentage:.2f}%" + '\n' + f"High: {((cur_stats['High'] - prev_stats['Close'])/prev_stats['Close'])*100:.2f}%" + '\n')

		print(f"{stock.ticker.upper()}: Current: ${cur_stats['Close']:.2f}, High: ${cur_stats['High']:.2f}, Low: ${cur_stats['Low']:.2f}"
			+ '\n' + f"Current: {current_percentage:.2f}%" + '\n' + f"High: {high_percentage:.2f}%" + '\n' + f'Low: {low_percentage:.2f}%' + '\n')


# Detect stocks crossing the 9 MA + RSI below 45. For 9 MA crossing, maybe wait for it to cross above and be greater than for one/two periods (sum(m2['Close']) > sum(m2['9_sma']))

def trending_stocks(portfolio, signals):
	"""The function will display the stock's ticker and relevant information when a pattern is detected"""
	"""I could potentially load the data 20-25s before displaying the stocks, would have to sleep() for less, and have a while 
	loop in the function. So you would still have the print function displaying the old data during processing. 
	Could make this easier by appending all of the strings that will be displayed. Then you can control when they are displayed.
	"""
	# Alerts if a stock triggers a variety of signals. The program displays both the ticker and the signal that was triggered.
	# stocks_to_display = [strftime('%I:%M:%S', localtime())]
	print(end='\n' * 2)
	print('Time ' + strftime('%I:%M:%S', localtime()))
	t1 = time()

	good_stocks = []

	# Maybe periodically update the hottest stocks (ten mins) 
	# Show new stocks that are hot rn (very recently percent_change increase)

	signal_list = []

	def detect_pennant(intra_day):
		first, second, third, last = intra_day.iloc[-48:-36], intra_day.iloc[-36:-24], intra_day.iloc[-24:-12], intra_day.iloc[-12:]
		deltas = [first.max()['High'] - first.min()['Low'], second.max()['High'] - second.min()['Low'], third.max()['High'] - third.min()['Low'], last.max()['High'] - last.min()['Low']]
		pattern = len([i for i in range(3) if deltas[i] > deltas[i+1]]) >= 2
		return pattern, deltas

	def spike_1ma():
		if m1.iloc[0]['Volume'] > (1.25 * sum(m15['Volume'])) and m1.iloc[0]['Close'] > (1.015 * sum(m15['Close'])):
			print(f'{stock.ticker}, Current Price: ${cur_stats["Close"]}, Current: {current_percentage:.2f}%, High: {high_percentage:.2f}%, Low: {low_percentage:.2f}%, 1m')
			good_stocks.append(stock)		

	def spike_2ma():
		if sum(m2['Volume']) > (1.25 * sum(m15['Volume'])) and sum(m2['Close']) > (1.015 * sum(m15['Close'])):
			print(f'{stock.ticker}, Current Price: ${cur_stats["Close"]}, Current: {current_percentage:.2f}%, High: {high_percentage:.2f}%, Low: {low_percentage:.2f}%, 2m')
			good_stocks.append(stock)

	def basing():
		basing = intra_day_stats[-50:].nsmallest(5, ['Low'])['Low'].sort_values(ascending=True)
		basing = [price for price in basing[1:] if basing[0]*1.01 >= price] 
		print('Basing: ', basing, stock.ticker)

	def cross_9ma():
		if m15.iloc[-3]['9_sma'] > m15.iloc[-3]['Close'] and m15.iloc[-2]['9_sma'] < m15.iloc[-2]['Close'] and m1.iloc[0]['9_sma'] < m1.iloc[0]['Close']:
			print(f'{stock.ticker}, Current Price: ${cur_stats["Close"]}, Current: {current_percentage:.2f}%, High: {high_percentage:.2f}%, Low: {low_percentage:.2f}%, 9_sma crossed and held')
			good_stocks.append(stock)		

	def double_bottom():
		# Double_bottom, maybe the values have to be 10 mins apart or more
		bottom = intra_day_stats[-50:].nsmallest(5, ['Low'])['Low'].sort_values(ascending=True)
		bottom = [price for price in bottom[1:] if bottom[0]*1.01 >= price] 
		print(stock.ticker, 'Bottom: ', bottom)		

	def double_top():
		top = intra_day_stats[-50:].nsmallest(10, ['Low'])['Low'].sort_values(ascending=False)
		top = [price for price in top[1:] if top[0] <= price*1.01]
		print(stock.ticker, 'Top: ', top)

	if '1ma' in signals:
		signal_list.append(spike_1ma)
	if '2ma' in signals:
		signal_list.append(spike_2ma)
	if '9ma_cross' in signals:
		signal_list.append(cross_9ma)
	if 'double_bottom' in signals:
		signal_list.append(double_bottom)
	if 'double_top' in signals:
		signal_list.append(double_top)
	if 'basing' in signals:
		signal_list.append(basing)

	print([func.__name__ for func in signal_list])
	print([(stock.ticker, stock.df) for stock in portfolio])

	for stock in portfolio:
		try:
			stock.update_stock()
			intra_day_stats = stock.df
			m1, m2, m15, m30 = intra_day_stats.iloc[-1:][['Volume', 'Close', '2_sma', '9_sma']], intra_day_stats.iloc[-2:][['Volume', 'Close', '2_sma', '9_sma']]/2, intra_day_stats.iloc[-15:][['Volume', 'Close', '2_sma', '9_sma']]/15, intra_day_stats.iloc[-30:][['Volume', 'Close', '2_sma', '9_sma']]/30
			cur_stats = stock.df_month.iloc[-1]
			prev_stats = stock.df_month.iloc[-2]
			current_percentage = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100
			high_percentage = ((cur_stats['High'] - prev_stats['Close'])/prev_stats['Close'])*100
			low_percentage = ((cur_stats['Low'] - prev_stats['Close'])/prev_stats['Close'])*100
		except:
			continue

		# Maybe detect a drop in value as well?
		# print('30 min high', stock.ticker, m30.max(), m30.idxmax())
		# print(m1['9_sma'])


		# if len(bottom) > 0:
		# 	print(f'{stock.ticker} bottom @ {bottom[0]}')

		# General uptrend: can track this through 50 SMA crossing 200 SMA/100

		# OR COULID DO PUT ALL OF THE DESIRED FUNCTIONS IN A LIST AND LOOP THROUGH THEM FOR EVERY STOCK. CHOOSE WHICH FUNCTIONS
		# BY DOING THIS IF STATEMENT AT THE START 
		if cur_stats['Volume'] > 100_000:
			for signal in signal_list:
				signal()
			

	print(f'Computing time: {time() - t1:.2f}s. Average of {len(portfolio)/(time() - t1):.2f} stocks per second.')	

	return good_stocks

