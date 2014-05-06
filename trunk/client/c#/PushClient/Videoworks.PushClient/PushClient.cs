using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Net.Sockets;
using System.Net;

namespace Videoworks.PushClient
{
    public interface IMsgReciever
    {
        void OnGetMsg(string from, string msg);
    }

    public interface ICloseCallback
    {
        void OnClosed();
    }

    public class PushClientManager
    {
        #region 常量
        public const string CMD_END_TAG = "#EndOfCmd#";
        public const string CMD_SPLIT_TAG = "#SplitOfCmd#";
        public const int RECONNECT_INTERVAL = 5000; //单位:毫秒
        public const int TCP_RECIEVE_BUFFER = 1* 1024 * 1024;
        #endregion

        private IMsgReciever _msgReciever;
        public IMsgReciever MsgReciever
        {
            get { lock (taskMutex) { return _msgReciever; } }
            set { lock (taskMutex) { _msgReciever = value; } }
        }
        public ICloseCallback CloseCallback = null;

        public AutoResetEvent taskMutex = new AutoResetEvent(false);

        static private void ListenThreadLogic(object o)
        {
            PushClientManager manager = o as PushClientManager;
            TcpClient client = manager.tcpClient;
            while (true)
            {
                try
                {
                    client = new TcpClient();
                    manager.msgbuffer = "";
                    client.Connect(manager.endPoint);
                    NetworkStream stream = client.GetStream();
                    string tmp = "join " + manager._listenedChannels + CMD_END_TAG;
                    stream.Write(Encoding.UTF8.GetBytes(tmp), 0, tmp.Length);

                    byte[] data = new byte[TCP_RECIEVE_BUFFER];
                    while (true)
                    {
                        int size = stream.Read(data, 0, data.Length);
                        string msg = Encoding.UTF8.GetString(data, 0, size);
                        List<string> cmds = manager.GetMsgs(msg);
                        if (cmds == null || cmds.Count == 0)
                            continue;
                        foreach (string cmd in cmds)
                        {
                            try
                            {
                                manager.OnGetMsg(cmd);
                            }
                            catch (Exception e)
                            { }
                        }
                    }
                }
                catch (Exception e)
                {
                    client.Close();
                    Thread.Sleep(RECONNECT_INTERVAL);
                }
            }
        }

        public PushClientManager(string ip, int port)
        {
            _ip = ip;
            _port = port;

            try
            {
                endPoint = new IPEndPoint(IPAddress.Parse(ip), port);
            }
            catch (Exception e)
            {
            }

        }

        public void Write(string channel, string msg)
        {
            try
            {
                if (endPoint != null)
                {
                    string sendstr = channel + " " + msg + CMD_END_TAG;

                    udpClient.Send(Encoding.UTF8.GetBytes(sendstr), Encoding.UTF8.GetBytes(sendstr).Length, endPoint);
                }
            }
            catch (Exception e)
            {
            }
        }

        public void Join(string channels)
        {
            try
            {
                if (!_listenThreadFlag)
                {
                    _listenedChannels = channels;
                    _listenThread.IsBackground = true;
                    _listenThread.Start(this);
                    _listenThreadFlag = true;
                }
            }
            catch (Exception e)
            { }
        }

        public void Close(bool isblock = true)
        {
            try
            {
                udpClient.Close();
                _listenThread.Abort(); //暂时使用这么暴力的方法
                tcpClient.Close();
            }
            catch (Exception e)
            {

            }
        }

        public void Close()
        {
            this.Close(true);
        }

        public void Wait(int timeout)
        {
            taskMutex.WaitOne(TimeSpan.FromMilliseconds(timeout));
        }

        #region 私有成员

        private void OnGetMsg(string msg)
        {
            string[] result = msg.Split(new string[1] { PushClientManager.CMD_SPLIT_TAG }, StringSplitOptions.None);
            string content = result[0];
            string fromaddr = result[1];


            if (content == "go")
            {
                taskMutex.Set();
            }

            if (MsgReciever != null)
            {
                MsgReciever.OnGetMsg(fromaddr, content);
            }
        }

        List<string> GetMsgs(string msg)
        {
            msgbuffer += msg;
            string[] result = msgbuffer.Split(new string[1] { CMD_END_TAG }, StringSplitOptions.None);
            List<string> rst = new List<string>();
            for (int i = 0; i < result.Length - 1; ++i)
            {
                rst.Add(result[i]);
            }
            msgbuffer = result[result.Length - 1];
            return rst;
        }

        private string msgbuffer = "";

        private string _ip;
        private int _port;

        private UdpClient udpClient = new UdpClient();
        private TcpClient tcpClient = new TcpClient();
        private IPEndPoint endPoint = null;
        private string _listenedChannels;
        private Thread _listenThread = new Thread(ListenThreadLogic);
        private bool _listenThreadFlag = false;
        #endregion
    }

}
