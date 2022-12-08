#from newsapi import NewsApiClient
#import pycountry

# you have to get your api key from newapi.com and then paste it below
# newsapi = NewsApiClient(api_key='6d74523f498e43409389d24e10ae2c37')

import logging
import random
import time
import traceback
from datetime import date

import psycopg2
import requests
import telegram
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
from selenium.common import InvalidSelectorException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import ParseMode
import os
import secur

logging.basicConfig(filename=f'getNews{date.today().strftime("%Y%m%d")}.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def set_conn():
    secur1 = secur.get_connect()
    conn = psycopg2.connect(dbname=secur1['dbname'], user=secur1['user'],
                            password=secur1['password'], host=secur1['host'])
    return conn


def translate(stext,lfrom, lto):
    try:
        translator = Translator()
        translated = translator.translate(stext, src=lfrom, dest=lto)
        return translated.text
    except Exception as e:
        serr = f'Error: {traceback.format_exc()} text: {stext}'
        logging.error('%s raised an error', serr)
        return ''

#p = translate('Są prodziekani, którzy osobiście przywożą studentów na konsultacje psychologiczne','pl','ru')
#print(p)

options = Options();
options.add_argument("--disable-extensions");
options.add_argument("test-type");
options.add_argument("--ignore-certificate-errors");
options.add_argument("no-sandbox");
options.add_argument("--headless");

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
        serr = f'Error: {traceback.format_exc()} text: {sorigin_text}'
        logging.error('%s raised an error', serr)

data_list = []

def ins_to_data(rus_text,origin_text, eng_text, link, surl, lang):
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
        rus_text = translate(origin_text, lang, 'ru')
        eng_text = translate(origin_text, lang, 'en')
        sorigin_text = origin_text
    else:
        bload = False
    if bload and rus_text!= '' and rus_text!= None:
        bload = len(rus_text.split(' '))>4
    if bload:
        data_list.append((rus_text,sorigin_text, eng_text, link, surl, lang))

def ins_to_db():
    try:
        conn = set_conn();
        cur = conn.cursor()
        for data in data_list:
            cur.execute('select public.ins_t_news_data(%s, %s, %s, %s, %s) as val', (data[0],data[1], data[2], data[3], data[4]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        serr = f'Error: {traceback.format_exc()} text: {sorigin_text}'
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
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text').text.strip()
        #print(stext, slink)
        ins_to_data('',stext, stext, slink, url,'en')

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
        ins_to_data('',stext, stext, slink, url,'en')
    datas = soup.find('body').find_all('a', class_='AnchorLink News__Item external flex flex-row', href=True)
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('h2', class_='News__Item__Headline enableHeadlinePremiumLogo').text.strip()
        ins_to_data('',stext, stext, slink, url,'en')
    datas = soup.find('body').find_all('a', class_='AnchorLink',attrs={"tabindex": "0"}, href=True)
    for i, x in enumerate(datas):
        if (x.text!=''):
            slink = x.attrs['href']
            if (slink[0] == '/'):
                slink = url + slink;
            stext = x.text.strip()
            ins_to_data('',stext, stext, slink, url,'en')

def cnn():
    browser = webdriver.Chrome(options=options)
    url = "https://edition.cnn.com"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source)
    datas = soup.find_all('h3',class_='cd__headline')
    for i, x in enumerate(datas):
        stext = x.text.strip()
        slink = x.findNext('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        #print (stext,slink)
        ins_to_data('', stext, stext, slink, url, 'en')

def buzzfeed():
    url = 'https://www.buzzfeed.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_="feedItem_smallTitle__KLfqG")
    for i, x in enumerate(datas):
        slink = x.parent.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')
    datas = soup.find_all('h2', class_="feedItem_title__0_9qB")
    for i, x in enumerate(datas):
        slink = x.parent.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')

def dmail():
    url = 'https://www.dailymail.co.uk/ushome/index.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='linkro-darkred')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext= tegData.text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')
    datas = soup.find_all('span', class_='pufftext')
    for i, x in enumerate(datas):
        slink = x.find_parent('a').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext= x.findNext('span', class_='arrow-small-r').findNext('strong').text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')


def mirror():
    browser = webdriver.Chrome(options=options)
    url = "https://www.mirror.co.uk/news/"
    browser.get(url)
    time.sleep(3)
    try:
        button = browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/button[2]')
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
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')
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
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')

def foxnews():
    url = 'https://www.foxnews.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('h2', class_='title title-decoration-default')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext= tegData.text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')
    datas = soup.find_all('h2', class_='title')
    for i, x in enumerate(datas):
        tegData = x.findNext('a')
        slink = tegData.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = tegData.text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')

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
        #print(stext, slink)
        ins_to_data('', stext, stext, slink, url, 'en')
    datas = soup.find_all('header', class_='post-block__header')
    for i, x in enumerate(datas):
        tegData = x.findNext('h2', class_='post-block__title')
        slink = tegData.findNext('a', class_='post-block__title__link').attrs['href']
        if (slink[0] == '/'):
            slink = url + slink
        stext = x.findNext('div', class_='post-block__content').text.strip()
        #print(stext, slink)
        ins_to_data( '', stext, stext, slink, url, 'en')

def meduza():
    url = 'https://meduza.io/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='Link-root Link-isInBlockTitle')
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
                ins_to_data( stext, stext, '', slink, url, 'ru')

def kommersant():
    url = 'https://www.kommersant.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='uho__link uho__link--overlay')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_data( stext, stext, '', slink, url, 'ru')

def unian():
    url = 'https://www.unian.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='list-news__title')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_data( stext, stext, '', slink, url, 'ru')
    datas = soup.find_all('a', class_='main-publication__text')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_data( stext, stext, '', slink, url, 'ru')

def svpressa():
    url = 'https://svpressa.ru/?utm_source=vsesmi_online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='b-article__title')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink)
        ins_to_data( stext, stext, '', slink, url, 'ru')

def iz():
    browser = webdriver.Chrome(options=options)
    url = "https://iz.ru/?utm_source=vsesmi_online"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    datas = soup.find_all('a', class_='two-infographic-block__item__inside__info')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('span').text.strip()
        if stext != '':
            #print(stext, slink)
            ins_to_data( stext, stext, '', slink, url, 'ru')
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
                ins_to_data( stext, stext, '', slink, url, 'ru')
    browser.close()

def rg():
    url = 'https://rg.ru/?utm_source=vsesmi_online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('a', class_='ItemOfListStandard_title__eX0Jw')+\
            soup.find_all('a', class_='NewsFeedItemAccent_link__B7ive')+ \
            soup.find_all('a', class_='PageIndexContentSecondSpiegelListPattern_title__lWoOM') + \
            soup.find_all('a', class_='NewsFeedItem_link__4XiJ_')

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
            ins_to_data( stext, stext, '', slink, url, 'ru')

def ukr():
    browser = webdriver.Chrome(options=options)
    url = "https://www.ukr.net/news/main.html?utm_source=vsesmi_online"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    datas = soup.find_all('a', class_='im-tl_a')
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink,'ukr')
        ins_to_data( '', stext, '', slink, url, 'uk')
    browser.close()

