import numpy as np

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

# Enter in total amount you would like to invest under amountInvested 
amountInvested = 10000


# GENERATING MARKET PORTFOLIO
# format [U.S. Stocks, International Stocks, U.S. Bonds, International Bonds] (in billions for market cap)
EOQmarketcaps = np.array(etfEOQmarketcaps)
EOQprices = np.array(etfEOQprices)
recentPrices = np.asarray(etfRecentPrices)
# Market proportions for each etf on end of quarter
EOQproportions = EOQmarketcaps/sum(EOQmarketcaps)
# Ratio of recent prices and end of quarter prices
priceRatios = recentPrices / EOQprices
# Multiply ratios to market proportions
products = EOQproportions * priceRatios
# Market weights if fractional shares existed
revisedProportions = products / sum(products)
# Amount of money invested in each etf if fractional shares existed
desiredValues = revisedProportions * amountInvested
# Number of shares of etfs to buy if fractional shares existed
currentPrices = np.array(etfCurrPrices(['VTI', 'VXUS', 'BND', 'BNDX']))
shares = desiredValues/currentPrices
# Optimize to get as close to 0 since fractional shares with Schwab doesn't exist
def asdf(a):
    return amountInvested - sum(np.round(shares * a)*currentPrices)
a = .90
while asdf(a) > 0:
    if a <.99999:
        a+=.00001
    else:
        break
    if asdf(a) < 0:
        a-=.00001
        break
# Actual shares of each etf to buy
actualShares = np.round(shares * a)
print('VTI, VXUS, BND, BNDX')
print(actualShares)

actualProportions = (actualShares * currentPrices)/sum(actualShares * currentPrices)
print('Theoretical proportions')
print(revisedProportions)
print('Actual proportions')
print(actualProportions)

# Cash left over. You can invest this cash into VTIP (Vanguard's US TIPS ETF) or something else if you'd like.
cash = amountInvested - sum((actualShares * currentPrices))
print(np.round(cash,2))