#encoding=utf8
'''
Created on 2011-12-21

@author: chenggong
'''
import smtplib
import time
import ConfigParser
import logout


from email.mime.text import MIMEText

mailto_list=[]

def init():
    logout.log("normal","initing email helper")
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    fileName = cf.get("mails","maillist")
    file = open(fileName)
    for line in file:
        mailaddr=line.replace("\n","").replace("\r","")
        mailto_list.append(mailaddr)
        logout.log("normal","add email addr:%s"%mailaddr)
    

def send_mail(to_list,mail_host, mail_user, mail_pass, mail_postfix, sub,content):
    me="mis_videoworks@163.com"
    msg = MIMEText(content,_subtype='plain', _charset='gbk')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def sendEmail(emailStr):
    mail_host="smtp.163.com"
    mail_user="mis_videoworks@163.com"
    mail_pass="Abc123"
    mail_postfix="163.com"
    mail_subject = emailStr.decode('utf-8')
    stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    mail_content = stime + ":" + emailStr.decode('utf-8')
    return send_mail(mailto_list, mail_host, mail_user, mail_pass, mail_postfix, mail_subject, mail_content)
    
if __name__ == '__main__':
    init()
    print sendEmail("中文测试")
