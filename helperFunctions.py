import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
etfs = ['vti','vxus','bnd','bndx']

def etfPriceData():
    etf_price_data = pd.DataFrame(columns=['Date','ETF','Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume'])
    start_epoch = int(datetime.datetime(2000,1,1).timestamp())
    curr_epoch = int(time.time())
    for etf in etfs:
        url = 'https://query1.finance.yahoo.com/v7/finance/download/'+etf+'?period1='+str(start_epoch)+'&period2='+str(curr_epoch)+'&interval=1d&events=history'
        try:
            df = pd.read_csv(url,parse_dates=[0])
        except ex.HTTPError:
            # Including some breaks to avoid being blocked
            time.sleep(20)
            continue
        df['ETF'] = etf.upper()
        df['AdjClose'] = df['Adj Close'].astype('float64')
        df = df.drop(['Adj Close'],axis=1)
        df = df.dropna(subset=['AdjClose', 'Volume'])
        df['Open']=df['Open'].astype('float64')
        df['High']=df['High'].astype('float64')
        df['Low']=df['Low'].astype('float64')
        df['Close']=df['Close'].astype('float64')
        df['Volume']=df['Volume'].astype('int64')
        etf_price_data = etf_price_data.append(df)
        etf_price_data = etf_price_data.reset_index(drop=True)
    # Saving historical price data
    etf_price_data.to_csv('Data/etf_price_data.csv',index=False)

def etfCurrPrices(etfList):
     options = webdriver.ChromeOptions()
     options.add_argument('--headless')
     driver = webdriver.Chrome('/Users/avinaashkoganti/chromedriver',options=options)
     prices = []
     for etf in etfList:
         driver.get('https://finance.yahoo.com/quote/'+etf)
         html = driver.page_source
         soup = BeautifulSoup(html,features="html.parser")
         x = soup.find('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
         price = float(x.text)
         prices.append(price)
     driver.close()
     return prices