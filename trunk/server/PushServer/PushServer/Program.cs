using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Runtime.InteropServices;

namespace PushServer
{
    class PushListener
    {
        public Socket sock;
        public string buffer = "";
        public List<string> listenedChannels = new List<string>();
    }

    class PushListenerManager
    {
        private const double PUSHMSG_TIMEOUT = 5;
        private const int PUSHMSG_BUFFERSIZE = 1000;
        private CmdSwitcher _switcher = null;

        public int DroppedMsg = 0;
        public int SendMsg = 0;

        public float DropRate
        {
            get
            {
                if (DroppedMsg + SendMsg == 0)
                    return 0;
                else
                {
                    return 100 * DroppedMsg / (DroppedMsg + SendMsg);
                }
            }
        }

        public PushListenerManager(CmdSwitcher switcher)
        {
            _switcher = switcher;
            Thread pushThread = new Thread(PushLogic);
            pushThread.IsBackground = true;
            pushThread.Start();
        }

        public void PushLogic()
        {
            Queue<PushCmd> pushQueue = _switcher.cmdQueue;
            while (true)
            {
                _switcher.queueSema.WaitOne(); //消费
                PushCmd cmd = null;
                int cmdCount = 0;
                lock (pushQueue)
                {
                    cmdCount = pushQueue.Count;
                    if (cmdCount > 0)
                    {
                        cmd = pushQueue.Dequeue();
                    }
                    else
                        continue;
                }

                if (DroppedMsg == int.MaxValue || SendMsg == int.MaxValue)
                {
                    LoggerDispatcher.Instance.Log("发送数量计数器上溢，清零...");
                    SendMsg = 0;
                    DroppedMsg = 0;
                }

                if (cmd == null) continue;
                if (cmd.time.AddSeconds(PUSHMSG_TIMEOUT) < DateTime.Now || cmdCount > PUSHMSG_BUFFERSIZE) //丢弃阻塞的数据
                {
                    DroppedMsg++;
                    continue;
                }
                SendMsg++;                          

                //寻找侦听该频道的客户端
                List<Socket> sendToSock = new List<Socket>();
                lock (listeners)
                {
                    foreach (var listener in listeners)
                    {
                        if (listener.listenedChannels.Contains(cmd.channel))
                        {
                            sendToSock.Add(listener.sock);
                        }
                    }
                }

                //发送
                foreach (var s in sendToSock)
                {
                    try
                    {
                        s.Send(Encoding.UTF8.GetBytes(cmd.SendPacket));
                    }
                    catch (Exception e)
                    {
                        LoggerDispatcher.Instance.Log("socket send error" + e.StackTrace);
                    }
                }
            }
        }

        List<PushListener> listeners = new List<PushListener>();

        public int Size()
        {
            lock (listeners)
            {
                return listeners.Count;
            }
        }

        public void Add(Socket sock)
        {
            lock (listeners)
            {
                listeners.Add(new PushListener() { sock = sock });
            }
        }

        public void Remove(Socket sock)
        {
            List<PushListener> temp = new List<PushListener>();
            lock (listeners)
            {
                for (int i = 0; i < listeners.Count; ++i)
                {
                    if (listeners[i].sock.Equals(sock)) temp.Add(listeners[i]);
                }
                foreach (var t in temp)
                {
                    listeners.Remove(t);
                }
            }
        }

        public List<Socket> GetSockList(Socket server)
        {
            List<Socket> rst = new List<Socket>();
            rst.Add(server);

            lock (listeners)
            {
                foreach (var p in listeners)
                {
                    if (!rst.Contains(p.sock))
                        rst.Add(p.sock);
                }
            }
            return rst;
        }
        
        public void OnGetData(Socket sock, string msg)
        {
            lock (listeners)
            {
                foreach (var p in listeners)
                {
                    if (p.sock.Equals(sock))
                        p.buffer += msg;
                    string[] temp = p.buffer.Split(new string[] { CmdSwitcher.CMD_END_TAG }, StringSplitOptions.None);
                    if (temp.Length >= 2)
                    {
                        for (int i = 0; i < temp.Length - 1; ++i)
                        {
                            string[] temp2 = temp[i].Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                            if (temp2.Length >= 2)
                            {
                                string cmd = temp2[0];
                                string[] paras = new string[temp2.Length - 1];
                                for (int j = 1; j < temp2.Length; ++j)
                                {
                                    paras[j - 1] = temp2[j];
                                }

                                //具体指令
                                if (cmd == "join") //加入频道
                                {
                                    foreach (var para in paras)
                                    {
                                        if (!p.listenedChannels.Contains(para))
                                            p.listenedChannels.Add(para);
                                    }
                                }
                                else if (cmd == "exit") //离开频道
                                {
                                    foreach (var para in paras)
                                    {
                                        if (p.listenedChannels.Contains(para))
                                            p.listenedChannels.Add(para);
                                    }
                                }
                            }
                        }
                        p.buffer = temp[temp.Length - 1];
                    }
                }
            }
        }
    }

    class Program
    {

