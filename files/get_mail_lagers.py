#import requests
#from bs4 import BeautifulSoup

#response = requests.get('https://rate.mosgortur.ru/u-morya.htm')
#soup = BeautifulSoup(response.text, 'lxml')
#items = soup.find_all('div', class_='showModal')
#print (items)
#for item in items:
#    itemHtml = item.find('href').text
#    print(itemHtml)

from selenium import webdriver
from validate_email import validate_email
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
#options = Options()
#options.binary_location = r"chromedriver.exe"
# This line defines your Chromium exe file location.
driver = webdriver.Edge(executable_path=r'msedgedriver.exe')
driver1 = webdriver.Edge(executable_path=r'msedgedriver.exe')

file = open("smail.txt", 'w',encoding='utf-8')
file1 = open("other.txt", 'w',encoding='utf-8')
lagers = ["https://rate.mosgortur.ru/u-morya.htm","https://rate.mosgortur.ru/u-vodoema.htm","https://rate.mosgortur.ru/ne-u-vodoema.htm"]
for htmls in lagers:
    driver.get(htmls)
    elems = driver.find_elements_by_class_name('showModal')
    #elems = driver.find_elements_by_xpath('/html/body/div[1]/main/div/div/div[3]/div[*]/div[3]/a')
    for elem in elems:
        try:
            href = elem.get_attribute('href')
            driver1.get(href)
            emails = driver1.find_element_by_xpath('//*[@id="modal_info"]/table/tbody/tr[3]/td/a').text
            try:
                ssite = driver1.find_element_by_xpath('//*[@id="modal_info"]/table/tbody/tr[4]/td/a').text
            except:
                ssite=''
            try:
                saddr = driver1.find_element_by_xpath('//*[@id="modal_info"]/table/tbody/tr[1]/td').text
            except:
                saddr=''
            try:
                sname = driver1.find_element_by_xpath('//*[@id="modalRatioLabel"]').text
            except:
                sname=''

            lznak = ','
            if emails.find(';')!=-1:
                lznak = ';'
            elif emails.find(',')!=-1:
                lznak = ';'
            elif emails.find(' ') != -1:
                lznak = ' '
            for email in emails.split(lznak):
                is_valid = validate_email(email,verify=True)
                if is_valid:
                    file.write(f"{email};")
                    file1.write(f"{sname}|{ssite}|{saddr}|{email}\n")
            print (f"{href} - ok")
        except Exception as e:
            print(f"Ошибка: {e} {href}")
    print(f"{htmls} - Сделал")
file.close()
file1.close()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
driver.close()

#<a class="showModal" data-target="#modalInfo" href="/camp1.htm">Государственное предприятие «Международный детский центр «Артек»</a>
#/html/body/div[1]/main/div/div/div[3]/div[1]/div[3]/a