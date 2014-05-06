package com.videoworks.pushclient;

public interface IMsgReciever {
	void onGetMsg(String from, String msg);
}
