import sys
import smtplib
import email
import time
import psycopg2
import pprint
import time
import logging
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from validate_email import validate_email

def mail_validate(sMail):
    is_valid = validate_email(sMail)
    return is_valid

logging.basicConfig(filename="i:\\Bases\\send.log", level=logging.INFO)
logging.info(datetime.datetime.now())

def smail(sto, pName):
    try:
        #name = "bardetbiedl"
        from_address = "help@bardetbiedl.ru"
        to_address = sto
        #subject = "Test"
        
        psName = ""
        if len(pName.strip())==0:
            psName= ", я "
        else:
            psName= " "+pName+", я "
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = "Прошу помощь"
        #<br><img src="cid:image1"><br>
        html = """
        <html>
          <head></head>
          <body>
            <p class="P3">Здравствуйте"""+psName+"""нашел ваш адрес в интернете. Извиняюсь, что обращаюсь.</p><p class="P3">Моя дочка - Алиса, сейчас ей 10 лет, теряет зрение. Множество исследований и процедур ничем не помогли. Она уже почти не видит то, что пишет, не видит, что написано в книжках. Врачи разводят руками. Есть подозрение, что у нее синдром Барде-Бидля. Если это правда, то она может потерять зрение к 20 годам или ранее. Нужны дорогостоящие генетические исследования. </p>
            <p class="P3">Требуются финансовые средства для реабилитации и поддержки, кроме того хотелось бы найти людей с подобными проблемами.</p><p class="P1"></p><p class="P3">Я сделал сайт bardetbiedl.ru для привлечения внимания к этому заболеванию людей в России.</p><p class="P3">Для желающих помочь:</p><p class="P2">карта сбербанка: <span class="T4">4276 3800 5226 9458 </span></p>
            <p class="P2">Карта Тинькоф: <span class="T4">5536 9137 9611 2411</span></p><p class="P2">Yandex кошелек: <span class="T4">41001554073970</span> <br>Спасибо.</br></p>      
          </body>
        </html>
        """
        #fp = open('/home/zorro/SITE/img123.jpg', 'rb')
        #msgImage = MIMEImage(fp.read())
        #fp.close()
        #msgImage.add_header('Content-ID', '<image1>')
        #body = """
        #Content-type: text/html
        #<br></br>
        #<h1><ПРИВЕТ></h1>
        #<ПРИВЕТ>    
        #""".format(name)
        
        body = MIMEText(html, 'html')
        msg.attach(body)    
        #msg.attach(msgImage)

        #msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com', 587)
        server.starttls()
        server.login("AKIAVWDLGH3YMEOAS7BW", "BD8eHuAYznYiYnj1J5SD+ZynZheXw/QEQxAmCtH74iCI")
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        return 1
    except Exception as ex:
        logging.error('Ошибка: %s' % (ex))
        return -1

    
#smail("help@bardetbiedl.ru")
conn = psycopg2.connect("postgres://yarik:rjnjhsq1980@127.0.0.1:5432/yarik")  
conn.autocommit=True
cursor = conn.cursor()  
updcur = conn.cursor()  
try:
	nRows = int(sys.argv[1])
except:
	nRows=2
cursor.execute('select id, first_nm, smail from public.t__all_data where status=0 limit '+str(nRows))  
rows = cursor.fetchall()  
s=0
#file = open("i:\Bases\send.log","w", encoding="utf-8") 
for i in rows:
	sMail= i[2]
	sName= i[1]
	var=int(i[0])
	s+=1
	stat = 0
	if mail_validate(sMail):
		stat = smail(sMail, sName)
	else:
		stat=-2
	str = "%i stat=%i sNmae=%s sMail=%s" % (s, stat, sName, sMail)
	logging.info(str)
    #print(str)
    #file.write(str) 
	updcur.execute('UPDATE public.t__all_data SET status = %s WHERE id = %s' , (stat,var))	
	time.sleep(1)

    
#file.close()    
updcur.close()
cursor.close()
conn.commit()
conn.close()   
dt = "конец: %s" % (datetime.datetime.now())	
logging.info(dt)