using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.IO;

namespace PushServerTestTcp
{
    class Program
    {
        static void Main(string[] args)
        {
            TcpClient client = new TcpClient();
            IPEndPoint addr = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 27000);

            client.Connect(addr);
            NetworkStream stream = client.GetStream();

            string tmp = "join test1 test2#EndOfCmd#";
            stream.Write(Encoding.UTF8.GetBytes(tmp), 0, tmp.Length);

            byte[] data = new byte[1024 * 1024];

            while (true)
            {
                int size = stream.Read(data, 0, data.Length);
                string msg = Encoding.UTF8.GetString(data, 0, size);
                Console.WriteLine(msg);
            }
        }
    }
}
