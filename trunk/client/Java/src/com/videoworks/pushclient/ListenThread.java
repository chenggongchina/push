package com.videoworks.pushclient;

import java.io.*;
import java.net.Socket;
import java.util.List;

public class ListenThread implements Runnable{
	
	private PushClientManager manager;
	private boolean isConnected = false;
	
	public PushClientManager getManager() {
		return manager;
	}
	public void setManager(PushClientManager manager) {
		this.manager = manager;
	}
	
	public boolean getConnectStatus(){
		return isConnected;
	}

	public void run(){
		Socket client = manager.getTcpClient();
		BufferedReader in = null;
		BufferedWriter out = null;
		isConnected = false;
		while(true){
			try{
				client = new Socket(manager._ip, manager._port);
				manager.msgbuffer = "";
				
				in = new BufferedReader(new InputStreamReader(client.getInputStream()));
				out = new BufferedWriter(new OutputStreamWriter(client.getOutputStream()));

				String tmp = "join " + manager._listenedChannels + manager.CMD_END_TAG;
				out.write(tmp);
				out.flush();
				
				char[] data = new char[manager.TCP_RECIEVE_BUFFER];
				isConnected = true;
				while(true){
					int size = in.read(data);
					String msg = new String(data,0,size);
					List<String> cmds = manager.getMsgs(msg);
					if(cmds == null || cmds.size() == 0)
						continue;
					for(String cmd:cmds){
						try{
							manager.onGetMsg(cmd);
						}catch(Exception e){}
					}
				}
			}
			catch(Exception e){
				isConnected = false;
				try {
					if(client!=null)
						client.close();
					if(in!=null)
						in.close();
					if(out!=null)
						out.close();
					Thread.sleep(manager.RECONNECT_INTERVAL);
				} catch (Exception e1) {
				}
				
			}
		}
	}
}
