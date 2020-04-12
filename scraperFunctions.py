import requests
from bs4 import BeautifulSoup
import re
import io
import PyPDF2
import pandas as pd
import datetime
import time
from selenium import webdriver
etfs = ['vti','vxus','bnd','bndx','vtip']

def vtiScraper():
    vtiURL = "http://www.crsp.org/fact-sheet-archive"
    r = requests.get(vtiURL)
    soup = BeautifulSoup(r.text,features="html.parser")
    marketCaps = []
    dates = []
    for link in soup.find_all('a'):
        if re.search('crsptm', str(link.get('href')), re.IGNORECASE):
            date = link.text.replace('Quarter Ending ', '')
            dates.append(date)
            pdf = requests.get(link.get('href'))
            open_pdf = io.BytesIO(pdf.content)
            read_pdf = PyPDF2.PdfFileReader(open_pdf)
            pdf_page2 = read_pdf.getPage(1)
            page_text = pdf_page2.extractText()
            try:
                market_cap = int(re.findall('INDEX MARKET CAP\d+,\d+,\d+', page_text, re.IGNORECASE)[0].upper().replace('INDEX MARKET CAP','').replace(',',''))
            except:
                try:
                    page_text = pdf_page2.extractText().replace('\n','')
                    market_cap = int(re.findall('INDEX MARKET CAP\d+,\d+,\d+', page_text, re.IGNORECASE)[0].upper().replace('INDEX MARKET CAP','').replace(',',''))
                except:
                    market_cap = 'n/a'
            marketCaps.append(market_cap)
    vtiDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    return vtiDF

def vxusScraper():
    cur_year = datetime.datetime.now().year
    cur_month = datetime.datetime.now().month
    error_url = 'https://www.ftserussell.com/products/indices/home/errorview?aspxerrorpath=/Analytics/FactSheets/Home/DownloadSingleIssueByDate'
    dates = []
    report_links = []
    marketCaps = []
    for y in range(2013,cur_year+1):
        year = str(y)
        for m in range(1,13):
            if y==cur_year and m>cur_month:
                break
            if m < 10:
                month = '0' + str(m)
            else:
                month = str(m)
            for d in range(28,32):
                day = str(d)
                date = year + month + day
                url = "https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssueByDate?IssueName=GXUSS&IssueDate="+ date + "&IsManual=false.pdf"
                response = requests.get(url)
                if response.url != error_url:
                    dates.append(date)
                    pdf = requests.get(url)
                    open_pdf = io.BytesIO(pdf.content)
                    read_pdf = PyPDF2.PdfFileReader(open_pdf)
                    pdf_page2 = read_pdf.getPage(1)
                    page_text = pdf_page2.extractText()
                    cleaned_page_text = page_text.replace('\n',' ').replace('  ',' ').replace('  ',' ')
                    mc = re.findall('Totals \d+ \d+,\d+,\d+', cleaned_page_text, re.IGNORECASE)
                    if mc == []:
                        mc = 'n/a'
                        marketCaps.append(mc)
                        continue
                    else:
                        mc_1 = mc[0].replace(',','')
                        mc_2 = mc_1.replace('\n','')
                        mc_3 = mc_2.replace('Totals','')
                        mc = [int(s) for s in mc_3.split() if s.isdigit()][1]
                        marketCaps.append(mc)
                    break
    vxusDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    return vxusDF

def bndScraper():
    cur_year = datetime.datetime.now().year
    cur_month = datetime.datetime.now().month
    error_url = 'https://www.ftserussell.com/products/indices/home/errorview?aspxerrorpath=/Analytics/FactSheets/Home/DownloadSingleIssueByDate'
    error_url2 = 'https://research.ftserussell.com/Analytics/FactSheets/Home/ErrorPage?ErrorMessage=There%20has%20been%20a%20problem%20downloading%20this%20file'
    dates = []
    marketCaps = []
    for y in range(2019,cur_year+1):
        year = str(y)
        for m in range(1,13):
            if y==cur_year and m>cur_month:
                break
            if m < 10:
                month = '0'+ str(m)
            else:
                month = str(m)
            for d in range(28,32):
                day = str(d)
                date = year + month + day
                status = 'true'
                url = "https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssueByDate?IssueName=USBIG&IssueDate="+date+"&IsManual="+status
                response = requests.get(url)
                if response.url == error_url or response.url == error_url2:
                    status = 'false'
                    url = "https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssueByDate?IssueName=USBIG&IssueDate="+date+"&IsManual="+status
                    response = requests.get(url)
                elif response.url != error_url and response.url != error_url2:
                    dates.append(date)
                    pdf = requests.get(url)
                    open_pdf = io.BytesIO(pdf.content)
                    read_pdf = PyPDF2.PdfFileReader(open_pdf)
                    pdf_page2 = read_pdf.getPage(0)
                    page_text = pdf_page2.extractText()
                    info = re.findall('USBIG\d+,\d+,\d+.\d\d', page_text, re.IGNORECASE)
                    mc = float(re.sub(r'USBIG\d+,\d\d\d','',info[0]).replace(',',''))
                    marketCaps.append(mc)
                    break
    bndDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    return bndDF

def bndxScraper():
    cur_year = datetime.datetime.now().year
    cur_month = datetime.datetime.now().month
    error_url = 'https://www.ftserussell.com/products/indices/home/errorview?aspxerrorpath=/Analytics/FactSheets/Home/DownloadSingleIssueByDate'
    error_url2 = 'https://research.ftserussell.com/Analytics/FactSheets/Home/ErrorPage?ErrorMessage=There%20has%20been%20a%20problem%20downloading%20this%20file'
    dates = []
    marketCaps = []
    for y in range(2019,cur_year+1):
        year = str(y)
        for m in range(1,13):
            if y==cur_year and m>cur_month:
                break
            if m < 10:
                month = '0'+ str(m)
            else:
                month = str(m)
            for d in range(28,32):
                day = str(d)
                date = year + month + day
                status = 'true'
                url = "https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssueByDate?IssueName=WBIG&IssueDate="+date+"&IsManual="+status
                response = requests.get(url)
                if response.url == error_url or response.url == error_url2:
                    status = 'false'
                    url = "https://research.ftserussell.com/Analytics/FactSheets/Home/DownloadSingleIssueByDate?IssueName=WBIG&IssueDate="+date+"&IsManual="+status
                    response = requests.get(url)
                elif response.url != error_url and response.url != error_url2:
                    dates.append(date)
                    pdf = requests.get(url)
                    open_pdf = io.BytesIO(pdf.content)
                    read_pdf = PyPDF2.PdfFileReader(open_pdf)
                    pdf_page2 = read_pdf.getPage(0)
                    page_text = pdf_page2.extractText()
                    info = re.findall('WorldBIG\d+,\d+,\d+.\d\d', page_text, re.IGNORECASE)
                    mc = float(re.sub(r'WorldBIG\d+,\d\d\d','',info[0]).replace(',',''))
                    marketCaps.append(mc)
                    break
    bndxDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    return bndxDF

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
    etf_price_data.to_csv('etf_price_data.csv',index=False)

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
