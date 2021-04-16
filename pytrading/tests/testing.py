from requests import get
import pandas as pd 
from bs4 import BeautifulSoup

def get_nyse(): # Test to see if duplicate tickers on backend or Django webapp. Ok, so it's the Django side.
	dfs = []
	for letter in 'abcdefghijklmnopqrstuvwxyz':
		request = get(f'https://eoddata.com/stocklist/NYSE/{letter}.htm')
		soup = BeautifulSoup(request.text, 'lxml')
		table = soup.find('table', {'class': 'quotes'})
		df = pd.read_html(str(table))
		dfs.append(df[0])
	print(pd.concat(dfs).shape)
	return pd.concat(dfs)

get_nyse()