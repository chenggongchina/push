#encoding=utf8
'''
Created on 2012-7-3

@author: chenggong
'''

import socket
import threading
import time

CMD_END_TAG = "#EndOfCmd#"
CMD_SPLIT_TAG = "#SplitOfCmd#"

TCP_RECIEVE_BUFFER_SIZE = 1*1024*1024
RECONNECT_INTERVAL = 5  #seconds

msgreciever = None

class ListenThread(threading.Thread):
    def init(self,manager,channels):
        self.manager = manager
        self.channels = channels
        
    
    def on_get_data(self,msg):
        self.msgbuffer += msg
        list = msg.split(CMD_END_TAG)
        self.msgbuffer = list[-1]
        if(len(list)>1):
            return list[:-1]
        return None
    
    def run(self):
        while(True):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.msgbuffer = ""
                self.sock.connect(self.manager.serveraddr)
                
                sendata = "join %s%s"%(self.channels,CMD_END_TAG)
                self.sock.send(sendata)
                
                while True:
                    msg= self.sock.recv(TCP_RECIEVE_BUFFER_SIZE)
                    msglist = self.on_get_data(msg)
                    if(msglist==None):
                        continue
                    for m in msglist:
                        try:
                            self.manager.on_get_msg(m)
                        except:
                            pass
            except Exception,e:
                self.sock.close()
                time.sleep(RECONNECT_INTERVAL)

class PushClientManager():
    def __init__(self,ip,port):
        self.msgs = []
        self.udpsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.serveraddr = (ip,port)
        self.listenThreadFlag = False
        self.taskmutex = threading.Event()
    
    def write(self,channel,msg):
        try:
            sendmsg = "%s %s%s"%(channel,msg,CMD_END_TAG)
            self.udpsock.sendto(sendmsg, self.serveraddr)
        except:
            pass
        
    def join(self,channels):
        #pass
        try:
            if(not self.listenThreadFlag):
                self.listenThreadFlag = True
                self.listenThread = ListenThread()
                self.listenThread.init(self,channels)
                self.listenThread.start()
        except:
            pass
        
    def wait(self,timeout):
        self.taskmutex.wait(timeout)
        
    def close(self):
        if(self.listenThread != None):
            #abort thread
            self.listenThread.setDaemon(True)
            self.listenThread.join(1)
            
            #close sock
            if self.listenThread.sock!=None:
                self.listenThread.sock.close()
        if(self.udpsock != None):
            self.udpsock.close()
            
    def on_get_msg(self,msg):
        content = msg.split(CMD_SPLIT_TAG)[0]
        fromaddr = msg.split(CMD_SPLIT_TAG)[1]
        
        if content == 'go':
            self.taskmutex.set()
            self.taskmutex.clear()
        #for debug
        else:
            msgreciever.on_get_msg(content,fromaddr)
            #print "[%s]%s"%(fromaddr,content)
            #pass
