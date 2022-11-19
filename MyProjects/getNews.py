#from newsapi import NewsApiClient
#import pycountry

# you have to get your api key from newapi.com and then paste it below
# newsapi = NewsApiClient(api_key='6d74523f498e43409389d24e10ae2c37')

#https://libguides.wlu.edu/c.php?g=357505&p=2412837

import requests
from selenium import webdriver
from selenium.common import InvalidSelectorException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

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


def mirror():
    browser = webdriver.Chrome()
    url = "https://www.mirror.co.uk/news/"
    browser.get(url)
    try:
        button = browser.find_element(By.XPATH,'#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-78i25x')
        button.click()
    except InvalidSelectorException as e:
        print('Не найдена кнопка активации')

    soup = BeautifulSoup(browser.page_source)
    datas = soup.find_all('div', class_='story__title')
    for i, x in enumerate(datas):
        tegData = x.findNext('h2')
        stext = tegData.text.strip()
        slink = x.find_parent('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        print(stext, slink)
    browser.close()


def washingtonpost():
    url = 'https://www.washingtonpost.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='relative left font--headline font-bold font-size-sm')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= tegData.findNext('span').text.strip()
        print(stext, slink)

def foxnews():
    url = 'https://www.foxnews.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='title title-decoration-default')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= tegData.text.strip()
        print(stext, slink)
    datas = soup.find_all('h2', class_='title')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = tegData.text.strip()
        print(stext, slink)

def techcrunch():
    url = 'https://techcrunch.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h3', class_='mini-view__item__title')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.findNext('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= tegData.text.strip()
        print(stext, slink)
    datas = soup.find_all('header', class_='post-block__header')
    for i, x in enumerate(datas):
        tegData = x.findNext('h2', class_='post-block__title')
        slink = tegData.findNext('a', class_='post-block__title__link').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.findNext('div', class_='post-block__content').text.strip()
        print(stext, slink)
#<header class="post-block__header"><div class="article__primary-category"><a class="article__primary-category__link gradient-text gradient-text--green-gradient" href="/category/venture/">Venture</a></div><h2 class="post-block__title"><a class="post-block__title__link" href="/2022/11/18/drive-capitals-investors-hit-a-fork-in-the-road/">Drive Capital’s investors reach a fork in the road</a></h2><div class="post-block__meta"><div class="river-byline"><span class="river-byline__authors"><span><a aria-label="Posts by Connie Loizos" href="/author/connie-loizos/">Connie Loizos</a></span></span><div class="river-byline__full-date-time__wrapper"><time class="river-byline__full-date-time" datetime="2022-11-19T05:29:19">8:29 AM GMT+3<span class="full-date-time__separator">•</span>November 19, 2022</time></div></div></div></header>
#<article class="post-block post-block--image post-block--unread river-enter-active"><header class="post-block__header"><div class="article__primary-category"><a class="article__primary-category__link gradient-text gradient-text--green-gradient" href="/category/venture/">Venture</a></div><h2 class="post-block__title"><a class="post-block__title__link" href="/2022/11/18/drive-capitals-investors-hit-a-fork-in-the-road/">Drive Capital’s investors reach a fork in the road</a></h2><div class="post-block__meta"><div class="river-byline"><span class="river-byline__authors"><span><a aria-label="Posts by Connie Loizos" href="/author/connie-loizos/">Connie Loizos</a></span></span><div class="river-byline__full-date-time__wrapper"><time class="river-byline__full-date-time" datetime="2022-11-19T05:29:19">8:29 AM GMT+3<span class="full-date-time__separator">•</span>November 19, 2022</time></div></div></div></header><div class="post-block__content">Drive Capital was founded by two former Sequoia Capital Partners looking to start anew in the Midwest. But investors in the Columbus, Oh.-based firm have had a bumpy ride of late, and according to ...</div><footer class="post-block__footer"><figure class="post-block__media"><picture><source srcset="https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=100&amp;h=53&amp;crop=1 100w" media="(max-width: 380px)"><source srcset="https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=200&amp;h=107&amp;crop=1 200w" media="(max-width: 575px)"><source srcset="https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=430&amp;h=230&amp;crop=1 430w" media="(min-width: 576px)"><img alt="" sizes="(min-width: 1024px) 430px, 100vw" src="https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=430&amp;h=230&amp;crop=1" srcset="https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=100&amp;h=53&amp;crop=1 100w, https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=200&amp;h=107&amp;crop=1 200w, https://techcrunch.com/wp-content/uploads/2016/11/gettyimages-157429059.jpg?w=430&amp;h=230&amp;crop=1 430w"></picture></figure></footer></article>

#bbs()
#abcnews()
#buzzfeed()
#dmail()
#mirror()
#washingtonpost()
#foxnews()
techcrunch()