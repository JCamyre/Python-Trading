# Pytrading
This package contains modules with functions that assist day and swing traders by aiding them in keeping track of their positions 
and trending stocks.

# Basic tutorial
import py_trading as pytrade

my_portfolio = pytrade.Portfolio(['AAPL', 'TSLA', 'F', 'COKE'])
for stock in my_portfolio:
	stock.update_stock() 
	print(stock.get_month_data())
	print(stock.daily_change_percentage())
	print(stock.get_last_updated())
	print(stock.daily_high_change_percentage())
	print(stock.daily_stats())

