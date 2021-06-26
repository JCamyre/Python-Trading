from requests import get 
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
from pathlib import Path
import pandas as pd

# IMPLEMENT THREADING
# results = [executor.submit(test_stocks, i, n_threads) for i in range(n_threads)] # Can try executor.map()
        
#         for f in concurrent.futures.as_completed(results):
#             print(f.result())
    
# def test_stocks(index_of_thread, num_of_threads): # Divide # of stocks per thread / total stocks to be tested. Index_of_thread is which thread from 0 to n threads.
#     n_stocks_per_thread = len(Stock.objects.all()) 
#     portion = Stock.objects.all()[index_of_thread*n_stocks_per_thread:(index_of_thread+1)*n_stocks_per_thread]

def get_sp500():
	request = get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = BeautifulSoup(request.text, 'lxml')
	table = soup.find('table')
	df = pd.read_html(str(table))
	return df[0]

def get_nasdaq(): # Nasdaq + NYSE + AMEX
    dfs = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        request = get(f'https://www.advfn.com/nasdaq/nasdaq.asp?companies={letter.upper()}')
        soup = BeautifulSoup(request.text, 'lxml')
        table = soup.find('table', {'class': 'market tab1'})
        df = pd.read_html(str(table))[0]
        df.columns = df.iloc[1].tolist()
        df = df.iloc[2:]
        df = df.reset_index()
        df = df[['Symbol', 'Equity']]
        df.columns = ['ticker', 'name']
        dfs.append(df)
        
    for letter in 'abcdefghijklmnopqrstuvwxyz':           
        request = get(f'http://eoddata.com/stocklist/NASDAQ/{letter}.htm')
        soup = BeautifulSoup(request.text, 'lxml')
        table = soup.find('table', {'class': 'quotes'})
        df = pd.read_html(str(table))[0]
        df = df[['Code', 'Name']]
        df.columns = ['ticker', 'name']
        dfs.append(df)
  
    df = pd.concat(dfs)
    df = df.reset_index()
    df = df[['ticker', 'name']]
    # if as_list:
        # return df.set_index('ticker').to_dict()
    return df

def get_nyse(): # Test to see if duplicate tickers on backend or Django webapp
    dfs = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        request = get(f'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={letter.upper()}')
        soup = BeautifulSoup(request.text, 'lxml')
        table = soup.find('table', {'class': 'market tab1'})
        df = pd.read_html(str(table))[0]
        df.columns = df.iloc[1].tolist()
        df = df.iloc[2:]
        df = df.reset_index()
        df = df[['Symbol', 'Equity']]
        df.columns = ['ticker', 'name']
        dfs.append(df)
        
    for letter in 'abcdefghijklmnopqrstuvwxyz':       
        request = get(f'https://eoddata.com/stocklist/NYSE/{letter}.htm')
        soup = BeautifulSoup(request.text, 'lxml')
        table = soup.find('table', {'class': 'quotes'})
        try:
            df = pd.read_html(str(table))[0]
        except:       
            df = pd.read_html(str(table))            
        df = df[['Code', 'Name']]
        df.columns = ['ticker', 'name']
        dfs.append(df)
        
    	# Will this work since they are series?
    df = pd.concat(dfs)
    df = df.reset_index()
    df = df[['ticker', 'name']]
    # df['ticker'] = df['ticker'].unique()
    # df['name'] = df['name'].unique()
    # if as_list:
    #     return sorted(df.tolist())
    return df.sort_values(by='ticker', ascending=True)


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
	try:
		print('Biggest winners from TheStockMarketWatch:')
		marketwatch_list = [(ticker.get_text(), float(change.get_text()[:-1].replace(',',''))) for ticker, change in zip(table.find_all('td', {'class': 'tdSymbol'}), table.find_all('td', {'class': 'tdChangePct'}))]
		for ticker, percentage in sorted(marketwatch_list, key=lambda x: x[1], reverse=True):
			print(f'{ticker}: {percentage}%')
	except:
		print('Due to unseen errors, the stockmarketwatch list is unable to be reached.')
	print()

	url = 'https://www.benzinga.com/money/premarket-movers/'
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	div = soup.find('div', {'id': 'movers-stocks-table-gainers'})
	tbody = div.find('tbody')
	data = [(i.get_text().replace('\n    ', '')[2:], float(j.get_text().replace('\n  ', '')[2:-1])) for i, j in zip(tbody.find_all('a', {'class': 'font-normal'}), tbody.find_all('td')[3::5])]
	try:
		print('Biggest winners from Benzinga:')
		for ticker, percentage in data:
			print(f'{ticker}: {percentage}%')
	except:
		print('Due to unseen errors, the Benzinga list is unable to be reached.')

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

