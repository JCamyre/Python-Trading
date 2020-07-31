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


def pennant(intra_day):
	first, second, third, last = intra_day.iloc[-48:-36], intra_day.iloc[-36:-24], intra_day.iloc[-24:-12], intra_day.iloc[-12:]
	deltas = [first.max()['High'] - first.min()['Low'], second.max()['High'] - second.min()['Low'], third.max()['High'] - third.min()['Low'], last.max()['High'] - last.min()['Low']]
	pattern = len([i for i in range(3) if deltas[i] > deltas[i+1]]) >= 2
	return pattern, deltas


def stock_tracker(portfolio):
	t1 = time()
	info = [f"Time: {strftime('%I:%M:%S', localtime())}"]
	for stock in portfolio:

		# alert_sound() Do sound if within 5% of price target. Or do it if stock up 10% from price you bought it at. 
		stock.update_stock()
		cur_stats = stock.df_month.iloc[-1]
		prev_stats = stock.df_month.iloc[-2]
		intra_day_stats = stock.df
		m1, m5, m15, m30 = intra_day_stats.iloc[-1:][['Volume', 'Close']], intra_day_stats.iloc[-5:][['Volume', 'Close']]/5, intra_day_stats.iloc[-15:][['Volume', 'Close']]/5, intra_day_stats.iloc[-30:][['Volume', 'Close']]/5
		delta_volume = cur_stats['Volume']/sum(stock.df_month.iloc[-30:]['Volume'])
		
		print(sum(m5['Volume'])/5, 1.25 * sum(m30['Volume'])/30, sum(m5['Close'])/5, 1.05 * sum(m30['Close'])/30)
		change_percentage = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100 

		info.append(f"{stock.ticker}: Current: ${cur_stats['Close']:.2f}, High: ${cur_stats['High']:.2f}, Low: ${cur_stats['Low']:.2f}"
			+ '\n' + f"Current: {change_percentage:.2f}%" + '\n' + f"High: {((cur_stats['High'] - prev_stats['Close'])/prev_stats['Close'])*100:.2f}%" + '\n')

	print(f'Computing time: {time() - t1:.2f}s')
	return info

weekly_tickers = ['IVV','SPY','BDX','DIA','LH','IJH','PH','GLD','SAP','MMM','QLD','LLY','MTUM','LQD','EBON','BSIG','AMKR','TSM','OSTK','MFG','SPWR','BVN','SOXL','LTRPA','KLIC','MELI','CSIQ','BBD','ANH','CWH','CC','NVCN','GSX','LL','SID','ABEV','SE','CX','LSCC','SCCO','ACCD','MDLA','PS','ELY','SEM','BRZU','ARAY','ALXN','JKS','PDD','FTCH','ICHR','STNE','SEDG','CHNG','AVTR','GT','GPRO','DDD','PAYS','ATHM','IOVA','BCC','AA','BIIB','FLEX','LPX','BECN','NAVI','SHOP','INVA','REGN','FOLD','KLAC','NET','ETSY','EDC','CRON','MDRX','FBHS','GLW','SDC','LEN','PKI','PD','STM','JELD','SPWH','MAXR','KBH','PHM','DHI','LW','EBAY','ON','CRWD','ANET','GGB','QCOM','CCC','SMTC','LITE','ST','CIEN','SMH','DDOG','RYN','AMAT','ASML','NOK','GRMN','TAL','IFRX','MTOR','PSEC','CLF','LEG','MAS','SQ','PMT','BHP','NXPI','AN','CVA','EWZ','BBL','LRCX','FDX','LBTYA','GDOT','NFLX','CNQ','SWK','CCJ','HAIN','MU','ROKU','GKOS','GRUB','BGS','DKS','LBRT','LBTYK','RIO','FCX','OI','BRKR','JD','BILI','DOCU','XHB','PTON','STOR','INTU','YNDX','ADI','ERIC','GMED','CRMD','SOXX','CTB','AYX','OC','MS','INFN','ALC','AXL','SNE','RPRX','GLNG','IRDM','MXIM','NTR','ARNA','GNTX','IBB','IQV','LULU','AKAM','CDNS','NKTR','CREE','HCAT','PHG','RH','EWW','MHK','HPQ','NUE','PLAN','DLR','CTSH','MRK','NOW','INFY','EQIX','MNST','JNPR','PBR','EMN','ICPT','AAPL','CSTM','ALV','OLLI','MBT','ACC','REGI','JHG','CPRX','BOTZ','CRUS','SNAP','SRC','ANGI','ATVI','PM','NVDA','FMX','CDK','OSK','GNRC','HP','LEA','PRGO','SPG','BKI','BR','KC','STLD','CG','CPRT','LXP']

