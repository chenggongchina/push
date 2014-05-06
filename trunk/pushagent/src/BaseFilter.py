#encoding=utf8
'''
Created on 2012-8-8

@author: chenggong
'''
import datetime
import logout
import MailHelper
import MessageHelper

DEBUG_PRINT_FLAG = False

LOGLEVEL_LOG = 1
LOGLEVEL_WARNING = 2
LOGLEVEL_ERROR = 3

REPORT_DELAY_TIME = 30

class BaseFilter:
    def debug(self,msg):
        if(DEBUG_PRINT_FLAG):
            print msg
            
    def __init__(self):
        self.reportTips = {}
        self.debug("Filter created.")
    
    def filter(self,argvs):        
        if(not self.trigger(argvs)): return
        self.debug('on filter')
        hash = self.getPkHash(argvs)
        reportTip = self.getReportTipByPk(argvs)
        if(self.judge(argvs)):
            self.debug('judge result true')
            if(reportTip==None or reportTip['flag']==False or self.timeExcced(reportTip['time'])):
                self.debug('flag on')
                tmp = {}
                tmp['flag'] = True
                tmp['time'] = datetime.datetime.now()
                tmp['report'] = False
                self.reportTips[hash] = tmp
                #self.on(argvs)
            elif(reportTip['flag']==True and self.delayExcced(reportTip['time']) and reportTip['report']==False):
                self.debug('report on')
                self.on(argvs)
                reportTip['report'] = True
            else:
                pass
        else:
            self.debug('way 2')
            if(reportTip!=None and reportTip['flag']==True):
                self.debug('flag off')
                if(reportTip['report']==True):
                    self.debug('report off')
                    self.off(argvs)
                tmp={}
                tmp['flag'] = False
                tmp['time'] = datetime.datetime.now()
                tmp['report'] = False
                self.reportTips[hash] = tmp
            else:
                pass
        
    def getReportTipByPk(self,argvs):
        hash = self.getPkHash(argvs)
        
        if(self.reportTips.has_key(hash)):
            return self.reportTips[hash]
        else:
            return None
        
    def getPkHash(self,argvs):
        pk = self.pk
        ret = {}
        for p in pk:
            ret[p] = argvs[p]
        return str(ret)
    
    def timeExcced(self,time):
        delta = datetime.datetime.now() - time
        return delta.seconds>self.interval
    
    def delayExcced(self,time):
        delta = datetime.datetime.now() - time
        return delta.seconds>REPORT_DELAY_TIME
    
    def report(self,level,msg):
        logout.log('agent',msg)
        if(level>=2):
            #发送邮件
            MailHelper.sendEmail(msg)
            pass
        if(level>=3):
            #发送短信
            MessageHelper.send(msg)
            pass
    
    def getMsgHead(self,argvs):
        pk = self.pk
        ret = ""
        for p in pk:
            if(p=='host'):
                ret = ret + argvs['fromaddr']
            else:
                ret = ret + argvs[p]
            ret += " "
        return ret
    
    def on(self,argvs):
        self.report(self.level ,"%s%s"%(self.getMsgHead(argvs),self.msg(argvs)))
    def off(self,argvs):
        self.report(self.level ,"已恢复 %s%s"%(self.getMsgHead(argvs),self.msg(argvs)))
    