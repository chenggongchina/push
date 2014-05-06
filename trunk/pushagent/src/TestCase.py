#encoding=utf8
'''
Created on 2012-7-3

@author: chenggong
'''
from PushClient import PushClientManager
import time
manager = PushClientManager('127.0.0.1',27000)

#manager.join('tvf_monitor_v0.0.0.3')

k = 0
errorcode = 0
while(True):
    
    manager.write('tvf_monitor_v0.0.0.3',"{'type':'iprecord','host':'test','fact':'test','errorcode':'%d'}"%errorcode)
    manager.write('tvf_monitor_v0.0.0.3',"{'type':'iprecord','host':'test2','fact':'test2','errorcode':'%d'}"%0)
    
    #time.sleep(1)
    manager.wait(1)
    k=k+1
    if k>=2:
        if errorcode == 0:errorcode = -1
        else: errorcode = 0
        k =0
    
manager.close()