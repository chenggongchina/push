package com.videoworks.pushclient;

public class TestMsgReciever implements IMsgReciever{
	public void onGetMsg(String from, String msg){
		System.out.println("["+(count++)+"]"+"[["+from+"]]"+msg+"/");
	}
	
	private int count = 0;
}
