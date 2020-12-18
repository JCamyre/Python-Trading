import time
import kivy
from pytrading import Portfolio
from pytrading.live_trading import trending_stocks
from pytrading.download_tickers import load_todays_biggest_movers, pickle_biggest_movers, get_biggest_movers


kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty

my_portfolio = Portfolio(load_todays_biggest_movers())
# I need to make asdding price_targets easier
# target_prices_list = [[22, 19, 10.5, 9.5, 8, 6.7, 5.6], [17, 15, 12, 9.8, 8, 7, 6], [1.6, 0.8], [10.5, 8.5, 4.1]]
# for stock, target_prices in zip(my_portfolio, target_prices_list):
#     stock.add_target_prices(target_prices)

# Alert if near price target

Builder.load_string("""
<MySec>:
    orientation: 'horizontal'
    Label:
        id: kv_sec
        text: root.seconds_string
        font_size: 20
""")


class MySec(BoxLayout):
    seconds_string = StringProperty('')


class MyApp(App):

    def build(self):
        Clock.schedule_interval(lambda dt: self.update_time(), 90)
        return MySec()

    def update_time(self):
        self.root.seconds_string = '\n'.join(trending_stocks(my_portfolio))

if __name__ == '__main__':
    MyApp().run()

'''
Trying to have two columns of data
import time
import kivy

kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from livetrading import Portfolio, stock_tracker

Builder.load_string("""
<MySec>:
    orientation: 'horizontal'
    Label:
        id: kv_stocks1
        text: root.seconds_string1
        font_size: 20
    Label:
        id: kv_stocks2
        text: root.seconds_string2
        font_size: 20
""")


class MySec(BoxLayout):
    seconds_string = StringProperty('')


class MyApp(App):

    def build(self):
        Clock.schedule_interval(lambda dt: self.update_time(), 25)
        return MySec()

    def update_time(self):
        uurr = stock_tracker(Portfolio(['ABB', 'RGR', 'AYRO', 'SWBI', 'NIO', 'SOLO', 'TSLA', 'DADA', 'BILI']))
        self.root.seconds_string1 = '\n \n'.join(uurr[:len(uurr)])
        self.root.seconds_string2 = '\n \n'.join(uurr[len(uurr):])
        print('Glizzy, joy emoji')

if __name__ == '__main__':
    MyApp().run()

'''