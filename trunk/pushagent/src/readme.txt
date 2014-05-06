		push agent


[����]
��Ҫ�Ȱ�װ python2.6����

[�����в���]
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

[�����ļ�]
config.ini - �����ļ�����Ҫ�ƶ�maillist��phonelist��filterlist

maillist.txt ���ù���ÿ��һ��email��ַ
phonelist.txt ���ù���ÿ��һ���ֻ�����
filters.txt ���ù��� ÿ��һ������������ʽ [�ļ�].[����] �� Filters.XXXXFilter


[����filter]
���裺
1) ��дfilter�ű�
2) �޸�filterlist�ļ�
3) ����push agent


[filter�ű�����]

�������:python version:2.6

�ű�ʾ����⣺

#��������BaseFilter����
class IprecordFilter(BaseFilter):

    #ʵ�ִ˺���ʵ��filter�Ļ�������
    def __init__(self):
	#����ʵ�֣����û���Ĺ��캯�� 
        BaseFilter.__init__(self)         

        #����
	self.pk = ['fact','host']       

        #��С�㱨�������λ����
	self.interval = 15*60           
        
	#�㱨���𣨸���־�����ͬʱ���еͼ���Ļ������Ż�ͬʱ���ʼ��ͼ���־��
	#LOGLEVEL_LOG : ��¼��־
	#LOGLEVEL_WARNING : �����ʼ�
	#LOGLEVEL_ERROR : ���Ͷ���
	self.level = LOGLEVEL_WARNING   
	

    #ʵ�ִ˺���ʵ�ַ��ص���Ϣ,argvs��dict���͵�push���ݰ�
    def msg(self,argvs): 
        return "TS¼�ƻ������ϴ󣬴洢���ܸ��ش����·�������⡣" 

    #ʵ�ִ˺�����������filter��������
    def trigger(self,argvs): 
        return argvs['type']=='iprecord'

    #ʵ�ִ˺�����������������������
    def judge(self,argvs):
        k = Tools.getFromPatten2("Buff= (.*?)/(.*?) Write",argvs['memo'])[0]
        currentBuf = k[0]
        maxBuf = k[1]
        return (float(currentBuf)>3.0)


