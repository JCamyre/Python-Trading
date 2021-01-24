import pytrading
import mplfinance as mpf

# I will be rich with Spac + Ev + Biotech + Ziptrader + Data analysis companies + ML trading
stocks = pytrading.Portfolio(['PLTR', 'CCIV', 'NPA'], interval='1d', period='1m')
for stock in stocks:
	df = stock.get_month_data()
	print(type(df.index[0]))
	mpf.plot(df, type='candle', style='charles', mav=(2, 9))
	
