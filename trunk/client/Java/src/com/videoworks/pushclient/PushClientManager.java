package com.videoworks.pushclient;

import java.net.*;
import java.util.ArrayList;
import java.util.List;

/**
 * @author chenggong
 * PushClientManager java版本
 * 暂没有实现push驱动功能
 */
public class PushClientManager {
	
	public PushClientManager(String ip,int port){
		_ip = ip;
		_port = port;
		try {
			udpClient = new DatagramSocket();
			_addr = InetAddress.getByName(_ip);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public List<String> getMsgs(String msg){
		msgbuffer += msg;
		String[] result = msgbuffer.split(CMD_END_TAG);
		ArrayList<String> rst = new ArrayList<String>();
		if(msgbuffer.endsWith(CMD_END_TAG)){
			for(String r:result){
				rst.add(r);
			}
			msgbuffer = "";
		}else{
			for(int i=0;i<result.length-1;++i){
				rst.add(result[i]);
			}
			msgbuffer  = result[result.length-1];
		}
		return rst;
	}
	
	public void onGetMsg(String msg){
		String[] result = msg.split(this.CMD_SPLIT_TAG);
		String content = result[0];
		String fromaddr = result[1];
		
		if(content.equals("go")){
			//TODO 实现PUSH驱动，暂无需求
		}
		if(this.msgReciever!=null){
			msgReciever.onGetMsg(fromaddr, content);
		}
	}
	
	public void write(String channel,String msg){
		try{
			if(_addr!=null){
				String sendStr = channel + " " + msg + CMD_END_TAG;
				byte[] sendBuf;
				sendBuf = sendStr.getBytes("utf-8");
				DatagramPacket sendPacket = new DatagramPacket(sendBuf, sendBuf.length, _addr, _port);
				udpClient.send(sendPacket);
			}
		}catch(Exception e){
			
		}
	}
	
	public synchronized void join(String channels){
		try{
			if(!_listenThreadFlag){
				_listenedChannels = channels;
				
				listenThread = new ListenThread();
				listenThread.setManager(this);
				
				_listenThread = new Thread(listenThread);
				_listenThread.setDaemon(true);
				_listenThread.start();
				_listenThreadFlag = true;
			}
		}catch(Exception e){
			
		}
	}
	
	public synchronized void close(){
		try{
			udpClient.close();
			_listenThread.stop(); //暂时使用这么暴力的方法
			//tcpClient.close();
		}catch(Exception e){
			
		}
	}
	
	public void Wait(int timeout){
		
	}
	
	public boolean getConnectStatus(){
		if(listenThread==null) 
			return false;
		return listenThread.getConnectStatus();
	}
	
	public final String CMD_END_TAG = "#EndOfCmd#";
	public final String CMD_SPLIT_TAG = "#SplitOfCmd#";
    public final int RECONNECT_INTERVAL = 5000; 
    public final int TCP_RECIEVE_BUFFER = 1* 1024 * 1024;

    private IMsgReciever msgReciever;
	public IMsgReciever getMsgReciever() {
		return msgReciever;
	}
	public void setMsgReciever(IMsgReciever msgReciever) {
		this.msgReciever = msgReciever;
	}
	
	public String _ip;
	public int _port;
	public String msgbuffer = "";
	
	private InetAddress _addr;
	private DatagramSocket udpClient;
	private Socket tcpClient;
	private ListenThread listenThread;
	
	private boolean _listenThreadFlag = false;
	public String _listenedChannels;
	private Thread _listenThread;
	public void setTcpClient(Socket tcpClient) {
		this.tcpClient = tcpClient;
	}

	public Socket getTcpClient() {
		return tcpClient;
	}

	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		PushClientManager manager = new PushClientManager("127.0.0.1",27000);
		String tmp = "我" + manager.CMD_END_TAG + "的";
		
		List<String> ra = (manager.getMsgs(tmp));
		for(String r:ra){
			System.out.println(r);
		}
		System.out.println("============");
		System.out.println(manager.getMsgs(tmp));
	}

}
