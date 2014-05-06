package com.videoworks.pushclient;

public class TestPushClientManager {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		PushClientManager manager = new PushClientManager("127.0.0.1",27000);
		manager.setMsgReciever(new TestMsgReciever());
		manager.join("tvf_monitor_v0.0.0.3");
		
		try{
			while(true){
				manager.write("tvf_monitor_v0.0.0.3", "中文测试！！！！！！！！");
				Thread.sleep(1000);
			}
		}
		catch(Exception e){
			
		}
		
		manager.close();
	}

}
