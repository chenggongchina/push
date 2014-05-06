		push agent


[环境]
需要先安装 python2.6环境

[命令行参数]
Usage: PushAgent.py [options]

Options:
  -h, --help            show this help message and exit
  -i IPADDR, --ipaddr=IPADDR
                        push server ip
  -p PORT, --port=PORT  push server port
  -l LOGPATH, --logpath=LOGPATH
                        log path,default:./log/
  -c CHANNELS, --channels=CHANNELS
                        join push channel,default:tvf_monitor_v0.0.0.3
  -t INTERVAL, --interval=INTERVAL
                        living report interval(seconds),default=5

[配置文件]
config.ini - 配置文件，需要制定maillist、phonelist、filterlist

maillist.txt 配置规则：每行一个email地址
phonelist.txt 配置规则：每行一个手机号码
filters.txt 配置规则： 每行一个过滤器：格式 [文件].[类名] 如 Filters.XXXXFilter


[配置filter]
步骤：
1) 编写filter脚本
2) 修改filterlist文件
3) 重启push agent


[filter脚本规则]

编程语言:python version:2.6

脚本示例详解：

#必须派生BaseFilter基类
class IprecordFilter(BaseFilter):

    #实现此函数实现filter的基本配置
    def __init__(self):
	#必须实现，调用基类的构造函数 
        BaseFilter.__init__(self)         

        #主键
	self.pk = ['fact','host']       

        #最小汇报间隔，单位：秒
	self.interval = 15*60           
        
	#汇报级别（高日志级别会同时进行低级别的活动，如短信会同时发邮件和记日志）
	#LOGLEVEL_LOG : 记录日志
	#LOGLEVEL_WARNING : 发送邮件
	#LOGLEVEL_ERROR : 发送短信
	self.level = LOGLEVEL_WARNING   
	

    #实现此函数实现返回的信息,argvs是dict类型的push数据包
    def msg(self,argvs): 
        return "TS录制缓冲区较大，存储可能负载大或链路出现问题。" 

    #实现此函数来决定本filter过滤条件
    def trigger(self,argvs): 
        return argvs['type']=='iprecord'

    #实现此函数来决定触发报警的条件
    def judge(self,argvs):
        k = Tools.getFromPatten2("Buff= (.*?)/(.*?) Write",argvs['memo'])[0]
        currentBuf = k[0]
        maxBuf = k[1]
        return (float(currentBuf)>3.0)


