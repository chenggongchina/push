#encoding=utf8
'''
Created on 2012-8-10

@author: chenggong
'''
import uuid
import os

import ConfigParser
import logout
phonelist = []

def init():
    logout.log("normal","initing message helper")
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    fileName = cf.get("message","phonelist")
    f = open(fileName)
    for line in f:
        if(line[0]=="#"):
            continue
        num= line.replace("\n","").replace("\r","")
        if(len(num)!=11): 
            logout.log("error","error phone number:%s"%num)
            continue
        phonelist.append(num)
        logout.log("normal","add phone number:%s"%num)
    f.close()

def sendmsg(phone,msg):
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    messagepath = cf.get("message","path")
    
    filename = os.path.join(messagepath,"%s_%s.txt"%(phone,str(uuid.uuid4()).replace("-","")))
    
    f = open(filename+".w","w")
    f.write(msg)
    f.close()
    
    os.rename(filename+".w",filename)

def send(msg):
    for p in phonelist:
        sendmsg(p,msg)

if __name__ == '__main__':
    init()
    send("中文测试")