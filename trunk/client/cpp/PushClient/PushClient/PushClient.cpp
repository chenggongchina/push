/*
****************************************
*  Videoworks PushClient CppLib        *
*                                      *
*  Copyright 2012 @ Videoworks         *
*  All Rights Reserved Worldwide       *
*  Author: chenggong                   *
****************************************
*/

#include "stdafx.h"
#include "PushClient.h"

#pragma comment(lib,"ws2_32.lib")

PushClient* pushClient = NULL;

bool ConnectToTCPServerAndStartListen()
{
	pushClient->tcpSock = socket(AF_INET,SOCK_STREAM,0);
	if(pushClient->tcpSock == INVALID_SOCKET)
		return false;

	SOCKADDR_IN addrSrv;
	addrSrv.sin_addr.S_un.S_addr=inet_addr(pushClient->m_ip.c_str());
    addrSrv.sin_family=AF_INET;
	addrSrv.sin_port=htons(pushClient->m_port);
	int ret = ::connect(pushClient->tcpSock,(SOCKADDR*)&addrSrv,sizeof(SOCKADDR));
	if(ret!=0)
		return false;

	string listenChannalsCmd = pushClient->m_listenChannels + CMD_END_TAG;
	ret = ::send(pushClient->tcpSock,listenChannalsCmd.c_str(),listenChannalsCmd.length(),0);
	if(ret==SOCKET_ERROR)
	{
		closesocket(pushClient->tcpSock);
		return false;
	}
	return true;
}

DWORD WINAPI RecieveThreadLogic(PVOID param)
{
	Debug("recieve thread created.");
	char recvBuf[TCP_BUFFER_SIZE];
	while(true)
	{
		Debug("try to connect..");
		if(false==ConnectToTCPServerAndStartListen())
		{
			Debug("connect fail..wait");
			closesocket(pushClient->tcpSock);
			::Sleep(RECONNECT_INTERVAL);
		}
		Debug("connect success, start to recieve");
		while(SOCKET_ERROR != ::recv(pushClient->tcpSock, recvBuf, TCP_BUFFER_SIZE, 0))
		{
			cout<<recvBuf<<endl;
		}
		closesocket(pushClient->tcpSock);
		::Sleep(RECONNECT_INTERVAL);
	}
	return 0;
}

void PushClient_Init(const char* ip, int port)
{
	Debug("init called");
	pushClient = new PushClient(string(ip),port);
}

void PushClient_Write(const char* channel, const char* msg)
{
	Debug("write called");
	if(pushClient!=NULL)
	{
		pushClient->Write(string(channel),string(msg));
	}
}

//void PushClient_Listen(const char* channels,OnGotMsgCallback callback)
//{
//	Debug("listen called");
//	if(pushClient!=NULL)
//	{
//		pushClient->Listen(string(channels),callback);
//	}
//}

void PushClient_Listen(const char* channels)
{
	Debug("listen called");
	/*if(pushClient!=NULL)
	{
		pushClient->Listen(string(channels),NULL);
	}*/
}


void PushClient_Close()
{
	Debug("close called");
	if(pushClient!=NULL){
		delete pushClient;
	}
}

void Debug(const char* msg)
{
#ifdef EXPORT_DEBUG_FLAG
		cout<<msg<<endl;
#endif
}