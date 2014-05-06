# -*- coding: gbk -*- 

import re
import urllib

class Tools():   
    
    #转unicode
    @staticmethod 
    def toUnicode(s,charset):
        if( charset == "" ):
            return s
        else:
            try:
                u = unicode( s, charset )
            except:
                u = ""
        return u 
      
    #正则抓取   
    #@param single 是否只抓取一个  
    @staticmethod    
    def getFromPatten(patten,src,single=False,set=False):      
        p = re.compile(patten,re.S)   
        all = p.findall(src) 
        if set:
            rst = [];
        else:
            rst = "";
        for matcher in all:  
            if set:
                rst.append(matcher.strip())
            else: 
                rst += matcher.strip() + " "  
            if( single ):   
                break  
        return rst   

    #正则抓取 2  
    #@param single 是否只抓取一个  
    @staticmethod    
    def getFromPatten2(patten,src):      
        p = re.compile(patten,re.S)   
        all = p.findall(src) 
        rst = []
        for matcher in all:  
            rst.append(matcher)
        return rst   
    
    #下载文件
    @staticmethod
    def downloadFile(url,file):
        MAXRETRY = 3
        retry = 0
        try:
            urllib.urlretrieve(url,file)
        except:
            retry+=1
            if retry > MAXRETRY:
                return False
        return True
        
    @staticmethod
    def writeFile(content,path):
        f = file(path,'w')
        f.write(content)
        f.close()