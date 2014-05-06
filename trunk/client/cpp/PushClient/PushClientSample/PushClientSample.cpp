// PushClientSample.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <iostream>
#include "PushClient.h"

using namespace std;

void OnGetMsg(const char* from, const char* msg)
{
	cout<<from<<" "<<msg<<endl;
}

int _tmain(int argc, _TCHAR* argv[])
{
	HINSTANCE hdll = NULL;
	hdll = ::LoadLibraryA("PushClient.dll");
	if(hdll==NULL)
	{
		cout<<"load dll error"<<endl;
		FreeLibrary(hdll);
	}

	PushClient_Init pc_init = (PushClient_Init)::GetProcAddress(hdll,"PushClient_Init");
	PushClient_Write pc_write = (PushClient_Write)::GetProcAddress(hdll,"PushClient_Write");
	PushClient_Close pc_close = (PushClient_Close)::GetProcAddress(hdll,"PushClient_Close");
	//PushClient_Listen pc_listen = (PushClient_Listen)::GetProcAddress(hdll,"PushClient_Listen");

	pc_init("127.0.0.1",27000);
	//pc_listen("test",OnGetMsg);
	//pc_listen("test");
	while(true)
	{
		pc_write("tvf_monitor_v0.0.0.3","go");
		::Sleep(1);
	}
	pc_close();

	FreeLibrary(hdll);
	return 0;
}

