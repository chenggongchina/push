#encoding=utf8
'''
Created on 2012-5-11

@author: chenggong
'''

import logout
import ConfigParser

filters = []

def init():
    try:
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        fileName = cf.get("filters","filterlist")
        
        logout.log("normal","initing filters")
        f = open(fileName)
        line = f.readline()
        while line:
            if(len(line.split("."))!=2):
                line = f.readline()
                continue
            line = line.replace("\n","").replace("\r","")
            print "loading filter : %s"%line ,
            modname = line.split(".")[0]
            classname = line.split(".")[1]
            mod = __import__(modname)
            filters.append(getattr(mod,classname)())
            print("[ok]")
            line = f.readline()
            
        f.close()
        return True
    except Exception,e:
        logout.log('error',"init failed. %s"%str(e))
        return False
    
def on_get_msg(argvs,fromaddr):
    argvs['fromaddr'] = fromaddr
    if(not argvs.has_key('errorcode') or argvs['errorcode']==''):
        argvs['errorcode']='0'
    if(not argvs.has_key('memo')):
        argvs['memo']='0'
    
    for f in filters:
        try:
            f.filter(argvs)
            #print f
        except Exception,e:
            #logout.log('error','%s 执行异常%s'%(f, str(e)))
            pass
    
    """
    if(argv['type']=='tsdemux'):
        rst = Tools.getFromPatten2("丢包率统计    1min:  (.*)   10min:  (.*)   1hour:  (.*)  24hour:  (.*)",argv['memo'])
        rate = rst[0][0]
        r = float(rate.split(" ")[0])
        if(r>1e-4):
            print "warning!!!!丢包率过高,rate=%f"%r 
    """ 
    