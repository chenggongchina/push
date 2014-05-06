#encoding=utf-8
import os
import time
import glob
import threading

logger = None

def log(level,msg):
    if(logger != None):
        logger.logout(level,msg)
    else:
        #only print
        stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        (logFileName,timeInfo) = stime.split(" ")
        writeContent = "[%s][%s]%s\n" % (level,timeInfo,msg)
        print writeContent.decode('utf-8')
        
class Log():
    def __init__(self,logPath):
        self.logoutPath = logPath
        
    def writeError2OnePlace(self,errorPath):
        try:
            targetFileName = "C:\\error.txt"
            if os.path.isfile("errorpathconfig.txt"):
                file = open("errorpathconfig.txt","r")
                targetFileName = file.readLine()
                file.close()
                if "errorpath" in targetFileName:
                    targetFileName = targetFileName.replace("errorpath=","").replace("\n","").replace("\r","")
    
            targetPath = os.path.dirname(targetFileName)
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
                
            targetFile = open(targetFileName,"a")
            errorFileList = glob.glob(os.path.join(errorPath,"*.txt"))
            for errorFileName in errorFileList:
                file = open(errorFileName,"r")
                errString = file.readline()
                file.close()
                targetFile.write(errString)
                os.remove(errorFileName)
            targetFile.close()
        except Exception,e:
            print "writeError2OnePlace error"
    
    def logout(self, level, description):
        try:
            if not os.path.exists(self.logoutPath):
                os.makedirs(self.logoutPath)
            stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            (logFileName,timeInfo) = stime.split(" ")
            logFile = open(os.path.join(self.logoutPath,logFileName+".log"),"a")
            writeContent = "[%s][%s]%s\n" % (level,timeInfo,description)
            logFile.write(writeContent)
            print writeContent.decode('utf-8')
            logFile.close()
            
            """
            if level=="error":
                errorPath = os.path.join(logoutPath,"error")
                if not os.path.exists(errorPath):
                    os.mkdir(errorPath)
                timeName = logFileName.replace("-","")+timeInfo.replace(":","")
                errorFileName = "%s\\%s.txt"%(errorPath,timeName)
                file = open(errorFileName,"w")
                file.write(writeContent)
                file.close()
                th = threading.Thread(target=self.writeError2OnePlace,args=(errorPath,))
                th.start()
            """
        except Exception,e:
            print str(e)
            print "add log error"
    
if __name__=="__main__":
    log = Log("D:\\log")
    log.logout("error","test1","test1")
    print "over"
