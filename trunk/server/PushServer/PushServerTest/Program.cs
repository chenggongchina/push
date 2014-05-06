using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Net;

namespace PushServerTest
{
    class Program
    {
        static void Main(string[] args)
        {
            UdpClient client = new UdpClient();
            IPEndPoint addr = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 27000);
            while (true)
            {
                try
                {
                    string msg = Console.ReadLine();
                    client.Send(Encoding.UTF8.GetBytes(msg), msg.Length, addr);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                }
            }
        }
    }
}
