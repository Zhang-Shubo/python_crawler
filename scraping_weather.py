#import moudules

import requests
from lxml import html
import selenium

#import email moudule
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from datetime import datetime,time,date,timedelta
import time

import threading

#set weather url
WEATHER_URL = "http://www.weather.com.cn/weather1d/101010100.shtml"

#set email sender account
sender = '591583861@qq.com'
sender_pwd = 'ewxgyrkwoahubbhi'
receiver = 'supozhang@126.com'

smtpserver = 'smtp.qq.com'

#login THUNET
def login_net():
    THUNET_URL = "http://net.tsinghua.edu.cn/wired/"
    THUNET_LOGIN = "http://net.tsinghua.edu.cn/do_login.php"

    data = {
        'action':'login',
        'username':'yj-chen16',
        'password':'{MD5_HEX}32bf6336155a6f5e06f43260aaebd425',
        'ac_id':'1'
    }

    requests.post(THUNET_LOGIN,data = data)

def search_wea_data():
    #create requests session
    s = requests.session()
    r = s.get(WEATHER_URL)

    #set encoding format
    r.encoding = 'UTF-8'

    #look the requests results text
    #print(r.text)
    #search the weather data
    tree = html.fromstring(r.text)
    el = tree.xpath('//input[@id="hidden_title"]')[0]
    today_weather = el.values()[2]

    return today_weather

def send_email(today_weather):
    #set email content
    subject = '今天的天气'
    content = today_weather

    msg = MIMEText('<html><h1>'+today_weather+'</h1></html>','html','utf-8')
    msg['Subject'] = Header(subject,'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    try:
        s = smtplib.SMTP_SSL(smtpserver,465)
        s.login(sender,sender_pwd)
        s.sendmail(sender,receiver,msg.as_string())
        print('Send successful!')

    except smtplib.SMTPException as e:
        print('Send Faail!',e)

    finally:
        s.quit()

def task():

    login_net()
    #init time
    now = datetime.now()
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    print('now:',str_now)

    today_weather = search_wea_data()
    send_email(today_weather)

    global timer
    timer = threading.Timer(14400,task)
    timer.start()

if __name__ == "__main__":

    timer = threading.Timer(13500,task)
    timer.start()
