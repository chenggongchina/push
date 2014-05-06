#encoding=utf8
'''
Created on 2012-8-8

@author: chenggong
'''

from BaseFilter import *
from Tools import Tools

class IprecordFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 15*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "TS录制缓冲区较大"
    def trigger(self,argvs): 
        return argvs['type']=='iprecord'
    def judge(self,argvs):
        k = Tools.getFromPatten2("Buff= (.*?)/(.*?) Write",argvs['memo'])[0]
        currentBuf = k[0]
        maxBuf = k[1]
        return (float(currentBuf)>3.0)
        
class IprecordFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 15*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "TS录制缓冲区溢出"
    def trigger(self,argvs): 
        return argvs['type']=='iprecord'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1
        
class IprecordFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "TS录制文件不增长"
    def trigger(self,argvs): 
        return argvs['type']=='iprecord'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2

class FlvtranscodeFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "FLV伴随转码跟不上实时"
    def trigger(self,argvs): 
        return argvs['type']=='flvtranscode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-3
    
class FlvtranscodeFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "FLV伴随转码无法转码且阻死"
    def trigger(self,argvs): 
        return argvs['type']=='flvtranscode'
    def judge(self,argvs):
        #print argvs['errorcode']
        return int(argvs['errorcode'])==-1

class FlvtranscodeFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "FLV伴随转码任务无法开始转码"
    def trigger(self,argvs): 
        return argvs['type']=='flvtranscode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2
    
class RecordFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "虚拟录制无法连接fileserver"
    def trigger(self,argvs): 
        return argvs['type']=='record'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1

class RecordFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "虚拟录制:fileserver返回无后续数据"
    def trigger(self,argvs): 
        return argvs['type']=='record'
    def judge(self,argvs):
        return int(argvs['errorcode'])==1
    
class RecordFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','channel','host']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "虚拟录制无法写入存储"
    def trigger(self,argvs): 
        return argvs['type']=='record'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2
    
class TranscodeFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "转码阻塞"
    def trigger(self,argvs): 
        return argvs['type']=='transcode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1

class TranscodeFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "transcode跟不上实时"
    def trigger(self,argvs): 
        return argvs['type']=='transcode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==2
    
class TranscodeFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "transcode无法开始转码"
    def trigger(self,argvs): 
        return argvs['type']=='transcode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2
        
class DeployFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "发布worker无法连接存储"
    def trigger(self,argvs): 
        return argvs['type']=='deploy'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1
    
class DeployFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','memo']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "发布worker无法连接对方服务器"
    def trigger(self,argvs): 
        return argvs['type']=='deploy'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2

class DeployFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','memo']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "deploy worker:发布缓慢"
    def trigger(self,argvs): 
        return argvs['type']=='deploy'
    def judge(self,argvs):
        return int(argvs['errorcode'])==1
    
class FileServerFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','instanceid']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "fileserver:通道被占满"
    def trigger(self,argvs): 
        return argvs['type']=='fileserver'
    def judge(self,argvs):
        return int(argvs['errorcode'])==1
    
class FileServerFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','instanceid']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "fileserver:无法访问存储"
    def trigger(self,argvs): 
        return argvs['type']=='fileserver'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1
    
class FileStreamFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','instanceid','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "filestream:该频道ts/flv无法传输"
    def trigger(self,argvs): 
        return argvs['type']=='filestream'
    def judge(self,argvs):
        return int(argvs['errorcode'])==3
    
class VGDownloadFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "vgdownload:fileserver返回无后续数据"
    def trigger(self,argvs): 
        return argvs['type']=='videogatedownload'
    def judge(self,argvs):
        return int(argvs['errorcode'])==1
    
class VGDownloadFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 60*60
        self.level = LOGLEVEL_LOG
    def msg(self,argvs): 
        return "vgdownload下载速度非常慢"
    def trigger(self,argvs): 
        return argvs['type']=='videogatedownload'
    def judge(self,argvs):
        return int(argvs['errorcode'])==2
    
class VGDownloadFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 60*60
        self.level = LOGLEVEL_ERROR
    def msg(self,argvs): 
        return "videogate访问不了存储"
    def trigger(self,argvs): 
        return argvs['type']=='videogatedownload'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2    
    
class VGDownloadFilter4(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','instanceid']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "videogate无法连接fileserver"
    def trigger(self,argvs): 
        return argvs['type']=='videogatedownload'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1
    
class VGTransFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "vgtrans跟不上实时"
    def trigger(self,argvs): 
        return argvs['type']=='videogatetranscode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==1
    
class VGTransFilter2(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "vgtrans无法转码"
    def trigger(self,argvs): 
        return argvs['type']=='videogatetranscode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-1
    
class VGTransFilter3(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.pk = ['fact','host','channel']
        self.interval = 60*60
        self.level = LOGLEVEL_WARNING
    def msg(self,argvs): 
        return "vgtrans无法开始转码"
    def trigger(self,argvs): 
        return argvs['type']=='videogatetranscode'
    def judge(self,argvs):
        return int(argvs['errorcode'])==-2