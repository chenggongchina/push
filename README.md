PUSH framework==================PUSH is simple status report framework, you can use it to report data from client to server, or recieve data from other clients.

PUSH do not promise data will be reached successfully.		>client->server is comunicate in udp. so, PUSH do not promise that all the report message will be reached successfully.
server->client is comunicate in tcp. but, to adapter jam network, server may drop some message if necessary. so, PUSH do not promise all the data with be reached successfully.

Features---------------
* push sending: send data to server* push recieving: recving data from appointed channel
* push driving: see details below
# Push driving
When we design a trigger system aritecher, we may design it as a Polling Mode system so it may be easy to implement.

But if we want to improve the respone performance, the Polling Mode is not fit. In some scene, we may use COMET, in a word: REQUEST, HANG UP, RESPONE: it brings server lots of pressure.

The PUSH is design to get easy to change Polling Mode to Driving Mode.
We can see a normal Polling Mode code as below:
<pre><code>
while true{
	sleep
	work
}
</pre></code>

In PUSH you can write like this

<pre><code>
pushclient.joinchannel
while true{
	pushclient.wait
	work
}
</pre></code>

pushclient.wait implements as waiting for a singal, it will be release as push client recieve a message from server.
And the trigger source system write a simple code : pushclient.send(channel,message) to multicast a message to the client who listened to the channel.


What the scene do we use PUSH?
---------------
* distributed component report data to single center
* to change the Polling Mode to Driving Mode with one line code

Push Server
===============
Push server is console server. It recieves data from clients , dispatches data to listener ,and logs.
<pre><code>
usage:		PushServer.exe
		or
		PushServer.exe [port] [logpath]
		[port] default = 27000
		[logpath] default = .</pre></code>
Push Clent
===============There is no exceptions in Push Client, so the push client lib will not inflect the main logic of client program.

Push client will start a new thread for recieving, and will reconnect if there is any network issue, it cost little resource, and will not affect client program performance.

Support Programming Languages
---------------
		Language	Push Sending		Push Recieving		Push Driving
		C++			O					X					X
		C#			O					O					O
		python		O					O					O
		java		O					O					X
		
Push Agent
===============
You can process the messages easily by Push Agent, as sending a email , writing a log or event send a phone message...