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
stocks = pytrading.Portfolio(['NNDM', 'CCIV'])

mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

def graph_stocks(stocks, lines=None): # lines: pass an array of lists with support line values
	for i, stock in enumerate(stocks):
		df = stock.get_month_data(num=2)
		# I would like to add multiple support/resistance lines. 
		df['support'] = lines[i][0]
		apdict = mpf.make_addplot(df['support'])
		mpf.plot(df, style=s, title=f'${stock.ticker}', type='candle', mav=(2, 9), volume=True, addplot=apdict)
		# fig, ax = mpf.plot(df, style=s, title=f'${stock.ticker}', type='candle', mav=(2, 9), volume=True, returnfig=True)
		# ax.plot(x, np.sin(x), '-b', label='Sine')
		# ax.plot(x, np.cos(x), '--r', label='Cosine')
		# ax.axis('equal')
		# leg = ax.legend();

graph_stocks(stocks, lines=[[20, 17.50], [15, 13, 11.5]])

def read_stock_excel(file):
	for index, row in pd.read_excel(file).iterrows():
		print(f'${row["Ticker"]}, {row["Price Targets"]}, {row["Catalyst Dates"]}')

# read_stock_excel(r'C:\Users\JWcam\Desktop\STONKS.xlsx')
