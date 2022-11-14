#from newsapi import NewsApiClient
#import pycountry

# you have to get your api key from newapi.com and then paste it below
# newsapi = NewsApiClient(api_key='6d74523f498e43409389d24e10ae2c37')

#https://libguides.wlu.edu/c.php?g=357505&p=2412837

import requests
from selenium import webdriver
from bs4 import BeautifulSoup

def bbs():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find('body').find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor', href=True)
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text').text.strip()
        print(stext, slink)

def abcnews():
    url = 'https://abcnews.go.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas=soup.find('body').find_all('a', class_='AnchorLink VideoTile', href=True)
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h3',class_='VideoTile__Title').text.strip()
        print (stext,slink)
    datas = soup.find('body').find_all('a', class_='AnchorLink News__Item external flex flex-row', href=True)
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h2', class_='News__Item__Headline enableHeadlinePremiumLogo').text.strip()
        print(stext, slink)
    datas = soup.find('body').find_all('a', class_='AnchorLink',attrs={"tabindex": "0"}, href=True)
    for i, x in enumerate(datas):
        if (x.text!=''):
            slink = x.attrs['href']
            if (slink[0] == '/'):
                slink = url + slink;
            stext = x.text.strip()
            print(stext, slink)

def cnn():
    browser = webdriver.Chrome()
    url = "https://edition.cnn.com"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source)
    datas = soup.find_all('h3',class_='cd__headline')
    for i, x in enumerate(datas):
        stext = x.text.strip()
        slink = x.findNext('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        print (stext,slink)

def buzzfeed():
    url = 'https://www.buzzfeed.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_="feedItem_smallTitle__KLfqG")
    for i, x in enumerate(datas):
        slink = x.parent.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        print(stext, slink)
    datas = soup.find_all('h2', class_="feedItem_title__0_9qB")
    for i, x in enumerate(datas):
        slink = x.parent.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        print(stext, slink)

def dmail():
    url = 'https://www.dailymail.co.uk/ushome/index.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='linkro-darkred')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= tegData.text.strip()
        print(stext, slink)
    datas = soup.find_all('span', class_='pufftext')
    for i, x in enumerate(datas):
        slink = x.find_parent('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= x.findNext('span', class_='arrow-small-r').findNext('strong').text.strip()
        print(stext, slink)


#bbs()
#abcnews()
#buzzfeed()
#dmail()
