from datetime import date, datetime
from .base import Ticker
import pandas as pd 
from requests import get
from bs4 import BeautifulSoup
import re
from GoogleNews import GoogleNews
from dotenv import load_dotenv
import os 
import tweepy 

class Portfolio:
	# Maybe do a DataFrame? Easier to display, can sort. Columns for tickers, change_percentage, last_updated_price
	# Pass in stocks with their target values, like this: (stock, target_prices)
	def __init__(self, stocks, interval='1m', period='1d'):
		# if type(stocks) == tuple:
		# 	self.stocks = stocks[0]

		# if type(stocks[0]) != str:
		# 	while stocks[0] != str:
		# 		stocks = stocks[0]
		# 		print(stocks)
		if type(stocks) == list:
			self.stocks = {Stock(stock, interval=interval, period=period) for stock in sorted(stocks)}
		else:
			self.stocks = {Stock(stock, interval=interval, period=period) for stock in sorted(stocks.split())}	

	def add_stocks(self, stocks):
		for stock in stocks.split():
			self.stocks.add(stock)

	def clean_stocks(self):
		for stock in self.stocks:
			if 'trash' in stock.ticker:
				self.stocks.remove(stock)

	def get_biggest_movers(self):
		print("These are today's biggest movers: ")
		for stock in self.stocks:
			if stock.daily_change_percentage > 10.0:
				print(stock.ticker)

	def get_highest_rel_volume(self):
		print("These are today's most relatively active stocks: ")
		for stock in self.stocks:
			if stock.get_relative_volume() > 3.0:
				print(stock.ticker)
		# return [stock.ticker for stock in self.stocks if stock.get_relative_volume() > 3.0]

	def get_stocks(self):
		return sorted([(stock.ticker, stock.daily_stats(), stock.daily_change_percentage()) for stock in self.stocks], key=lambda x: x[0])

	def get_stocks_daily(self): # Fix
		return [stock.df_month for stock in self.stocks]

	def get_stocks_intra(self):
		return [stock.df for stock in self.stocks]

	def sort_by(self, sort='name'):
		if sort == 'name':
			pass
		elif sort == 'change_percentage':
			pass
		elif sort == 'price':
			pass
		else:
			raise Exception('Please enter one of the following sorting methods: name, price, or change_percentage')

	def update_price_change(self):
		print("These stocks' prices have changed significantly.")
		for stock in self.stocks:
			if (stock.df.iloc[0]['Close'] - stock.get_last_updated())/(stock.get_last_updated())*100 > 5.0:
				stock.set_last_updated(stock.df.iloc[0]['Close'])
				print(stock.ticker)

	def __iter__(self):
		return iter(self.stocks)

	def __getitem__(self, i):
		return self.stocks[i]

	def __len__(self):
		return len(self.stocks)

	def __repr__(self):
		return 'A portfolio of #winning stocks.'

