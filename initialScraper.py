import requests
from bs4 import BeautifulSoup
import re
import io
import pandas as pd
import time
from pdftotext import PDF
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver_loc = '/Users/avinaashkoganti/chromedriver'

#Scraping Index for VTI
marketCaps = []
dates = []
r = requests.get("http://www.crsp.org/fact-sheet-archive")
soup = BeautifulSoup(r.text,features="html.parser")
for link in soup.find_all('a'):
    if re.search('crsptm', str(link.get('href')), re.IGNORECASE):
        pdf = requests.get(link.get('href'))
        open_pdf = io.BytesIO(pdf.content)
        read_pdf = PDF(open_pdf)[1]
        dates.append(link.text.replace('Quarter Ending ', ''))
        marketCaps.append(float(re.findall('INDEX MARKET CAP\s+\d+,\d+,\d+', read_pdf, re.IGNORECASE)[0].upper().replace('INDEX MARKET CAP','').replace(',',''))/1000)
vtiDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps}).sort_values(by='date').reset_index(drop=True)
vtiDF.to_csv('Data/vti_MC_data.csv',index=False)
print("VTI")
print(vtiDF)

#Scraping Index for VXUS
dates = []
marketCaps = []
links = []
driver = webdriver.Chrome(driver_loc,options=options)
driver.get('https://www.ftserussell.com/analytics/factsheets/home/search')
archive = driver.find_element_by_xpath('//a[@title="FTSE Global All Cap ex US Index"]/following-sibling::a')
driver.execute_script("arguments[0].click();", archive)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()
div = soup.find("h4", string="FTSE Global All Cap ex US Index").parent
for li in div.find('ul').findAll('li'):
    links.append(li.find('a',href=True)['href'])
links.append(BeautifulSoup(requests.get('https://www.ftserussell.com/analytics/factsheets/home/search').text,features="html.parser").find('a',{'title':'FTSE Global All Cap ex US Index'})['href'])
for link in links:
    pdf = requests.get(link)
    open_pdf = io.BytesIO(pdf.content)
    read_pdf = PDF(open_pdf)
    dates.append(re.sub('Dataasat:','',re.findall('Dataasat:\d+\S+\d+', re.sub(' ','',read_pdf[0]), re.IGNORECASE)[0]))
    marketCaps.append(float(re.sub('Totals\s+\d+\s+','',re.findall('Totals\s+\d+\s+\d+,\d+,\d+', read_pdf[1], re.IGNORECASE)[0]).replace(',',''))/1000)
vxusDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps}).sort_values(by='date').reset_index(drop=True)
vxusDF.to_csv('Data/vxus_MC_data.csv',index=False)
print("VXUS")
print(vxusDF)

#Scraping Index for BND
dates = []
marketCaps = []
links = []
driver = webdriver.Chrome(driver_loc,options=options)
driver.get('https://www.ftserussell.com/analytics/factsheets/home/search')
archive = driver.find_element_by_xpath('//a[@title="FTSE US Broad Investment-Grade Bond Index (USBIG®)"]/following-sibling::a')
driver.execute_script("arguments[0].click();", archive)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()
div = soup.find("h4", string="FTSE US Broad Investment-Grade Bond Index (USBIG®)").parent
for li in div.find('ul').findAll('li'):
    links.append(li.find('a',href=True)['href'])
links.append(BeautifulSoup(requests.get('https://www.ftserussell.com/analytics/factsheets/home/search').text,features="html.parser").find('a',{'title':'FTSE US Broad Investment-Grade Bond Index (USBIG®)'})['href'])
for link in links:
    pdf = requests.get(link)
    open_pdf = io.BytesIO(pdf.content)
    read_pdf = PDF(open_pdf)[0]
    dates.append(re.sub('FTSE Russell Factsheet\s\S\s','',re.findall('FTSE Russell Factsheet\s\S\s\w+ \d+, \d+', read_pdf, re.IGNORECASE)[0]))
    marketCaps.append(float(re.sub('USBIG\s+\d+,\d+\s+\d+,\d+.\d+\s+','',re.findall('USBIG\s+\d+,\d+\s+\d+,\d+.\d+\s+\d+,\d+.\d+', read_pdf, re.IGNORECASE)[0]).replace(',','')))
bndDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps}).sort_values(by='date').reset_index(drop=True)
bndDF.to_csv('Data/bnd_MC_data.csv',index=False)
print("BND")
print(bndDF)

#Scraping Index for BNDX
dates = []
marketCaps = []
links = []
driver = webdriver.Chrome(driver_loc,options=options)
driver.get('https://www.ftserussell.com/analytics/factsheets/home/search')
archive = driver.find_element_by_xpath('//a[@title="FTSE World Broad Investment-Grade Bond Index (WorldBIG)"]/following-sibling::a')
driver.execute_script("arguments[0].click();", archive)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()
div = soup.find("h4", string="FTSE World Broad Investment-Grade Bond Index (WorldBIG)").parent
for li in div.find('ul').findAll('li'):
    links.append(li.find('a',href=True)['href'])
links.append(BeautifulSoup(requests.get('https://www.ftserussell.com/analytics/factsheets/home/search').text,features="html.parser").find('a',{'title':'FTSE World Broad Investment-Grade Bond Index (WorldBIG)'})['href'])
for link in links:
    pdf = requests.get(link)
    open_pdf = io.BytesIO(pdf.content)
    read_pdf = PDF(open_pdf)[0]
    dates.append(re.sub('FTSE Russell Factsheet\s\S\s','',re.findall('FTSE Russell Factsheet\s\S\s\w+ \d+, \d+', read_pdf, re.IGNORECASE)[0]))
    marketCaps.append(float(re.sub('WorldBIG\s+\d+,\d+\s+\d+,\d+.\d+\s+','',re.findall('WorldBIG\s+\d+,\d+\s+\d+,\d+.\d+\s+\d+,\d+.\d+', read_pdf, re.IGNORECASE)[0]).replace(',','')))
bndxDF = pd.DataFrame({'date':pd.to_datetime(dates, infer_datetime_format=True),'Market Cap':marketCaps}).sort_values(by='date').reset_index(drop=True)
bndxDF['Market Cap'] = bndxDF['Market Cap'] - bndDF['Market Cap'] 
bndxDF.to_csv('Data/bndx_MC_data.csv',index=False)
print("BNDX")
print(bndxDF)