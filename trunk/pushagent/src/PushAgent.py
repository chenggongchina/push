#encoding=utf8
'''
Created on 2012-5-11

@author: chenggong
'''

import os,sys
import PushClient
from PushClient import PushClientManager
import logout
import time
from optparse import OptionParser

import AgentFilter
import MailHelper
import MessageHelper

VERSION = "0.0.0.4"
DATE = "2012-08-23"
MAX_COUNT = 99999999

class MessageReciver():
    
    def __init__(self):
        self.count = 0
    
    def on_get_msg(self,msg,fromaddr):
        #reload(AgentFilter)
        try:
            self.count+=1
            AgentFilter.on_get_msg(eval(msg), fromaddr)
        except Exception,e:
            #logout.log('error','filter excute error %s,msg=%s,fromaddr %s'%(str(e),msg,fromaddr))
            pass

class PushAgent():
    def __init__(self,options):
        AgentFilter.init()
        MessageHelper.init()
        MailHelper.init()
        self.options = options
        if options.logpath != '':
            logout.logger = logout.Log(options.logpath)
        else:
            logout.logger = None
        logout.log('normal',"starting push agent...push server at %s:%s"%(options.ipaddr,options.port))
        self.pushmanager = PushClientManager(options.ipaddr,int(options.port))
        CHANNELS = options.channels.split(",")
        for CHANNEL in CHANNELS:
            self.pushmanager.join(CHANNEL)
        self.interval = int(options.interval)
        
    def serve_forever(self):
        while True:
            if(PushClient.msgreciever.count>MAX_COUNT):
                logout.log("normal","recieved msg count clear")
                PushClient.msgreciever.count = 0
            logout.log('normal',"I'm living...recieved msg=%d"%PushClient.msgreciever.count)
            time.sleep(self.interval)

def versioninfo():
    print "***********************************"
    print "*  PushAgent                      *"
    print "*                                 *"
    print "*  Copyright2012@videoworks       *"
    print "*  All Rights Reserved Worldwide  *"
    print "*  Package build date:%s  *"%DATE
    print "*  Package version:%s        *"%VERSION
    print "***********************************"
    
    os.system("title videoworks PushAgent v%s"%VERSION)
    
if __name__ == "__main__":
    versioninfo()
    parser = OptionParser()
    parser.add_option('-i','--ipaddr',action='store',dest='ipaddr',help='push server ip',default='127.0.0.1')
    parser.add_option('-p','--port',action='store',dest='port',help='push server port',default='27000')
    parser.add_option('-l','--logpath',action='store',dest='logpath',help='log path,default:./log/',default='log')
    parser.add_option('-c','--channels',action='store',dest='channels',help='join push channel,default:tvf_monitor_v0.0.0.3',default='tvf_monitor_v0.0.0.3')
    parser.add_option('-t','--interval',action='store',dest='interval',help='living report interval(seconds),default=5',default='5')
    
    PushClient.msgreciever = MessageReciver()
    (options,argcs)=parser.parse_args(sys.argv)
    pushAgent = PushAgent(options)
    pushAgent.serve_forever()
    