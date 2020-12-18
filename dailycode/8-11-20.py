import sys
# Used to access local module outside of its folder
sys.path.append('C:/Users/JWcam/Desktop/All_projects/Python-Trading')
from intra_day_tracker import live_stock_data

# Need an try except thing if someone inputs the wrong ticker
stocks = [stock.upper() for stock in input().split()]
live_stock_data(stocks)

# 2k calls an hour. If ~100 stocks every 75 seconds