import requests
from bs4 import BeautifulSoup
import re
import io
import PyPDF2
import pandas as pd
import datetime
import time

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
                market_cap = int(re.findall('INDEX MARKET CAP\d+,\d+,\d+', page_text, re.IGNORECASE)[0].upper().replace('INDEX MARKET CAP','').replace(',',''))/1000
            except:
                try:
                    page_text = pdf_page2.extractText().replace('\n','')
                    market_cap = int(re.findall('INDEX MARKET CAP\d+,\d+,\d+', page_text, re.IGNORECASE)[0].upper().replace('INDEX MARKET CAP','').replace(',',''))/1000
                except:
                    market_cap = 'n/a'
            marketCaps.append(market_cap)
    vtiDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    vtiDF.to_csv('Data/vti_MC_data.csv',index=False)

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
                        mc = mc[0].replace(',','').replace('\n','').replace('Totals','')
                        mc = [int(s) for s in mc.split() if s.isdigit()][1] / 1000
                        marketCaps.append(mc)
                    break
    vxusDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    vxusDF.to_csv('Data/vxus_MC_data.csv',index=False)

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
    bndDF.to_csv('Data/bnd_MC_data.csv',index=False)

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
    bndxDF.to_csv('Data/bndx_MC_data.csv',index=False)
