using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Threading;

namespace PushServer
{
    class PushCmd
    {
        public string sender;
        public string msg;
        public string channel;
        public DateTime time;

        public string SendPacket
        {
            get { return msg + CmdSwitcher.CMD_SPLIT_TAG + sender + CmdSwitcher.CMD_END_TAG; }
        }
    }

    class CmdSwitcher
    {
        string cmdBuffer = "";

        public const string CMD_END_TAG = "#EndOfCmd#";
        public const string CMD_SPLIT_TAG = "#SplitOfCmd#";

        public void Add(byte[] data, IPEndPoint sender)
        {
            cmdBuffer += Encoding.UTF8.GetString(data, 0, data.Length);
            string[] sp = cmdBuffer.Split(new string[] { CMD_END_TAG }, StringSplitOptions.None);
            if (sp.Length >= 2)
            {
                cmdBuffer = sp[sp.Length - 1];
                for (int i = 0; i < sp.Length - 1; ++i)
                {
                    this.OnNewMessage(sender.Address.ToString() + ":" + sender.Port, sp[i]);
                }
            }
        }

        private void OnNewMessage(string sender, string msg)
        {
            //Console.WriteLine(sender + " " + msg);
            lock (cmdQueue)
            {
                string channel = "";
                string message = "";

                string[] temp = msg.Split(new string[] { " " }, StringSplitOptions.RemoveEmptyEntries);
                if (temp.Length < 2)
                {
                    LoggerDispatcher.Instance.Log(string.Format("error command from {0} : {1}", sender, msg));
                    return;
                }

                channel = temp[0];
                for (int i = 1; i < temp.Length; ++i)
                {
                    message += temp[i] + " ";
                }

                cmdQueue.Enqueue(new PushCmd() { time = DateTime.Now, channel=channel, msg = message.Trim(), sender = sender });
                queueSema.Release(); //生产
            }
        }

        public Queue<PushCmd> cmdQueue = new Queue<PushCmd>();
        public Semaphore queueSema = new Semaphore(0, int.MaxValue);

        public int Size()
        {
            lock (cmdQueue)
            {
                return cmdQueue.Count;
            }
        }
    }
}
