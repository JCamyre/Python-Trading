from datetime import date, datetime
from .base import Ticker
import pandas as pd 
from requests import get
from bs4 import BeautifulSoup
import re
from GoogleNews import GoogleNews
from dotenv import load_dotenv
import os 
import tweepy

# When I have time, replace yahoo api for alphavantage. https://rapidapi.com/alphavantage/api/alpha-vantage, https://www.alphavantage.co/premium/. https://rapidapi.com/mpeng/api/stock-and-options-trading-data-provider
# I can access a lot more stuff (like news and related) by directly accessing API. Most of these Stock. methods can be replaced by accessing API lol.

class Portfolio:
    # Maybe do a DataFrame? Easier to display, can sort. Columns for tickers, change_percentage, last_updated_price
    # Pass in stocks with their target values, like this: (stock, target_prices)
    def __init__(self, stocks, interval='1m', period='1d'):
        # if type(stocks) == tuple:
        # 	self.stocks = stocks[0]

        # if type(stocks[0]) != str:
        # 	while stocks[0] != str:
        # 		stocks = stocks[0]
        # 		print(stocks)

        if type(stocks) == list:
            self.stocks = [Stock(stock, interval=interval, period=period) for stock in sorted(stocks)]
        else:
            self.stocks = [Stock(stock, interval=interval, period=period) for stock in sorted(stocks.split())]

    def add_stocks(self, stocks):
        for stock in stocks.split():
            self.stocks.add(stock)

    def clean_stocks(self):
        for stock in self.stocks:
            if 'trash' in stock.ticker:
                self.stocks.remove(stock)

    def get_biggest_movers(self):
        print("These are today's biggest movers: ")
        for stock in self.stocks:
            if stock.daily_change_percentage > 10.0:
                print(stock.ticker)

    def get_highest_rel_volume(self):
        print("These are today's most relatively active stocks: ")
        for stock in self.stocks:
            if stock.get_relative_volume() > 3.0:
                print(stock.ticker)
        # return [stock.ticker for stock in self.stocks if stock.get_relative_volume() > 3.0]

    def get_stocks(self):
        return sorted([(stock.ticker, stock.daily_stats(), stock.daily_change_percentage()) for stock in self.stocks], key=lambda x: x[0])

    def get_stocks_daily(self): # Fix
        return [stock.df_month for stock in self.stocks]

    def get_stocks_intra(self):
        return [stock.df for stock in self.stocks]

    def sort_by(self, sort='name'):
        if sort == 'name':
            pass
        elif sort == 'change_percentage':
            pass
        elif sort == 'price':
            pass
        else:
            raise Exception('Please enter one of the following sorting methods: name, price, or change_percentage')

    def update_price_change(self):
        print("These stocks' prices have changed significantly.")
        for stock in self.stocks:
            if (stock.df.iloc[0]['Close'] - stock.get_last_updated())/(stock.get_last_updated())*100 > 5.0:
                stock.set_last_updated(stock.df.iloc[0]['Close'])
                print(stock.ticker)

    def __iter__(self):
        return iter(self.stocks)

    def __getitem__(self, i):
        return self.stocks[i]

    def __len__(self):
        return len(self.stocks)

    def __repr__(self):
        return 'A portfolio of #winning stocks.'