        const int MAXCLIENTS = 1000;
        const int TCP_RECIEVE_BUFFER = 1024 * 1024 * 1;
        const string BUILD_DATE = "2013-09-12";
        const int TCP_KEEP_ALIVE = 10 * 1000; //单位：毫秒

        public static void Log(string msg)
        {
            LoggerDispatcher.Instance.Log(msg);
        }

        public static void ShowVersionInfo()
        {
            Console.WriteLine( "***********************************");
            Console.WriteLine( "*  PushServer                     *");
            Console.WriteLine(  "*                                 *");
            Console.WriteLine( "*  Copyright2012@videoworks       *");
            Console.WriteLine( "*  All Rights Reserved Worldwide  *");
            Console.WriteLine( string.Format("*  Package build date:{0}  *",BUILD_DATE));
            Console.WriteLine( string.Format("*  Package version:{0}        *",System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.ToString()));
            Console.WriteLine("***********************************");
        }

        static PushListenerManager plManager = null;

        static public void TcpServerThread()
        {
            Socket server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            server.Bind(new IPEndPoint(IPAddress.Any, port));
            server.Listen(MAXCLIENTS);

            uint dummy = 0;
            byte[] inOptionValues = new byte[Marshal.SizeOf(dummy) * 3];
            BitConverter.GetBytes((uint)1).CopyTo(inOptionValues, 0);
            BitConverter.GetBytes((uint)TCP_KEEP_ALIVE).CopyTo(inOptionValues, Marshal.SizeOf(dummy));
            BitConverter.GetBytes((uint)1000).CopyTo(inOptionValues, Marshal.SizeOf(dummy) * 2);

            while (true)
            {
                List<Socket> temp = plManager.GetSockList(server);
                Socket.Select(temp, null, null, 1000);
                foreach(var sock in temp)
                {
                    if (sock.Equals(server))
                    {
                        Socket client = sock.Accept();
                        client.IOControl(IOControlCode.KeepAliveValues, inOptionValues, null);
                        Log("new client accpet from " + client.RemoteEndPoint.ToString());
                        plManager.Add(client);
                    }
                    else
                    {
                        byte[] data = new byte[TCP_RECIEVE_BUFFER];
                        int len;
                        try
                        {
                            if ((len = sock.Receive(data)) > 0)
                            {
                                string msg = Encoding.UTF8.GetString(data, 0, len);
                                //Log("get command from client " + sock.RemoteEndPoint.ToString() + ":" + msg);
                                plManager.OnGetData(sock, msg);
                            }
                            else
                            {
                                sock.Close();
                                plManager.Remove(sock);
                                Log("client " + sock.RemoteEndPoint.ToString() + " closed");
                            }
                        }
                        catch (Exception e)
                        {
                            try
                            {
                                Log("client " + sock.RemoteEndPoint.ToString() + " " + e.Message);
                            }
                            catch (Exception ex)
                            { }

                            if(sock!=null)
                                sock.Close();
                            plManager.Remove(sock);
                        }
                    }
                }
            }
        }

        static int port = 27000;
        static string logpath = ".";

        const int REPORT_INTERVAL = 1000;
        const int LOG_INTERVAL = 60; //单位:秒

        static public void ReportThread()
        {
            int timeCounter = 0;
            while (true)
            {
                Thread.Sleep(REPORT_INTERVAL);
                timeCounter += REPORT_INTERVAL;

                string reportInfo = string.Format("clients={0}/{1}, buffer/dropped/send={2}/{3}/{4},drop rate={5:####0}%",
                    plManager.Size(), MAXCLIENTS, cmdSwitcher.Size(), plManager.DroppedMsg, plManager.SendMsg, plManager.DropRate);

                if (timeCounter >= LOG_INTERVAL * 1000)
                {
                    Log(reportInfo);
                    timeCounter = 0;
                }
                Console.WriteLine(reportInfo);
            }
        }

        static CmdSwitcher cmdSwitcher = null;
        static void Main(string[] args)
        {
            try
            {
                
                ShowVersionInfo();

                if (args.Length == 2)
                {
                    port = int.Parse(args[0]);
                    logpath = args[1];
                    Logger.LogPath = logpath;
                }
                Console.Title = string.Format("Videoworks PushServer v{0} port:{1}",
                    System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.ToString(),
                    port);

                UdpClient reciever = new UdpClient(new IPEndPoint(IPAddress.Any, port));
                IPEndPoint sender = new IPEndPoint(IPAddress.Any, 0);
                Log(string.Format("Push server started..port={0}, logpath={1}", port, logpath));
            
                cmdSwitcher = new CmdSwitcher();
                plManager = new PushListenerManager(cmdSwitcher);

                Thread tcpAccpetThread = new Thread(TcpServerThread);
                tcpAccpetThread.IsBackground = true;
                tcpAccpetThread.Start();

                Thread reportThread = new Thread(ReportThread);
                reportThread.IsBackground = true;
                reportThread.Priority = ThreadPriority.Lowest;
                reportThread.Start();

                while (true)
                {
                    byte[] data = reciever.Receive(ref sender);
                    cmdSwitcher.Add(data, sender);
                }
            }
            catch (Exception e)
            {
                Log("push server初始化失败,"+e.Message);
            }
        }
    }
}
