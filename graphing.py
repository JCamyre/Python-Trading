import pytrading
import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import regex as re

pd.set_option('display.max_columns', None)

# Venv commands
# Run ".\pytradingenv\scripts\activate.bat" to activate venv
# deactivate
# pip install -r requirements.txt
# pip freeze

stocks = pytrading.Portfolio(['NNDM', 'CCIV'])

mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

def graph_stocks(stocks, lines=None): # lines: pass an array of lists with support line values
	for i, stock in enumerate(stocks):
		df = stock.get_month_data(num=2)
		# I would like to add multiple support/resistance lines. 
		df['support'] = lines[i][0]
		# apdict = mpf.make_addplot(df['support'])
		fig1, ax = plt.subplots()
		ax.scatter(df.index, df['support'], Label='Support 1')
		fig1.suptitle('yo1')
		fig2, volume = plt.subplots()
		volume.scatter(df.index, df['Volume'], Label='Volume')
		fig2.suptitle('yo2')
		print(df)
		# ax.axis('equal')
		# leg = ax.legend();
		mpf.plot(df, style=s, title=f'${stock.ticker}', type='candle', mav=(2, 9), volume=volume, ax=ax)

# graph_stocks(stocks, lines=[[20, 17.50], [15, 13, 11.5]])

def read_stock_excel(file):
	for index, row in pd.read_excel(file).iterrows():
		print(f'${row["Ticker"]}, {row["Price Targets"]}, {row["Catalyst Dates"]}')

# read_stock_excel(r'C:\Users\JWcam\Desktop\STONKS.xlsx')

def find_match(pattern, words):
	match = pattern.search(words)
	return match

def get_fda_calendar(textfile):
	# Unfortunately can not scrape data from website, so I copied the plain text manually.
	# Logic: All companies after a date, and before a new one, belong to the aforementioned date.
	date = re.compile(r'\w{3,6}day, \w{3,9}\s\d{1,2}') # Finds all dates in text using pattern
	testing = dict()
	with open(textfile, 'r') as f:
		lines = f.read().split('\n')
		cur_date = lines[0]
		for line in lines:
			yo = find_match(date, line)
			if yo:
				cur_date = yo.group(0)
				testing[cur_date] = []
			elif line != ' ':
				testing[cur_date].append(line)
	return testing

dates = get_fda_calendar('FDACalendar.txt')
for date, companies in dates.items():
	print(date, companies)

