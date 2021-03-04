# Pytrading
This package contains modules with functions that assist day and swing traders by aiding them in keeping track of their positions 
and trending stocks.

## Installation
```bash
pip install py-trading
```

## Usage
```python
import py_trading as pytrd

my_portfolio = pytrd.Portfolio(['AAPL', 'TSLA', 'F', 'COKE'])
for stock in my_portfolio:
	stock.update_stock() 
	print(stock.get_month_data())
	print(stock.daily_change_percentage())
	print(stock.get_last_updated())
	print(stock.daily_high_change_percentage())
	print(stock.daily_stats())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)