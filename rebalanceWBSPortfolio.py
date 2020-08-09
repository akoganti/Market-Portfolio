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


# REBALANCE (run this cell if you already have money invested in the market portfolio)
# Enter in number of shares here in current port in the format of VTI, VXUS, BND, BNDX
currentPort = np.array([12.0588,27.0695,16.0667,21.0345])
trades = actualShares - currentPort
# Amount left for trades
amountInvestable = amountInvested - sum(currentPort * currentPrices)
# Need to make sure trades don't make balance go over amount of money available
def asdf(a):
    return amountInvestable - sum(np.round(trades * a)*currentPrices)
a = .90
while asdf(a) > 0:
    if a <.99999:
        a+=.00001
    else:
        break
    if asdf(a) < 0:
        a-=.00001
        break
actualTrades = np.round(trades * a)
print('Trades: VTI, VXUS, BND, BNDX')
print(actualTrades)
print()
print('Cash left over')
print(asdf(a))



portAfterTrades = currentPort + actualTrades
print('Theoretical proportions')
print(revisedProportions)
print()
print('Actual proportions after rebalance')
print((portAfterTrades * currentPrices)/sum(portAfterTrades * currentPrices))