class Stock:

    def __init__(self, ticker, target_prices=None, price_invested=None, interval='1m', period='1d'):
        try:
            self.ticker = ticker
            self.df = Ticker(ticker).get_data()
            self.prev_close = self.df.iloc[-1]
            self.target_prices = target_prices
            self.price_invested = price_invested
            self._cur_day_stats = self.df.iloc[-1]
            self._prev_day_stats = self.df.iloc[-2]
        except:
            raise Exception('Sorry, we could not find this stock!')
            
    # Return DataFrame with last 30 days of Stock's closing price and other stats
    def get_month_data(self):
        # This one should be full then cut down to 24 months
        df = Ticker(self.ticker).get_data()
        df.index = pd.to_datetime(df.index)
        for i in range(2, df.shape[0]):
            df.loc[df.index[i], '2_sma'] = sum([float(i) for i in df.iloc[i-2:i]['Close']])/2
        for i in range(9, df.shape[0]):
            df.loc[df.index[i], '9_sma'] = sum([float(i) for i in df.iloc[i-9:i]['Close']])/9
        try:
            df = df[['Close', 'Open', 'High', 'Low', '2_sma', '9_sma', 'Volume']]
        except:
            pass
        return df

    def add_target_prices(self, new_target_prices):
        self.target_prices = new_target_prices

    # Calculate the daily change % in a stock using current day's closing price and yesterday's closing price
    def daily_change_percentage(self, format='cosmetic'):
        value = (float(self._cur_day_stats['Close']) - float(self._prev_day_stats['Close']))/float(self._prev_day_stats['Close'])
        if (format == 'cosmetic'):
            return f"{value*100:.2f}%"
        elif (format == 'number'):
            return value

    # Calculate the change in price from the high of today from close of yesterday
    def daily_high_change_percentage(self, format='cosmetic'):
        value = (float(self._cur_day_stats['High']) - float(self._prev_day_stats['Close']))/float(self._prev_day_stats['Close'])
        if (format == 'cosmetic'):
            return f"{value*100:.2f}%"
        elif (format == 'number'):
            return value
    
    # Calculate the change in price from the low of today from close of yesterday
    def daily_low_change_percentage(self, format='cosmetic'):
        value = (float(self._cur_day_stats['Low']) - float(self._prev_day_stats['Close']))/float(self._prev_day_stats['Close'])
        if (format == 'cosmetic'):
            return f"{value:.2f}%"
        elif (format == 'number'):
            return value

    def daily_stats(self):
        df = Ticker(self.ticker).get_data('1d', '1d')
        df.index = pd.to_datetime(df.index)		
        return self.df.iloc[-1]['Close'], self.df.iloc[-1]['High'], self.df.iloc[-1]['Low']

    def get_relative_volume(self):
        avg_volume = sum(self.df['Volume'])/len(self.df)
        return self.df.iloc[-1]/avg_volume

    def _find_match(self, pattern, text):
        match = pattern.search(text)
        return match

    def _no_attributes(self, tag):
        if 'td' in str(tag):
            return tag.has_attr('class') or tag.has_attr('id')

    HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) AppleWebKit/537.36 " # Telling the website what browser I am "using"
                                "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}

    def _get_soup(self, url):
        response = get(url, headers=self.HEADERS, timeout=20)
        assert response.status_code == 200
        return BeautifulSoup(response.content, 'lxml')

    # Make this all one big function
    def get_summary(self):
        BASE_URL = f'https://www.marketwatch.com/investing/stock/{self.ticker}'
        soup = self._get_soup(BASE_URL)

        summary = soup.find('p', {'class': 'description__text'})

        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}'
        soup = self._get_soup(BASE_URL)
        website = soup.find('a', {'title': 'Company Profile'})
        if website:
            website = website['href']

        return summary.get_text(), website


        # Find the website of the stock and go to its information page

    def basic_stats(self):
        # Market cap, avg volume, financial information
        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}/key-statistics?p={self.ticker}'
        soup = self._get_soup(BASE_URL)

        info = []

        # Financial highlights
        div = soup.find('div', {'class': 'Mb(10px) Pend(20px) smartphone_Pend(0px)'})
        info.append([(i.find('h3', {'class': 'Mt(20px)'}), i.find('tbody').find_all('tr')) for i in div.find_all('div', {'class': 'Pos(r) Mt(10px)'})])

        # Trading Information
        div = soup.find('div', {'class': 'Pstart(20px) smartphone_Pstart(0px)'})
        info.append([(i.find('h3', {'class': 'Mt(20px)'}), i.find('tbody').find_all('tr')) for i in div.find_all('div', {'class': 'Pos(r) Mt(10px)'})])

        info_df = pd.DataFrame(info, columns={'Label', 'Value'})

        # Income Statement
        nerd_info = []
        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}/financials?p={self.ticker}'
        soup = self._get_soup(BASE_URL)
        rows = soup.find_all('div', {'data-test': 'fin-row'})
        for row in rows:
            title = row.find('div', {'class': 'D(tbc) Ta(start) Pend(15px)--mv2 Pend(10px) Bxz(bb) Py(8px) Bdends(s) Bdbs(s) Bdstarts(s) Bdstartw(1px) Bdbw(1px) Bdendw(1px) Bdc($seperatorColor) Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pstart(15px)--mv2 Pstart(10px)'})
            data = row.find('div', {'data-test': 'fin-col'})
            nerd_info.append([title.get_text(), data.get_text()])
        
        # Balance Sheet
        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}/balance-sheet?p={self.ticker}'
        soup = self._get_soup(BASE_URL)
        rows = soup.find_all('div', {'data-test': 'fin-row'})
        for row in rows:
            title = row.find('D(ib) Fw(b) Ta(start) Px(15px)--mv2 Px(10px) W(247px)--mv2 W(222px) Bxz(bb) Bdendw(1px) Bdstartw(1px) Bdbw(1px) Bdends(s) Bdstarts(s) Bdbs(s) Bdc($seperatorColor) Py(6px) Pos(st) Start(0) Bgc($lv2BgColor)')
            data = row.find('div', {'data-test': 'fin-col'})
            nerd_info.append([title.get_text(), data.get_text()])

        nerd_df = pd.DataFrame(nerd_info, columns={'Label', 'Value'})
        
        return info_df, nerd_df

    def price_target(self, exchange='NASDAQ'): # Automatically find correct stock exchange
        BASE_URL = f'https://www.marketbeat.com/stocks/{exchange}/{self.ticker}/price-target/'
        soup = self._get_soup(BASE_URL)
        
        price_target = soup.find('table', {'class': 'scroll-table'})
        _pattern = re.compile(r'Price Target: \$\d{1,3}\.\d\d')
        price_target = self._find_match(_pattern, table.get_text()).group(0)
        _pattern = re.compile(r'\d{1,3}\.\d\d\% \w{6,8}')
        percentage = self._find_match(_pattern, table.get_text()).group(0)

        BASE_URL = f'https://finviz.com/quote.ashx?t={self.ticker}'
        response = get(BASE_URL, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': "fullview-ratings-outer"})
        rows = table.find_all('td', {'class': 'fullview-ratings-inner'})
        df_data = []
        for row in rows:
            row = row.find_all('td')
            date, _, fund, action, pricetarget = [val.get_text() for val in row]
            date = datetime.strptime(date, '%b-%d-%y')
            df_data.append((date, fund, action, pricetarget))

        analyst_price_targets = pd.DataFrame(df_data, columns=['Date', 'Fund', 'Action', 'PriceTarget'])
        analyst_price_targets = analyst_price_targets.set_index('Date')
        return price_target, percentage, analyst_price_targets

    def price_predictions(self):
        BASE_URL = f'https://www.barchart.com/stocks/quotes/{self.ticker}/opinion'
        soup = self._get_soup(BASE_URL)

        table = soup.find('table', {'data-ng-class': "{'hide': currentView !== 'strengthDirection'}"})
        titles = soup.find_all('tr', {'class': 'indicator-title'})
        titles = [i.get_text() for i in titles]

        data = soup.find_all('tr', {'class': 'indicator-item'})
        data = [i.get_text() for i in data]
        data = data[len(data)//2 + 1:]
        df_data = []
        for i in data:
            signal, strength, direction = i.split()[-3:]
            indictator = ' '.join(i.split()[:-3])
            df_data.append((indictator, signal, strength, direction))
        df = pd.DataFrame(df_data, columns=['Indictator', 'Signal', 'Strength', 'Direction'])
        return df, titles

    def ta_indictators(self): # Loads wrong page. Beta, RSI history, above/below 9 SMA, above/below 180 SMA, volatility, rel volume, 52W high/low
        # OBV: calculate OBV, then compare to stock close price, say how close they correlate.
  

        pass


    def news_sentiments(self): # Returns news articles curated via Finviz, Yahoo, and Google News, GET UNUSUAL OPTION ACTIVITY
        BASE_URL = f'https://finviz.com/quote.ashx?t={self.ticker}'
        soup = self._get_soup(BASE_URL)

        table = soup.find('table', {'class': 'fullview-news-outer'})
        rows = table.find_all('tr')
        df_data = []
        for row in rows:
            date = row.find('td', {'align': 'right'})
            article = row.find('td', {'align': 'left'})
            link = article.find('a')['href']
            df_data.append((date.get_text(), article.get_text(), link))
        df = pd.DataFrame(df_data, columns=['Time', 'Headline', 'Link'])


        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}/news?p={self.ticker}'
        soup = self._get_soup(BASE_URL)

        links = soup.find_all('a', {'class': 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'})
        news = [(link.get_text(), str('yahoo.com' + link['href'])) for link in links]

        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}/press-releases?p={self.ticker}'
        soup = self._get_soup(BASE_URL)

        links = soup.find_all('a', {'class': 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'})
        press_releases = [(link.get_text(), str('yahoo.com' + link['href'])) for link in links]
        # Look for keywords in the news? Any showcases, Investor/analyst days, Analyst revisions, Management transitions
        # Product launches, Significant stock buyback changes
  
  
          # Getting news from google news search
        googlenews = GoogleNews(lang='en', period='14d') # Specify period for news
        googlenews.get_news(f'${self.ticker} stock')
        stock_news = googlenews.results()
  
        # print([(i, j) for i, j in zip(googlenews.get_texts(), googlenews.get_links())])
        # To get other pages, do googlenews.get_page(2), etc.
  
        # Have whitelist of websites to search articles from. Maybe have key word to filter out stupid stuff.
  
        sectors = self.find_competition()
        sector_news = []
        if sectors:
            for sector in sectors:
                googlenews = GoogleNews(lang='en', period='14d')
                googlenews.get_news(f'{sector} sector stocks')
                sector_news.append(googlenews.result())
    
        return df, news, press_releases, sector_news, stock_news

    def financials(self): # OMEGALUL
        # Displaying all information. Could leave this as a dictionary.
        BASE_URL = f'https://finviz.com/quote.ashx?t={self.ticker}'
        soup = self._get_soup(BASE_URL)
        table = soup.find('table', {'class': 'snapshot-table2'})
        labels = table.find_all('td', {'class': 'snapshot-td2-cp'})
        values = table.find_all('td', {'class': 'snapshot-td2'})
        info_dict = {}
        for label, val in zip(labels, values):
            info_dict[str(label.get_text())] = str(val.get_text()) 
   
        info_dict['company_name'] = soup.find_all('b')[5].get_text()
        df = pd.DataFrame(info_dict.items(), columns={'Label', 'Value'})

        return df

    def short_selling(self):
        '''
        Returns a stocks short_selling information
        '''
        BASE_URL = f'https://finviz.com/quote.ashx?t={self.ticker}'
        soup = self._get_soup(BASE_URL)

        labels = soup.find_all('td', {'class': 'snapshot-td2-cp'})
        values = soup.find_all('td', {'class': 'snapshot-td2'})

        return labels[16].get_text(), values[16].get_text(), labels[22].get_text(), values[22].get_text()


    def put_call_ratio(self): 
        '''
        Returns various information regarding the put call ratio of a stock.
        '''
        BASE_URL = f'https://www.alphaquery.com/stock/{self.ticker}/volatility-option-statistics/120-day/put-call-ratio-oi'
        soup = self._get_soup(BASE_URL)

        ratio_volume = soup.find('tr', {'id': 'indicator-put-call-ratio-volume'})
        ratio_open_interest = soup.find('tr', {'id': 'indicator-put-call-ratio-oi'})
        forward_price = soup.find('tr', {'id': 'indicator-forward-price'})
        call_breakeven_price = soup.find('tr', {'id': 'indicator-call-breakeven'})
        put_breakeven_price = soup.find('tr', {'id': 'indicator-put-breakeven'})
        option_breakeven_price = soup.find('tr', {'id': 'indicator-option-breakeven'})

        return ratio_volume, ratio_open_interest, forward_price, call_breakeven_price, put_breakeven_price, option_breakeven_price

    def find_competition(self):
        BASE_URL = f'https://finviz.com/quote.ashx?t={self.ticker}'
        soup = self._get_soup(BASE_URL)

        td = soup.find_all('td', {'class': 'fullview-links'})[1]
        sectors = td.find_all('a', {'class': 'tab-link'})
        # sector_urls = ([str('https://finviz.com/' + i['href']) for i in sectors])
        # for url in sector_urls: # Find stocks with similar P/E ratios and market cap, then track difference in performance
        # 	print(url)
  
        sectors = [sector.get_text() for sector in sectors]
        return sectors

    def etfs(self):
        BASE_URL = f'https://etfdb.com/stock/{self.ticker}/'
        soup = self._get_soup(BASE_URL)
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')
        rows = [[i.get_text() for i in row.find_all('td')] for row in rows]
        train_df = pd.DataFrame(rows, columns={'self.Ticker', 'ETF', 'ETF Category', 'Expense Ratio', 'Weighting'})
        return train_df

    def insider_trading(self):
        BASE_URL = f'https://finviz.com/quote.ashx?t={self.ticker}'
        soup = self._get_soup(BASE_URL)

        tr = soup.find_all('tr', {'class': "insider-sale-row-2"})
        return [i.get_text() for i in tr]

        BASE_URL = f'https://www.secform4.com/'
        # Will be hard to get a stock, think I have to use Selenium to type in search bar and search.

    def social_media_sentiment(self, num_of_tweets=50): # Also reddit sentiment, and twitter
        # Twitter
        load_dotenv()
        consumer_key = os.getenv('TWEEPY_KEY')
        consumer_secret = os.getenv('TWEEPY_SECRET_KEY')
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        tweets = []
        for i, tweet in enumerate(tweepy.Cursor(api.search, q=f'${self.ticker}', count=num_of_tweets).items(num_of_tweets)):
            tweets.append(i, tweet.text, tweet.author.screen_name, tweet.retweet_count, tweet.favorite_count, tweet.created_at)
   
        # Get sentiment from stocktwits, get a token later. symbol, trending, sectors, symbols, 
        # Symbol
        BASE_URL = f'https://api.stocktwits.com/api/2/streams/symbol/{self.ticker}.json'
        symbol_messages = [message['body'] for message in get(BASE_URL).json()['messages']]

        BASE_URL = 'https://api.stocktwits.com/api/2/streams/trending.json'
        trending_messages = [message['body'] for message in get(BASE_URL).json()['messages']]

        # https://api.stocktwits.com/api/2/streams/sectors/technology.json?access_token=<access_token>
  
        return tweets, symbol_messages, trending_messages

    # Stocks with three good days in a row or above 9sma for three days. Good rsi = either high break out, piss low, ~40 support.
    
    def adl(self):
        data = self.get_month_data()
        adl = 0.0
        for row in data.iterrows():
            adl += (((row['Close'] - row['Low']) - (['High'] - row['Close']))/(['High'] - row['Low'])) * row['Volume']     
        
        return adl
  
 
    def technical_analysis(self):
        pass

    def fundamental_analysis(self):
        pass

    def seasonality(self):
        pass

    def catalysts(self): # Returns date of showcases, FDA approvals, earnings, etc
        df_data = []
        # Earnings date: 
        BASE_URL = f'https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}&.tsrc=fin-srch'
        soup = self._get_soup(BASE_URL)
        
        # Convert to datetime
        earnings_date = soup.find('td', {'data-test': 'EARNINGS_DATE-value'})
        earnings_date = f'Next earnings date: {earnings_date.get_text()}'

        # FDA approvals
        BASE_URL = 'https://www.rttnews.com/corpinfo/fdacalendar.aspx'
        soup = self._get_soup(BASE_URL)

        company = soup.find_all('div', {'data-th': 'Company Name'})

        events = soup.find_all('div', {'data-th': 'Event'})

        outcome = soup.find_all('div', {'data-th': 'Outcome'})

        dates = soup.find_all('span', {'class': 'evntDate'})

        for i in range(len(company)):
            if outcome[i]:
                if not len(dates[i].split()) > 1:
                    date = datetime.strptime(dates[i].get_text(), '%m/%d/%Y')
                else:
                    date = datetime.strptime(dates[i].split()[1:].get_text(), '%b %Y')

                df_data.append([date, company[i].get_text(), events[i].get_text(), outcome[i].get_text()])
            else:
                df_data.append([company[i].get_text(), events[i].get_text(), outcome[i]])

        # FDA trials
        df = pd.DataFrame(df_data, columns=['Date', 'Company Name', 'Event', 'Outcome'])
        # ?PageNum=4 to ?PageNum=1
        return df

    def big_money(self): # Returns recent institutional investments in a stock, as well as the largest shareholders and mutual funds holding the stock
        BASE_URL = f'https://money.cnn.com/quote/shareholders/shareholders.html?symb={self.ticker}&subView=institutional'
        soup = self._get_soup(BASE_URL)

        # Top 10 Owners
        df_data = []
        table = soup.find('table', {'class': 'wsod_dataTable wsod_dataTableBig wsod_institutionalTop10'})
        rows = table.find_all('tr')[1:]
        for row in rows:
            data = row.find_all('td')
            df_data.append([i.get_text() for i in data])

        owners_df = pd.DataFrame(df_data, columns=['Stockholder', 'Stake', 'Shares owned', 'Total value($)', 'Shares bought / sold', 'Total change'])

        # Top 10 Mutual Funds Holding 
        table = soup.find_all('table', {'class': 'wsod_dataTable wsod_dataTableBig wsod_institutionalTop10'})[1]
        rows = table.find_all('tr')[1:]
        df_data = []
        for row in rows:
            data = row.find_all('td')
            df_data.append([i.get_text() for i in data])

        mutual_funds_df = pd.DataFrame(df_data, columns=['Stockholder', 'Stake', 'Shares owned', 'Total value($)', 'Shares bought / sold', 'Total change'])

        # Recent instutional investments, from a better source this time
        # Make sure sorted by most recent.
        BASE_URL = f'https://fintel.io/so/us/{self.ticker}'
        soup = self._get_soup(BASE_URL)
        table = soup.find('table', {'id': 'transactions'})
        rows = table.find_all('tr')
        df_data = []
        for row in rows[1:]:
            date, form, investor, _, opt, avgshareprice, shares, shareschanged, value, valuechanged, _, _, _ = [i.get_text() for i in row.find_all('td')]
            df_data.append([date, form, investor, opt, avgshareprice, shares, shareschanged, value, valuechanged])
        recent_purchases_df = pd.DataFrame(df_data, columns=['Date', 'Form', 'Investor', 'Opt', 'Avg Share Price',
            'Shares', 'Shares Changed (%)', 'Value ($1000)', 'Value Changed (%)'])
        recent_purchases_df = recent_purchases_df.set_index('Date').sort_index(ascending=False)

        return owners_df, mutual_funds_df, recent_purchases_df.tail()


    def r_and_d(self):
        BASE_URL = f'https://ycharts.com/companies/{self.ticker}/r_and_d_expense'
        soup = self._get_soup(BASE_URL)
        tables = soup.find_all('table', {'class': 'histDataTable'})
        _pattern = re.compile(r'\d{1,3}\.\d{2}M')
        all_dicts = []
        for table in tables:
            keys = [key.get_text() for key in table.find_all('td', {'class': 'col1'})]
            vals = [_find_match(_pattern, val.get_text()).group() for val in table.find_all('td', {'class': 'col2'})]
            data_dict = {key : val for key, val in zip(keys, vals)}
            all_dicts.append(data_dict)
        return all_dicts

    # Options links: https://www.optionsprofitcalculator.com, f'https://marketchameleon.com/Overview/{ticker}/IV/', Need to find stock api that has option chain info like robinhood (greeks, iv, etc, price)	
    
    def __str__(self):
        return self.ticker

    def __repr__(self):
        return self.ticker

print('Welcome to Py-Trading!')

if __name__ == '__main__':
    # You can use this to test code out without it being imported/ran 
    pass
