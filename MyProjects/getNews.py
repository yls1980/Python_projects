#from newsapi import NewsApiClient
#import pycountry

# you have to get your api key from newapi.com and then paste it below
# newsapi = NewsApiClient(api_key='6d74523f498e43409389d24e10ae2c37')

#https://libguides.wlu.edu/c.php?g=357505&p=2412837
import sys

import requests
from selenium import webdriver
from selenium.common import InvalidSelectorException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import psycopg2
from googletrans import Translator
import logging
from datetime import date

def set_conn():
    conn = psycopg2.connect(dbname='zorrodb', user='zorropg',
                            password='rjnjhsq1980', host='168.232.165.10')
    return conn


def translate(stext,lfrom, lto):
    try:
        translator = Translator()
        translated = translator.translate(stext,  src=lfrom, dest=lto)
        return translated.text
    except Exception as e:
        serr = 'Ошибка в строке {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__+';'+e
        logging.error('%s raised an error', serr)
        return ''

def ins_to_db(conn, rus_text,origin_text, eng_text, link, surl, lang):
    try:
        sorigin_text = origin_text
        bload = True
        if (rus_text!='' and eng_text==''):
            eng_text = translate(rus_text, 'ru','en')
            sorigin_text = rus_text
        elif (rus_text=='' and eng_text!=''):
            rus_text = translate(eng_text, 'en', 'ru')
            sorigin_text = eng_text
        elif (rus_text != '' and eng_text !=''):
            sorigin_text = rus_text
        elif (rus_text == '' and eng_text =='' and origin_text!=''):
            rus_text = translate(eng_text, lang, 'ru')
            eng_text = translate(eng_text, lang, 'en')
            sorigin_text = origin_text
        else:
            bload = False
        if bload:
            cur = conn.cursor()
            cur.execute('select public.ins_t_news_data(%s, %s, %s, %s, %s) as val', (rus_text,sorigin_text, eng_text, link, surl))
            conn.commit()
            cur.close()
    except Exception as e:
        serr = 'Ошибка в строке {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__+';'+e
        logging.error('%s raised an error', serr)


def ins_text(rus_text,sorigin_text, eng_text, link, surl):
    conn = set_conn();
    ins_to_db(conn, rus_text,sorigin_text, eng_text, link, surl)
    conn.close()

#prus_text text,
#     porigin_text text,
#     peng_text text,
#     plink text,
#     psurl text)




def bbs():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find('body').find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor', href=True)
    conn = set_conn();
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text').text.strip()
        #print(stext, slink)
        ins_to_db(conn,'',stext, stext, slink, url,'en')
    conn.close()

def abcnews():
    url = 'https://abcnews.go.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas=soup.find('body').find_all('a', class_='AnchorLink VideoTile', href=True)
    conn = set_conn();
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h3',class_='VideoTile__Title').text.strip()
        ins_to_db(conn,'',stext, stext, slink, url,'en')
    datas = soup.find('body').find_all('a', class_='AnchorLink News__Item external flex flex-row', href=True)
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h2', class_='News__Item__Headline enableHeadlinePremiumLogo').text.strip()
        ins_to_db(conn,'',stext, stext, slink, url,'en')
    datas = soup.find('body').find_all('a', class_='AnchorLink',attrs={"tabindex": "0"}, href=True)
    for i, x in enumerate(datas):
        if (x.text!=''):
            slink = x.attrs['href']
            if (slink[0] == '/'):
                slink = url + slink;
            stext = x.text.strip()
            ins_to_db(conn,'',stext, stext, slink, url,'en')
    conn.close()