def hotnews():
    browser = webdriver.Chrome(options=options)
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
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.text.strip()
        #print(stext, slink, 'rom')
        ins_to_data( '', stext, '', slink, url, 'ro')
    browser.close()

def gazeta():
    browser = webdriver.Chrome(options=options)
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
    for i, x in enumerate(datas):
        slink = x.attrs['href']
        if (slink[0] == '/'):
            slink = url + slink;
        stext = x.findNext('div',class_="article__title").text.strip()
        #print(stext, slink, 'pl')
        ins_to_data( '', stext, '', slink, url, 'pl')
    browser.close()

def svpressa():
    url = 'https://oxu.az/?utm_source=vsesmi_online'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    datas = soup.find_all('div', class_='news-i')
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
            ins_to_data( '', stext, '', slink, url, 'az')


def read_all():
    news = [bbs,abcnews,buzzfeed,dmail,mirror,washingtonpost,foxnews,techcrunch,meduza,kommersant,unian,svpressa,iz,rg,ukr,hotnews,gazeta,svpressa]
    #news = [svpressa]
    for fnc in news:
        try:
            fnc();
        except:
            serr = f'Error: {traceback.format_exc()}'
            logging.error('%s raised an error', serr)
    ins_to_db()

def show_news():
    conn = set_conn()
    ssql = """select id,rus_text,origin_text,eng_text,link,surl, to_char(sdate,'dd.mm.yyyy') sdate,substring(surl from '^(?:http:\/\/|www\.|https:\/\/)([^\/]+)') substrurl
                from datas.t_news_data
                where sdate::date=(select max(sdate::date) from datas.t_news_data)
                and coalesce(showed,false) = false
                order by random() limit 10"""
    cur = conn.cursor()
    cur.execute(ssql)
    res = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return res

# ьот
#newsWhouseBot


# Токен, который выдает @botfather
def run_bot():
    secur2 = secur.get_bot();
    bot = telegram.Bot(secur2['Bot'])
    # Адрес телеграм-канала, начинается с @
    CHANNEL_NAME = secur2['CHANNEL_NAME']
    while True:
        try:
            cur_news =show_news()
            if len(cur_news) == 0 or (time.strftime("%H") in ('7')):
                read_all()
            conn = set_conn()
            cur = conn.cursor()
            conn.autocommit = True
            for new in cur_news:
                #mess = f'<table><tr style="color:#B22222"><th><a href={new[4]}>{new[1]}</a></th></tr><tr style="color:#0000ff"><td>{new[2]}<td></tr></table>'
                if new[2] == new[1]:
                    mess = f'<b><i>{new[6]}: </i>{new[7]}</b>\n<a href="{new[4]}">{new[1]}</a>'
                else:
                    mess = f'<b><i>{new[6]}: </i>{new[7]}</b>\n<a href="{new[4]}">{new[1]}</a>\n{new[2]}'
                bot.send_message(chat_id=CHANNEL_NAME, text=mess,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
                #bot.send_message(chat_id=CHANNEL_NAME, text='fgfg')
                nid = new[0]
                cur.execute("update datas.t_news_data set showed = true where id=%s", [nid])
                wait = random.randint(100,500)
                time.sleep(20)
            cur.close()
            conn.close()
            time.sleep(600)
        except Exception as e:
            serr = f'Error: {traceback.format_exc()} text: {mess}'
            logging.error('%s raised an error', serr)
            break

#run_bot()
gazeta()


