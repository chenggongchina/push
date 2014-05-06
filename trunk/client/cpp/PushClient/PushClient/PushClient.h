/*
****************************************
*  Videoworks PushClient CppLib        *
*                                      *
*  Copyright 2012 @ Videoworks         *
*  All Rights Reserved Worldwide       *
*  Author: chenggong                   *
*  Update:  2012-06-21                 *
****************************************
*/
#ifndef VIDEOWORKS_PUSHCLIENT_H_
#define VIDEOWORKS_PUSHCLIENT_H_

#define DLLEXPORT extern "C" _declspec(dllexport)

#include<iostream>
#include<string>
#include<vector>
#include<Windows.h>
#include<WinSock2.h>

using namespace std;

//#define DEBUG
#define CMD_END_TAG "#EndOfCmd#"

#define MSG_SEND_BUFFER 1
#define RECONNECT_INTERVAL 10000
#define TCP_BUFFER_SIZE 1024*1024

//如果不需要控制台输出信息，注释掉下面一行
//#define EXPORT_DEBUG_FLAG

DLLEXPORT typedef void(*OnGotMsgCallback)(const char* from, const char* msg);
DLLEXPORT void PushClient_Init(const char* ip, int port);
DLLEXPORT void PushClient_Write(const char* channel, const char* msg);
//DLLEXPORT void PushClient_Listen(const char* channels,OnGotMsgCallback callback); 
DLLEXPORT void PushClient_Listen(const char* channels); 
DLLEXPORT void PushClient_Close();

DWORD WINAPI RecieveThreadLogic(PVOID param);
void Debug(const char* msg);

class PushClient
{
public:
	PushClient(string ip, int port)
	{
		m_ip = ip;
		m_port = port;
		m_init_send = false;
		m_init_recieve = false;

		WORD wVersionRequested = MAKEWORD(1,1);
		WSADATA wsaData;
		int err = WSAStartup(wVersionRequested,&wsaData);
	}
	
	~PushClient()
	{
		if(udpSock!=NULL)
			closesocket(udpSock);
		if(tcpSock!=NULL)
			closesocket(tcpSock);
		::WSACleanup();
	}

	void Write(string channel,string msg)
	{
		try
		{
			if(!m_init_recieve) InitSend();
			string sendstr = channel + " " + msg + CMD_END_TAG;
			::sendto(udpSock,sendstr.c_str(),sendstr.size(),0,(SOCKADDR*)&udpServerAddr,sizeof(SOCKADDR));
		}
		catch(...)
		{}
	}

	void Listen(string channels,OnGotMsgCallback callback)
	{
		m_listenChannels = channels;
		m_callback = callback;
		if(!m_init_recieve)
		{
			InitRecieve();
		}
	}

	string m_ip;
	int m_port;
	OnGotMsgCallback m_callback;
	string m_listenChannels;
	SOCKET tcpSock;
private:
	void InitSend()
	{
		Debug("init send called..");
		udpSock = socket(AF_INET,SOCK_DGRAM,0);
		
		udpServerAddr.sin_addr.S_un.S_addr = inet_addr(m_ip.c_str());
		udpServerAddr.sin_family = AF_INET;
		udpServerAddr.sin_port = htons(m_port);
		m_init_recieve = true;
	}

	void InitRecieve()
	{
		DWORD threadId;
		h_RecievingThread = ::CreateThread(
			NULL,0,RecieveThreadLogic,(PVOID)this,0,&threadId);
		m_init_recieve = true;
	}

	bool m_init_send, m_init_recieve;

	SOCKET udpSock;
	SOCKADDR_IN udpServerAddr;

	HANDLE h_RecievingThread;
};

#endif