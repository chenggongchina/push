using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Threading;
using Videoworks.PushClient;

namespace Videoworks.PushClient.Sample
{
    class Program
    {
        class MessageReciever : IMsgReciever
        {
            public void OnGetMsg(string from, string msg)
            {
                Console.WriteLine("get msg:" + msg + " from " + from);
            }
        }

        class CloseCallback : ICloseCallback
        {
            public void OnClosed()
            {
                Console.WriteLine("closed");
            }
        }

        static void Main(string[] args)
        {
            //string ip = args[0];
            //int port = int.Parse(args[1]);

            string ip = "127.0.0.1";
            int port = 27000;

            PushClientManager manager = new PushClientManager(ip, port);
            manager.MsgReciever = new MessageReciever();
            manager.CloseCallback = new CloseCallback();
            manager.Join("tvf_monitor_v0.0.0.3");

            //send
            //manager.Write("controlcenter", "go");

            int k = 0;
            while (true)
            {
                manager.Write("tvf_monitor_v0.0.0.31", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                //Console.WriteLine("do work...");
                //manager.Write("tvf_monitor_v0.0.0.3", "go");
                k++;
                //manager.Wait(1000);    
                Thread.Sleep(20);
            }

            manager.Close(false);
            Console.WriteLine("end");
            Thread.Sleep(3000);
        }
    }
}
