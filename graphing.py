import pytrading
import mplfinance as mpf

# I will be rich with Spac + Ev + Biotech + Ziptrader + Data analysis companies + ML trading
stocks = pytrading.Portfolio(['PLTR', 'CCIV', 'NPA'], interval='1d', period='1m')

mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

for stock in stocks:
	df = stock.get_month_data()
	print(type(df.index[0]))
	mpf.plot(df, style=s, title=f'${stock.ticker}', type='candle', mav=(2, 9), volume=True)
	
