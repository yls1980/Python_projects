file = open("smail.txt", 'r',encoding='utf-8')
sdata = file.read()
smails = sdata.split(';')
file.close()

import smtplib, ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(maddres):
    smtp_server = "smtp.mail.ru"
    port = 465  # For starttls
    sender_email = "y_skorkin@mail.ru"
    password = "ckfdfckfdeirf"
    message = "Здравствуйте. Подскажите пожалуйста в ваш лагерь можно отправить на отдых слабовидящего ребенка?"
    subject = "Вопрос о путевке"

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = maddres
    msg['Disposition-Notification-To'] = sender_email
    msg.attach(MIMEText(message, 'plain'))

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        #server.ehlo()  # Can be omitted
        #server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, maddres, msg.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

for smail in smails:
    #print (smail)
    send_mail(smail)