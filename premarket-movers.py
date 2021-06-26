from py_trading.download_tickers import get_day_premarket_movers
from datetime import datetime

if datetime.today().weekday() not in [5, 6]:
	get_day_premarket_movers()

