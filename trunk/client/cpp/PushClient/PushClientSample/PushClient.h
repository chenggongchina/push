#ifndef VIDEOWORKS_PUSHCLIENT_CPP_CLIENT_H_
#define VIDEOWORKS_PUSHCLIENT_CPP_CLIENT_H_

//typedef void(*OnGotMsgCallback)(const char* from, const char* msg);
typedef void(*PushClient_Init)(const char* ip,int port);
typedef void(*PushClient_Write)(const char* channel,const char* msg);
typedef void(*PushClient_Close)();
//typedef void(*PushClient_Listen)(const char* channels,OnGotMsgCallback callback); 

//typedef void(*PushClient_Listen)(const char* channels); 

#endif