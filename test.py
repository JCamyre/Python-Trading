import pytrading.py_trading as py_trd

stonks = py_trd.Portfolio(['CBAY', 'OPGN'])
print(stonks[0].daily_high_change_percentage())