class Stock:

	def __init__(self, ticker, interval='1m', period='1d', target_prices=None, price_invested=None):
		self.ticker = ticker
		self.df = Ticker(ticker).get_data(interval, period)
		self.prev_close = Ticker(ticker).get_data('1d', '2d').iloc[0]['Close']
		try:
			self._last_updated_price = self.df.iloc[-1]['Close']
		except:
			pass
		self.target_prices = target_prices
		self.price_invested = price_invested

	def get_month_data(self, num=1):
		df = Ticker(self.ticker).get_data('1d', f'{num}mo')
		df.index = pd.to_datetime(df.index)
		return df

	def add_target_prices(self, new_target_prices):
		self.target_prices = new_target_prices

	def daily_change_percentage(self):
		return ((self.df.iloc[-1]['Close'] - self.df.iloc[-2]['Close'])/self.df.iloc[-2]['Close'])*100

	def daily_high_change_percentage(self):
		return ((self.df.iloc[-1]['High'] - self.df.iloc[-2]['Close'])/self.df.iloc[-2]['Close'])*100

	def daily_stats(self):
		df = Ticker(self.ticker).get_data('1d', '1d')
		df.index = pd.to_datetime(df.index)		
		return self.df.iloc[-1]['Close'], self.df.iloc[-1]['High'], self.df.iloc[-1]['Low']

	def get_relative_volume(self):
		avg_volume = sum(self.df['Volume'])/len(self.df)
		return self.df.iloc[-1]/avg_volume

	def get_last_updated(self):
		return self._last_updated_price

	def set_last_updated(self, price):
		self._last_updated_price = price

	def update_stock(self):
		self.df = get_intra_day_data(self.ticker)
		self.df_month = get_month_data(self.ticker)

	def due_diligence(self):
		'''
		All of the functions I created for doing due diligence on a stock.
		''' 

		# Code reuse

		def _find_match(pattern, text):
			match = pattern.search(text)
			return match

		def _no_attributes(tag):
			if 'td' in str(tag):
				return tag.has_attr('class') or tag.has_attr('id')

		def _get_soup(url):
			response = get(url, headers=HEADERS, timeout=20)
			assert response.status_code == 200
			return BeautifulSoup(response.content, 'lxml')


		HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) AppleWebKit/537.36 " # Telling the website what browser I am "using"
									"(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}

		# Make this all one big function
		def _get_summary(ticker):
			BASE_URL = f'https://www.marketwatch.com/investing/stock/{ticker}'
			soup = _get_soup(BASE_URL)

			summary = soup.find('p', {'class': 'description__text'})

			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
			soup = _get_soup(BASE_URL)
			website = soup.find('a', {'title': 'Company Profile'})
			if website:
				website = website['href']

			return summary.get_text(), website


			# Find the website of the stock and go to its information page

		def _basic_stats(ticker):
			# Market cap, avg volume, price, chart, 
			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
			soup = _get_soup(BASE_URL)

			info = []

			with open('output1.html', 'w', encoding='utf-8') as file:
				file.write(str(soup))

			# Financial highlights
			div = soup.find('div', {'class': 'Mb(10px) Pend(20px) smartphone_Pend(0px)'})
			info.append([(i.find('h3', {'class': 'Mt(20px)'}), i.find('tbody').find_all('tr')) for i in div.find_all('div', {'class': 'Pos(r) Mt(10px)'})])

			# Trading Information
			div = soup.find('div', {'class': 'Pstart(20px) smartphone_Pstart(0px)'})
			info.append([(i.find('h3', {'class': 'Mt(20px)'}), i.find('tbody').find_all('tr')) for i in div.find_all('div', {'class': 'Pos(r) Mt(10px)'})])

			# Income Statement
			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
			soup = _get_soup(BASE_URL)

			# Balance Sheet
			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
			soup = _get_soup(BASE_URL)
			
			return info

		def _price_target(self, exchange='NASDAQ'): # Automatically find correct stock exchange
			BASE_URL = ''
			soup = _get_soup(BASE_URL)
			table = soup.find('table', {'class': "scroll-table"})
			# price_target = soup.find('table', {'class': 'scroll-table'})
			_pattern = re.compile(r'Price Target: \$\d{1,3}\.\d\d')
			price_target = _find_match(_pattern, table.get_text()).group(0)
			_pattern = re.compile(r'\d{1,3}\.\d\d\% \w{6,8}')
			percentage = _find_match(_pattern, table.get_text()).group(0)

			BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
			response = get(BASE_URL, headers=HEADERS, timeout=20)
			soup = BeautifulSoup(response.content, 'lxml')
			table = soup.find('table', {'class': "fullview-ratings-outer"})
			rows = table.find_all('td', {'class': 'fullview-ratings-inner'})
			df_data = []
			for row in rows:
				row = row.find_all('td')
				date, _, fund, action, pricetarget = [val.get_text() for val in row]
				date = datetime.strptime(date, '%b-%d-%y')
				df_data.append((date, fund, action, pricetarget))

			analyst_price_targets = pd.DataFrame(df_data, columns=['Date', 'Fund', 'Action', 'PriceTarget'])
			analyst_price_targets = analyst_price_targets.set_index('Date')
			return price_target, percentage, analyst_price_targets

		def _price_predictions(ticker):
			BASE_URL = f'https://www.barchart.com/stocks/quotes/{ticker}/opinion'
			soup = _get_soup(BASE_URL)

			table = soup.find('table', {'data-ng-class': "{'hide': currentView !== 'strengthDirection'}"})
			titles = soup.find_all('tr', {'class': 'indicator-title'})
			titles = [i.get_text() for i in titles]

			data = soup.find_all('tr', {'class': 'indicator-item'})
			data = [i.get_text() for i in data]
			data = data[len(data)//2 + 1:]
			df_data = []
			for i in data:
				signal, strength, direction = i.split()[-3:]
				indictator = ' '.join(i.split()[:-3])
				df_data.append((indictator, signal, strength, direction))
			df = pd.DataFrame(df_data, columns=['Indictator', 'Signal', 'Strength', 'Direction'])
			return df

		def _ta_indictators(self, exchange='NASDAQ'): # Loads wrong page. Beta, RSI history, above/below 9 SMA, above/below 180 SMA, volatility, rel volume
			BASE_URL = f'https://www.tradingview.com/symbols/{exchange}-{ticker}/technicals/'
			soup = _get_soup(BASE_URL)

			# Buy or sell (Summary, Oscillators, Moving Averages)
			s = soup.find_all('div', {'class': 'speedometerWrapper-1SNrYKXY'})
			
			# Oscillators
			oscillators = soup.find('div', {'class': 'container-2w8ThMcC tableWithAction-2OCRQQ8y'})
			# with open('output1.html', 'w', encoding='utf-8') as file:
			# 	file.write(str(soup.prettify('utf-8')))


		def _news_sentiments(ticker): # Returns news articles curated via Finviz, Yahoo, and Google News, GET UNUSUAL OPTION ACTIVITY
			BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
			soup = _get_soup(BASE_URL)

			table = soup.find('table', {'class': 'fullview-news-outer'})
			rows = table.find_all('tr')
			df_data = []
			for row in rows:
				date = row.find('td', {'align': 'right'})
				article = row.find('td', {'align': 'left'})
				link = article.find('a')['href']
				df_data.append((date.get_text(), article.get_text(), link))
			df = pd.DataFrame(df_data, columns=['Time', 'Headline', 'Link'])

			# Getting news from google news search
			googlenews = GoogleNews(lang='en', period='14d') # Specify period for news
			googlenews.self.search(ticker) 
			# print([(i, j) for i, j in zip(googlenews.get_texts(), googlenews.get_links())])
			# To get other pages, do googlenews.get_page(2), etc.

			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/news?p={ticker}'
			soup = _get_soup(BASE_URL)

			links = soup.find_all('a', {'class': 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'})
			news = [(link.get_text(), str('yahoo.com' + link['href'])) for link in links]

			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/press-releases?p={ticker}'
			soup = _get_soup(BASE_URL)

			links = soup.find_all('a', {'class': 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'})
			press_releases = [(link.get_text(), str('yahoo.com' + link['href'])) for link in links]
			# Look for keywords in the news? Any showcases, Investor/analyst days, Analyst revisions, Management transitions
			# Product launches, Significant stock buyback changes

			return df, news, press_releases

		def _financials(ticker): # OMEGALUL
			# Displaying all information. Could leave this as a dictionary.
			BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
			soup = _get_soup(BASE_URL)
			table = soup.find('table', {'class': 'snapshot-table2'})
			labels = table.find_all('td', {'class': 'snapshot-td2-cp'})
			values = table.find_all('td', {'class': 'snapshot-td2'})
			info_dict = {}
			for label, val in zip(labels, values):
				info_dict[str(label.get_text())] = str(val.get_text()) 
			df = pd.DataFrame(info_dict.items(), columns={'Label', 'Value'})

			# yo
			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
			soup = _get_soup(BASE_URL)

			# PE/G, market cap, profit margin, idk what else is important
			div = soup.find('div', {'id': 'quote-summary'})
			return df, 'Avg. Volume: ' + div.find('span', {'data-reactid': '48'}).get_text(), 'Market Cap: ' + div.find('span', {'data-reactid': '56'}).get_text(), 
			'Beta (5Y Monthly): ' + div.find('span', {'data-reactid': '61'}).get_text(), 'PE Ratio (TTM): ' + div.find('span', {'data-reactid': '66'}).get_text()

		def _short_selling(ticker):
			'''
			Returns a stocks short_selling information
			'''
			BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
			soup = _get_soup(BASE_URL)

			labels = soup.find_all('td', {'class': 'snapshot-td2-cp'})
			values = soup.find_all('td', {'class': 'snapshot-td2'})
			return labels[16].get_text(), values[16].get_text(), labels[22].get_text(), values[22].get_text()


		def _put_call_ratio(ticker): 
			'''
			Returns various information regarding the put call ratio of a stock.
			'''
			BASE_URL = f'https://www.alphaquery.com/stock/{ticker}/volatility-option-statistics/120-day/put-call-ratio-oi'
			soup = _get_soup(BASE_URL)

			ratio_volume = soup.find('tr', {'id': 'indicator-put-call-ratio-volume'})
			ratio_open_interest = soup.find('tr', {'id': 'indicator-put-call-ratio-oi'})
			forward_price = soup.find('tr', {'id': 'indicator-forward-price'})
			call_breakeven_price = soup.find('tr', {'id': 'indicator-call-breakeven'})
			put_breakeven_price = soup.find('tr', {'id': 'indicator-put-breakeven'})
			option_breakeven_price = soup.find('tr', {'id': 'indicator-option-breakeven'})

			return ratio_volume, ratio_open_interest, forward_price, call_breakeven_price, put_breakeven_price, option_breakeven_price

		def _find_competition(ticker):
			BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
			soup = _get_soup(BASE_URL)

			td = soup.find_all('td', {'class': 'fullview-links'})[1]
			sectors = td.find_all('a', {'class': 'tab-link'})
			sector_urls = ([str('https://finviz.com/' + i['href']) for i in sectors])
			for i in sector_urls: # Find stocks with similar P/E ratios and market cap, then track difference in performance
				pass

		def _etfs(ticker):
			BASE_URL = f'https://etfdb.com/stock/{ticker}/'
			soup = _get_soup(BASE_URL)
			tbody = soup.find('tbody')
			rows = tbody.find_all('tr')
			rows = [[i.get_text() for i in row.find_all('td')] for row in rows]
			train_df = pd.DataFrame(rows, columns={'Ticker', 'ETF', 'ETF Category', 'Expense Ratio', 'Weighting'})
			return train_df

		def _insider_trading(ticker):
			BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
			soup = _get_soup(BASE_URL)

			tr = soup.find_all('tr', {'class': "insider-sale-row-2"})
			return [i.get_text() for i in tr]

		def _social_media_sentiment(ticker, num_of_tweets=50): # Also reddit sentiment, and twitter
			# Twitter
			load_dotenv()
			consumer_key = os.getenv('API_KEY')
			consumer_secret = os.getenv('API_SECRET_KEY')
			auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
			api = tweepy.API(auth, wait_on_rate_limit=True)
			tweets = []
			for i, tweet in enumerate(tweepy.Cursor(api.search, q=f'${ticker}', count=num_of_tweets).items(num_of_tweets)):
				tweets.append(i, tweet.text, tweet.author.screen_name, tweet.retweet_count, tweet.favorite_count, tweet.created_at)
			return tweets

		def _catalysts(ticker): # Returns date of showcases, FDA approvals, earnings, etc
			df_data = []
			# Earnings date: 
			BASE_URL = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
			soup = _get_soup(BASE_URL)
			
			# Convert to datetime
			earnings_date = soup.find('td', {'data-test': 'EARNINGS_DATE-value'})
			earnings_date = f'Next earnings date: {earnings_date.get_text()}'

			# FDA approvals
			BASE_URL = 'https://www.rttnews.com/corpinfo/fdacalendar.aspx'
			soup = _get_soup(BASE_URL)

			# company = soup.find_all('div', {'data-th': 'Company Name'})
			# print(company[0].get_text())

			# events = soup.find_all('div', {'data-th': 'Event'})
			# print(events[0].get_text())

			# outcome = soup.find_all('div', {'data-th': 'Outcome'})
			# if outcome[0]:
			# 	print(outcome[0].get_text())

			# dates = soup.find_all('span', {'class': 'evntDate'})
			# print([date.get_text() for date in dates])

			for i in range(len(company)):
				if outcome[i]:
					if not len(dates[i].split()) > 1:
						date = datetime.strptime(dates[i].get_text(), '%m/%d/%Y')
					else:
						date = datetime.strptime(dates[i].split()[1:].get_text(), '%b %Y')

					df_data.append([date, company[i].get_text(), events[i].get_text(), outcome[i].get_text()])
				else:
					df_data.append([company[i].get_text(), events[i].get_text(), outcome[i]])

			# FDA trials
			df = pd.DataFrame(df_data, columns=['Date', 'Company Name', 'Event', 'Outcome'])
			# ?PageNum=4 to ?PageNum=1
			return df

		def _big_money(ticker): # Returns recent institutional investments in a stock, as well as the largest shareholders and mutual funds holding the stock
			BASE_URL = f'https://money.cnn.com/quote/shareholders/shareholders.html?symb={ticker}&subView=institutional'
			soup = _get_soup(BASE_URL)

			# Latest institutional activity
			# df_recent_activity = []
			# table = soup.find('table', {'class', 'wsod_dataTable wsod_dataTableBig'})
			# rows = table.find_all('tr')
			# for row in rows:
			# 	date = row.find('td', {'class': 'wsod_activityDate'})
			# 	info = row.find('td', {'class': 'wsod_activityDetail'})
			# 	df_recent_activity.append([date.get_text(), info.get_text()]) # Could make a data frame

			# Top 10 Owners of self.{Ticker}
			df_data = []
			table = soup.find('table', {'class': 'wsod_dataTable wsod_dataTableBig wsod_institutionalTop10'})
			rows = table.find_all('tr')[1:]
			for row in rows:
				data = row.find_all('td')
				df_data.append([i.get_text() for i in data])

			owners_df = pd.DataFrame(df_data, columns=['Stockholder', 'Stake', 'Shares owned', 'Total value($)', 'Shares bought / sold', 'Total change'])

			# Top 10 Mutual Funds Holding self.{Ticker}
			table = soup.find_all('table', {'class': 'wsod_dataTable wsod_dataTableBig wsod_institutionalTop10'})[1]
			rows = table.find_all('tr')[1:]
			df_data = []
			for row in rows:
				data = row.find_all('td')
				df_data.append([i.get_text() for i in data])

			mutual_funds_df = pd.DataFrame(df_data, columns=['Stockholder', 'Stake', 'Shares owned', 'Total value($)', 'Shares bought / sold', 'Total change'])

			BASE_URL = f'https://fintel.io/so/us/{ticker}'
			soup = _get_soup(BASE_URL)
			table = soup.find('table', {'id': 'transactions'})

			rows = table.find_all('tr')
			df_data = []
			for row in rows[1:]:
				date, form, investor, _, opt, avgshareprice, shares, shareschanged, value, valuechanged, _, _, _ = [i.get_text() for i in row.find_all('td')]
				df_data.append([date, form, investor, opt, avgshareprice, shares, shareschanged, value, valuechanged])

			recent_purchases_df = pd.DataFrame(df_data, columns=['Date', 'Form', 'Investor', 'Opt', 'Avg Share Price',
				'Shares', 'Shares Changed (%)', 'Value ($1000)', 'Value Changed (%)'])
			recent_purchases_df = recent_purchases_df.set_index('Date').sort_index(ascending=False)

			return owners_df, mutual_funds_df, recent_purchases_df.tail()
	
		# Have not decided how I want to format returning all of this information
		return _get_summary(self.ticker), _basic_stats(self.ticker), _price_target(self.ticker), _price_predictions(self.ticker), 
		_ta_indictators(self.ticker), _news_sentiments(self.ticker), _financials(self.ticker), _short_selling(self.ticker), 
		_put_call_ratio(self.ticker), _find_competition(self.ticker), _etfs(self.ticker),_insider_trading(self.ticker), 
		_social_media_sentiment(self.ticker), _catalysts(self.ticker), _big_money(self.ticker)

	def __str__(self):
		return self.ticker


# 	for i in range(2, ticker.shape[0]):
# 		ticker.loc[ticker.index[i], '2_sma'] = sum([float(i) for i in ticker.iloc[i-2:i]['Close']])/2
# 	for i in range(9, ticker.shape[0]):
# 		ticker.loc[ticker.index[i], '9_sma'] = sum([float(i) for i in ticker.iloc[i-9:i]['Close']])/9
# 	try:
# 		ticker = ticker[['Close', 'High', 'Low', '2_sma', '9_sma', 'Volume']]
# 	except:
# 		pass

print('Welcome to PyTrading!')

if __name__ == '__main__':
	# You can use this to test code out without it being imported/ran 
	pass
