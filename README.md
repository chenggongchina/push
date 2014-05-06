push体系介绍
push体系是一个简单的状态汇报及监控库。客户端可以向服务端汇报数据，或从服务端接收其他客户端汇报的数据。

实现原理:

客户端->服务端使用的是不可靠连接，也就是说，PUSH体系不保障所有的汇报内容均会被服务端成功接收到。
服务端->客户端使用的是可靠连接，但是由于数据众多或客户端连入数量众多，为了保障服务端缓存数据不堆积，服务端也会有选择的丢弃数据，也就是说，PUSH体系不保障所有的服务端数据均会传输到接收端。
功能：

push发送：将数据发送到服务端
push接收：侦听服务端指定通道的数据
push驱动：push驱动详细介绍
适用场景：

分散的组件服务向同一的中心汇报工作状态
轮询机制的服务变为驱动形式的服务

push server
push server是一个永久的控制台服务程序，启动后除非手动杀死，永不关闭。其接收客户端连入及各种数据请求，并记录日志。

usage:
  PushServer.exe 
  or
  PushServer.exe [port] [logpath]
  [port] default = 27000
  [logpath] default = .

push client 特性
push client库不会抛出异常，原则上不会影响到主程序
使用push接收功能，push client库将单独起一个线程进行接收，并且处理断线重连
push client库消耗量很小，不会影响程序整体性能
点击查看各库使用方法。
c++ c# python java

各语言当前实现功能
语言	push发送	push接收	push驱动
c++		√			X			X
c#		√			√			√
python	√			√			√
java	√			√			X
