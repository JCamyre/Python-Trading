from requests import get 
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
from pathlib import Path

# def get_biggest_movers():
# 	tickers = []
# 	request = get('https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/')
# 	soup = BeautifulSoup(request.text, 'lxml')
# 	table = soup.find('tbody', {'class': 'tv-data-table__tbody'})
# 	for i in table.find_all('a', {'class': 'tv-screener__symbol'})[::2]:
# 		tickers.append(i.get_text())

# 	request = get('http://thestockmarketwatch.com/markets/topstocks/')
# 	soup = BeautifulSoup(request.text, 'lxml')
# 	table = soup.find_all('div', {'class': 'activestockstbl'})

# 	return list(set(tickers))


def get_day_hot_stocks():
	url = 'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/'
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	rows = soup.find_all('tr', {'class':'tv-data-table__row tv-data-table__stroke tv-screener-table__result-row'})
	return [row.find('a').get_text() for row in rows]


def get_day_premarket_movers():
	url = 'https://thestockmarketwatch.com/markets/pre-market/today.aspx'
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	table = soup.find_all('table', {'id': 'tblMoversDesktop'})[0]
	print('First list is biggest winners, second list is from a different website.')
	marketwatch_list = [(ticker.get_text(), float(change.get_text()[:-1].replace(',',''))) for ticker, change in zip(table.find_all('td', {'class': 'tdSymbol'}), table.find_all('td', {'class': 'tdChangePct'}))]

	url = 'https://www.benzinga.com/money/premarket-movers/'
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	table = soup.find('ul', {'class': 'stock-list'})
	benzinga_list = [(ticker.get_text(), float(change.get_text()[:-1])) for ticker, change in zip(table.find_all('a'), table.find_all('span', {'class': 'flex-item-result company-ticker-gain'}))]

	print(sorted(marketwatch_list, key=lambda x: x[1], reverse=True))
	print(sorted(benzinga_list, key=lambda x: x[1], reverse=True))

def get_silver_stocks():
	url = 'http://www.24hgold.com/english/listcompanies.aspx?fundamental=datas&data=company&commodity=ag&commodityname=SILVER&sort=resources&iordre=107'
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	table = soup.find('table', {'id': 'ctl00_BodyContent_tbDataExport'})
	rows = table.find_all('td', {'class': ['cell_bleue_center', 'cell_gold_right']})
	for i in range(len(rows))[28::2]:
		if not '.' in rows[i].get_text():
			print(f'{rows[i].get_text()}: ${rows[i+1].get_text()}')


def load_biggest_movers():
	path = Path(__file__).parents[1]
	with open(f'{path}/dailypickle/biggest_movers-{datetime.now().strftime("%m-%d-%Y")}.pkl', 'rb') as f:
		return pickle.load(f)


def pickle_biggest_movers(portfolio):
	path = Path(__file__).parents[1]
	with open(f'{path}/dailypickle/biggest_movers-{datetime.now().strftime("%m-%d-%Y")}.pkl', 'wb') as f:
		pickle.dump(portfolio, f)

def load_positions():
	path = Path(__file__).parents[1]
	with open(f'{path}/dailypickle/positions-{datetime.now().strftime("%m-%d-%Y")}.pkl', 'rb') as f:
		return pickle.load(f)


def pickle_positions(portfolio):
	# This is useless
	path = Path(__file__).parents[1]
	with open(f'{path}/dailypickle/positions-{datetime.now().strftime("%m-%d-%Y")}.pkl', 'wb') as f:
		pickle.dump(portfolio, f)


def pickle_dump(portfolio):
	today = date.today()
	with open(f"{today.strftime('%m-%d')}_pickle.pkl", 'wb') as f:
		pickle.dump(portfolio, f)


def pickle_load():
	today = date.today()
	with open(f"{today.strftime('%m-%d')}_pickle.pkl", 'rb') as f:
		return pickle.load(f)

