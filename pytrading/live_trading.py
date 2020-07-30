import pandas as pd
import requests
import pickle
from requests import get 
from bs4 import BeautifulSoup
from time import sleep, strftime, localtime, time
from datetime import date, datetime
# This importing technique only works when you are importing pytrading.live_trading from outside of the package
from . import Portfolio

import yfinance as yf 
# from pygame import mixer 

# At the start of the day, get the top earners of the day, pickle it, and keep running the searching thing every 90 seconds (meaning time.sleep(15))

# mixer.init()

pd.options.display.max_rows = 1200
pd.options.display.max_columns = 10

# Stocks under two billion market cap, low float

my_stocks = ['AGI', 'AMAT', 'AYRO', 'BIDU', 'BILI', 'BILL', 'JBLU', 'JD', 'KHC', 'LUV', 'QD', 'RGR', 'SWBI', 'TSM', 'VIPS']

# with open('literally_all_tickers', 'rb') as f:
# 	tickers_to_check = pickle.load(f)

def alert_sound():
	regular_instrumental = mixer.music.load("C:/Users/JWcam/Desktop/NCT 127 - Regular (Instrumental).mp3")
	mixer.music.set_volume(0.7)
	mixer.music.play()
	sleep(6.85)
	mixer.music.stop()


'''Getting premarket movers -> reading charts -> getting list of 5-10 interesting stocks -> drawing/writing SR levels -> strategies with 
enter/exit prices -> be dynamic, sometimes things do not go to plan (breakout or plummet) -> stop losses

If a stock goes through resistance, but falls back on resistance can be either acting as support or could just fall through'''

# Get low float stocks. High short interest
# Look for super basing penny stocks/RSI low
# Day 3/4 Penny stocks



def stock_tracker(portfolio):
	# iNSTEAD OF SEARCHING FOR ALL STOCKS FOR THE MID DAY MOVERS, JUST TAKE ALL STOCKS UP MORE THAN A COUPLE PERCENT WITH SOME EITHER PENNY STOCK CRITERIA, THEN JUST SEARCH THROUGH THOSE
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

# Detect stocks crossing the 9 MA + RSI below 45

def trending_stocks(portfolio):
	stocks_to_display = [strftime('%I:%M:%S', localtime())]
	t1 = time()
	for stock in portfolio:
		stock.update_stock()

		# try:
		# 	cur_stats = stock.df_month.iloc[-1]
		# 	prev_stats = stock.df_month.iloc[-2]
		# except:
		# 	print(stock.ticker, 'this one bad.')
		# 	continue

		intra_day_stats = stock.df
		m1, m2, m15, m30 = intra_day_stats.iloc[-2:-1][['Volume', 'Close']], intra_day_stats.iloc[-3:-1][['Volume', 'Close']]/2, intra_day_stats.iloc[-16:-1][['Volume', 'Close']]/15, intra_day_stats.iloc[-31:-1][['Volume', 'Close']]/30
		
		# delta_volume = cur_stats['Volume']/sum(stock.df_month.iloc[-30:]['Volume'])
		# change_percentage = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100 

		# and delta_volume > 1.25 Is this needed?
		# Maybe detect a drop in value as well?
		# Maybe drop one minute volume/close
		if m2['9_sma'] < sum(m2['close']) or sum(m2['Volume']) > (1.25 * sum(m15['Volume'])) and sum(m2['Close']) > (1.015 * sum(m15['Close'])) and cur_stats['Volume'] > 100_000:
			stocks_to_display.append(stock.ticker + ' 2m')
		elif m1['9_sma'] < sum(m1['close']) or sum(m1['Volume']) > (1.25 * sum(m15['Volume'])) and sum(m1['Close']) > (1.015 * sum(m15['Close'])) and cur_stats['Volume'] > 100_000:
			stocks_to_display.append(stock.ticker + ' 1m')
	print(f'Computing time: {time() - t1:.2f}s. Average of {len(portfolio)/(time() - t1):.2f} stocks per second.')	
	return stocks_to_display

# def trending_stocks(portfolio, repeat=False):
# 	def return_trending_stocks(portfolio):
# 		stocks_to_display = []
# 		t1 = time()
# 		for stock in portfolio:
# 			stock.update_stock()

# 			try:
# 				cur_stats = stock.df_month.iloc[-1]
# 				prev_stats = stock.df_month.iloc[-2]
# 			except:
# 				print(stock.ticker, 'this one bad.')
# 				continue

# 			intra_day_stats = stock.df
# 			m1, m3, m15, m30 = intra_day_stats.iloc[-2:-1][['Volume', 'Close']], intra_day_stats.iloc[-4:-1][['Volume', 'Close']]/3, intra_day_stats.iloc[-16:-1][['Volume', 'Close']]/15, intra_day_stats.iloc[-31:-1][['Volume', 'Close']]/30
			
# 			delta_volume = cur_stats['Volume']/sum(stock.df_month.iloc[-30:]['Volume'])
# 			change_percentage = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100 

# 			# and delta_volume > 1.25 Is this needed?
# 			# Maybe detect a drop in value as well?
# 			if sum(m3['Volume']) > (1.25 * sum(m15['Volume'])) or sum(m3['Close']) > (1.02 * sum(m15['Close'])) and cur_stats['Volume'] > 100_000:
# 				stocks_to_display.append(stock.ticker)

# 		print(f'Computing time: {time() - t1:.2f}s. Average of {len(portfolio)/(time() - t1):.2f} stocks per second.')	

# 	if repeat:
# 		try:
# 			while True:
# 				return_trending_stocks(portfolio)
# 		except KeyboardInterrupt:
# 			pass
# 	else:
# 		return_trending_stocks(portfolio)

def intraday_stocks():
	try:
		while True:
			print(f"Time: {strftime('%I:%M:%S', localtime())}", end='\n' * 2)
			stock_tracker(day_tickers)
			sleep(20)
	except KeyboardInterrupt:
		pass

# BUY SOME AT 10, 11, 12, SELL SOME AT 15, BUY SOME AT 13 14 15, SELL SOME AT 18, ....
# Buying trending stocks a few days later, if the chart looks constructive and with support. Has to drop a lot hto.
# Ascending/descending triangle. Ascending: High lows, fighting resistance level, breakout. Descending: Lower highs, fighting support level, drop.
# Stop loss 1 ATR? Low float stocks