def cnn():
    browser = webdriver.Chrome()
    url = "https://edition.cnn.com"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source)
    datas = soup.find_all('h3',class_='cd__headline')
    conn = set_conn();
    for i, x in enumerate(datas):
        stext = x.text.strip()
        slink = x.findNext('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        #print (stext,slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    conn.close()

def buzzfeed():
    url = 'https://www.buzzfeed.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_="feedItem_smallTitle__KLfqG")
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.parent.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    datas = soup.find_all('h2', class_="feedItem_title__0_9qB")
    for i, x in enumerate(datas):
        slink = x.parent.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    conn.close()

def dmail():
    url = 'https://www.dailymail.co.uk/ushome/index.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='linkro-darkred')
    conn = set_conn()
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext= tegData.text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    datas = soup.find_all('span', class_='pufftext')
    for i, x in enumerate(datas):
        slink = x.find_parent('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext= x.findNext('span', class_='arrow-small-r').findNext('strong').text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    conn.close()


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
    conn = set_conn()
    for i, x in enumerate(datas):
        tegData = x.findNext('h2')
        stext = tegData.text.strip()
        slink = x.find_parent('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    browser.close()
    conn.close()


def washingtonpost():
    url = 'https://www.washingtonpost.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='relative left font--headline font-bold font-size-sm')
    conn = set_conn()
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= tegData.findNext('span').text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    conn.close()

def foxnews():
    url = 'https://www.foxnews.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='title title-decoration-default')
    conn = set_conn()
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext= tegData.text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    datas = soup.find_all('h2', class_='title')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = tegData.text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    conn.close()

def techcrunch():
    url = 'https://techcrunch.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h3', class_='mini-view__item__title')
    conn = set_conn()
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.findNext('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext= tegData.text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    datas = soup.find_all('header', class_='post-block__header')
    for i, x in enumerate(datas):
        tegData = x.findNext('h2', class_='post-block__title')
        slink = tegData.findNext('a', class_='post-block__title__link').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.findNext('div', class_='post-block__content').text.strip()
        #print(stext, slink)
        ins_to_db(conn, '', stext, stext, slink, url, 'en')
    conn.close()

def meduza():
    url = 'https://meduza.io/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='Link-root Link-isInBlockTitle')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        datas_txt = x.find_all('span')
        texts =[]
        for j, y in enumerate(datas_txt):
            try:
                texts.append(y.text.strip())
            except:
                pass
            stext = '. '.join(texts)
            if stext!='':
                #print(stext, slink)
                ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    conn.close()

def kommersant():
    url = 'https://www.kommersant.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='uho__link uho__link--overlay')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    conn.close()

def unian():
    url = 'https://www.unian.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='list-news__title')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    datas = soup.find_all('a', class_='main-publication__text')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    conn.close()

def svpressa():
    url = 'https://svpressa.ru/?utm_source=vsesmi_online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='b-article__title')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    conn.close()

def iz():
    browser = webdriver.Chrome()
    url = "https://iz.ru/?utm_source=vsesmi_online"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    datas = soup.find_all('a', class_='two-infographic-block__item__inside__info')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('span').text.strip()
        if stext != '':
            #print(stext, slink)
            ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    datas = soup.find_all('a', class_='node__cart__item__inside url-box')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        datas_txt = x.find_all('div', class_="five-news-blocks__list__item__info__title text-style1 big_text title-box")+\
                    x.find_all('div', class_='quote-content quote-box')+\
                    x.find_all('div', class_='node__cart__item__inside__info__title small-title-style1 title-box')

        texts = []
        for j, y in enumerate(datas_txt):
            try:
                texts.append(y.findnext("span").text.strip())
            except:
                pass
            try:
                texts.append(y.findnext("div").text.strip())
            except:
                pass
            try:
                texts.append(y.text.strip())
            except:
                pass
            stext = '. '.join(texts)
            if stext != '':
                #print(stext, slink)
                ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    browser.close()
    conn.close()

def rg():
    url = 'https://rg.ru/?utm_source=vsesmi_online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='ItemOfListStandard_title__eX0Jw')+\
            soup.find_all('a', class_='NewsFeedItemAccent_link__B7ive')+ \
            soup.find_all('a', class_='PageIndexContentSecondSpiegelListPattern_title__lWoOM') + \
            soup.find_all('a', class_='NewsFeedItem_link__4XiJ_')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        texts = []
        try:
            texts.append(x.findnext("span").text.strip())
        except:
            pass
        try:
            texts.append(x.findnext("div").text.strip())
        except:
            pass
        try:
            texts.append(x.text.strip())
        except:
            pass
        stext = '. '.join(texts)
        if stext != '':
            #print(stext, slink)
            ins_to_db(conn, stext, stext, '', slink, url, 'ru')
    conn.close()

def ukr():
    browser = webdriver.Chrome()
    url = "https://www.ukr.net/news/main.html?utm_source=vsesmi_online"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    datas = soup.find_all('a', class_='im-tl_a')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink,'ukr')
        ins_to_db(conn, '', stext, '', slink, url, 'ua')
    browser.close()
    conn.clsoe()

def hotnews():
    browser = webdriver.Chrome()
    url = "https://www.hotnews.ro/"
    browser.get(url)
    time.sleep(3)
    try:
        button = browser.find_element(By.ID,'onetrust-accept-btn-handler')
        button.click()
    except InvalidSelectorException as e:
        print('Не найдена кнопка активации')
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    datas = soup.find_all('a', class_="snip")
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink, 'rom')
        ins_to_db(conn, '', stext, '', slink, url, 'ro')
    browser.close()
    conn.close()

def gazeta():
    browser = webdriver.Chrome()
    url = "https://www.gazeta.pl"
    browser.get(url)
    time.sleep(3)
    try:
        button = browser.find_element(By.ID,'onetrust-accept-btn-handler')
        button.click()
    except InvalidSelectorException as e:
        print('Не найдена кнопка активации')
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    datas = soup.find_all('a', class_="article")
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('div',class_="article__title").text.strip()
        #print(stext, slink, 'pl')
        ins_to_db(conn, '', stext, '', slink, url, 'pl')
    browser.close()
    conn.close()

def svpressa():
    url = 'https://oxu.az/?utm_source=vsesmi_online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('div', class_='news-i')
    conn = set_conn()
    for i, x in enumerate(datas):
        slink = x.findNext('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        try:
            stext = x.findNext('div', class_="title").text.strip()
        except:
            pass
        try:
            stext = x.findNext('div').text.strip()
        except:
            pass
        try:
            stext = x.text.strip()
        except:
            pass
        if stext != '':
            #print(stext, slink, 'az')
            ins_to_db(conn, '', stext, '', slink, url, 'az')
    conn.close()

logging.basicConfig(filename=f'getNews{date.today().strftime("%Y%m%d")}.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#bbs()
abcnews()
#buzzfeed()
#dmail()
#mirror()
#washingtonpost()
#foxnews()
#techcrunch()
#meduza()
#kommersant()
#unian()
#svpressa()
#iz()
#rg()
#ukr()
#hotnews()
#gazeta()
#svpressa()