# Detect stocks crossing the 9 MA + RSI below 45. For 9 MA crossing, maybe wait for it to cross above and be greater than for one/two periods (sum(m2['Close']) > sum(m2['9_sma']))

def trending_stocks(portfolio):
	# Alerts if a stock triggers a variety of signals. The program displays both the ticker and the signal that was triggered.
	# stocks_to_display = [strftime('%I:%M:%S', localtime())]
	print('Time ' + strftime('%I:%M:%S', localtime()))
	t1 = time()
	for stock in portfolio:
		stock.update_stock()
		intra_day_stats = stock.df
		try:
			cur_stats = stock.df_month.iloc[-1]
			m1, m2, m15, m30 = intra_day_stats.iloc[-1:][['Volume', 'Close', '2_sma', '9_sma']], intra_day_stats.iloc[-2:][['Volume', 'Close', '2_sma', '9_sma']]/2, intra_day_stats.iloc[-15:][['Volume', 'Close', '2_sma', '9_sma']]/15, intra_day_stats.iloc[-30:][['Volume', 'Close', '2_sma', '9_sma']]/30
			# Since I don't care about volume rn
			# m1, m2, m15, m30 = intra_day_stats.iloc[-2:-1][['Volume', 'Close', '2_sma', '9_sma']], intra_day_stats.iloc[-3:-1][['Volume', 'Close', '2_sma', '9_sma']]/2, intra_day_stats.iloc[-16:-1][['Volume', 'Close', '2_sma', '9_sma']]/15, intra_day_stats.iloc[-31:-1][['Volume', 'Close', '2_sma', '9_sma']]/30
		except:
			continue
		# Maybe detect a drop in value as well?
		# print('30 min high', stock.ticker, m30.max(), m30.idxmax())
		# print(m1['9_sma'])

		# Don't care about (and cur_stats['Volume'] > 100_000) for now 
		# Need a better system for encompassing the most amount of stocks that may move

		# Double_bottom
		bottom = intra_day_stats[-50:].nsmallest(5, ['Low'])['Low'].sort_values(ascending=True)
		bottom = [price for price in bottom[1:] if bottom[0]*1.01 >= price]
		if len(bottom) > 0:
			print(f'{stock.ticker} bottoming @ {bottom[0]}')

		# Double_top
		top = intra_day_stats[-50:].nsmallest(10, ['Low'])['Low'].sort_values(ascending=False)
		top = [price for price in top[1:] if top[0] <= price*1.01]

		pennant = pennant(intra_day_stats)


		# if m15.iloc[-2]['2_sma'] < m15.iloc[-2]['Close'] and sum(m2['2_sma']) > sum(m2['Close']):
		# 	print(stock.ticker + ' will prob go lower.')
		if cur_stats['Volume'] > 100_000:
			if m15.iloc[-3]['9_sma'] > m15.iloc[-3]['Close'] and m15.iloc[-2]['9_sma'] < m15.iloc[-2]['Close'] and m1.iloc[0]['9_sma'] < m1.iloc[0]['Close']:
				print(stock.ticker + ' 9_sma crossed and held')
			if sum(m2['Volume']) > (1.25 * sum(m15['Volume'])) and sum(m2['Close']) > (1.015 * sum(m15['Close'])):
				print(stock.ticker + ' 2m')
			elif m1.iloc[0]['Volume'] > (1.25 * sum(m15['Volume'])) and m1.iloc[0]['Close'] > (1.015 * sum(m15['Close'])):
				print(stock.ticker + ' 1m')


	print(f'Computing time: {time() - t1:.2f}s. Average of {len(portfolio)/(time() - t1):.2f} stocks per second.')	
	# return stocks_to_display


