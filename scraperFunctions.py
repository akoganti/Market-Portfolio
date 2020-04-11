import requests
from bs4 import BeautifulSoup
import re
import io
import PyPDF2
import pandas as pd
import datetime

def vtiScraper():
    # Archive where all the index reports are
    vtiURL = "http://www.crsp.org/fact-sheet-archive"
    # Getting the urls for all VTI index reports and scraping date and market cap information
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
    # Saving information to dataframe
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
    # Saving information to dataframe
    vxusDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps})
    return vxusDF