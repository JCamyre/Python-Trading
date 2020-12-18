from intra_day_tracker import live_stock_data
from pytrading import Portfolio
# live_stock_data()

test_portfolio = Portfolio(['TTM', 'ADTX'], '1m', '1d')
print([stock.df for stock in test_portfolio])
