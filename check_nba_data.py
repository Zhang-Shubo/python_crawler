#import moudules

import requests
from lxml import html
from scraping_nba_data import Render

#import email moudule
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from datetime import datetime,time,date,timedelta
import time

import threading

#set hupu url
URL_HUPU = 'https://nba.hupu.com/games'


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

def search_game_data(r):
    #get nba today games data

    #set encoding format
    r.encoding = 'UTF-8'
    result = r.frame.toHtml()
    tree = html.fromstring(result)
    #look the requests results text
    #print(r.text)
    #search the games data
    em_score_zhu = tree.xpath('//div[@class = "gamecenter_livestart"]//\
     div[@class = "list_box"]//div[@class = "team_vs_a_1 clearfix"]//\
     div[@class = "txt"]/span')
    em_name_zhu = tree.xpath('//div[@class = "gamecenter_livestart"]//\
     div[@class = "list_box"]//div[@class = "team_vs_a_1 clearfix"]//\
     div[@class = "txt"]/span/a')
    em_score_ke = tree.xpath('//div[@class = "gamecenter_livestart"]//\
     div[@class = "list_box"]//div[@class = "team_vs_a_2 clearfix"]//\
     div[@class = "txt"]/span')
    em_name_ke = tree.xpath('//div[@class = "gamecenter_livestart"]//\
     div[@class = "list_box"]//div[@class = "team_vs_a_2 clearfix"]//\
     div[@class = "txt"]/span/a')
    
    name_zhu = []
    score_zhu = []
    name_ke = []
    score_ke = []
    
    #store game data into list
    for i in range(len(em_name_zhu)):
        score_zhu.append(em_score_zhu[2*i].text)
        name_zhu.append(em_name_zhu[i].text)   
        score_ke.append(em_score_ke[2*i].text)
        name_ke.append(em_name_ke[i].text)   

    return name_zhu,score_zhu,name_ke,score_ke

def email_text(name_zhu,score_zhu,name_ke,score_ke):
    sta = '<html><body><table>'
    end = '</html></body></table>'
    
    cnt =len(name_zhu)
    sheet = ''
    for i in range(cnt):
        sheet += '<tr><th>'+str(i)+'</th><th>'+name_zhu[i]+ '</th><th>'+name_ke[i]+'</th></tr>'
        sheet += '<tr><td>'+'score'+'</td><td>'+score_zhu[i]+ '</td><td>'+score_ke[i]+'</td></tr>'
        
    return sta+sheet+end

def send_email(content):
    #set email content
    subject = 'NBA games data'
    
    msg = MIMEText(content,'html','utf-8')
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

def task(r):
    
    login_net()
    #init time
    now = datetime.now()
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    print('now:',str_now)
    
    name_zhu,score_zhu,name_ke,score_ke = search_game_data(r)

    content = email_text(name_zhu,score_zhu,name_ke,score_ke)
    send_email(content)
    
if __name__ == "__main__":
    
    
    while(True): 
        r = Render(URL_HUPU)
    
        timer = threading.Timer(3600,task,[r])
        timer.start()
        
        r._loadFinished()
        del r
