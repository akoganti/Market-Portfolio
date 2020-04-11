import requests
from bs4 import BeautifulSoup
import re
import io
import PyPDF2
import pandas as pd

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