import pytrading
import mplfinance as mpf
import pandas as pd

pd.set_option('display.max_columns', None)

# Venv commands
# Run .\pytradingenv\scripts\activate.bat to activate venv
# deactivate
# pip install -r requirements.txt
# pip freeze

# I will be rich with Spac + Ev + Biotech + Ziptrader + Data analysis companies + ML trading
stocks = pytrading.Portfolio(['PLTR', 'CCIV', 'NPA'])

mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

def graph_stocks(stocks):
	for stock in stocks:
		df = stock.get_month_data(num=2)
		mpf.plot(df, style=s, title=f'${stock.ticker}', type='candle', mav=(2, 9), volume=True)
		# fig, ax = mpf.plot(df, style=s, title=f'${stock.ticker}', type='candle', mav=(2, 9), volume=True, returnfig=True)
		# ax.plot(x, np.sin(x), '-b', label='Sine')
		# ax.plot(x, np.cos(x), '--r', label='Cosine')
		# ax.axis('equal')
		# leg = ax.legend();

# graph_stocks(stocks)
# Goal: read stocks from Excel spreadsheet.
print(pd.read_excel(r'C:\Users\JWcam\Desktop\STONKS.xlsx'))	
