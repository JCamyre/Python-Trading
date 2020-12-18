import sys
# Used to access local module outside of its folder
sys.path.append('C:/Users/JWcam/Desktop/All_projects/Python-Trading')
from intra_day_tracker import live_stock_data

# Need an try except thing if someone inputs the wrong ticker
positions = [stock.upper() for stock in input().split()]
live_stock_data(positions)