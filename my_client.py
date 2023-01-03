# coding:utf-8
import threading
import time
from socket import *

print("=====================TCP客户端=====================");

HOST = '127.0.0.1'  # 为服务器，要是不使用请填写运行服务端的电脑ip
PORT = 20200  # 通信端口号
BUFSIZ = 1024  # 接收数据缓冲大小
ADDR = (HOST, PORT)
NAME = "No1(剩余容量 90%)"


# 接受消息类
def command(msg, cs):
    print("检查是否为命令")
    temp = str(msg)
    if temp.__contains__("/a"):
        print("执行a")
        cs.sendall(bytes("已执行命令a" + "\n", 'utf-8'))
    elif temp.__contains__("/b"):
        print("执行b")
        cs.sendall(bytes("已执行命令b" + "\n", 'utf-8'))


class ClientReceiveThread(threading.Thread):
    __buf = 1024

    # 初始化
    def __init__(self, cs):
        super(ClientReceiveThread, self).__init__()
        self.__cs = cs
        self.__cs.sendall(bytes(NAME + "\n", 'utf-8'))

    def run(self):
        self.receive_msg()

    def receive_msg(self):
        while True:
            msg = self.__cs.recv(self.__buf).decode('utf-8')
            if not msg:
                break
            command(msg, self.__cs)
            print(msg)


# 发送消息类
class ClientSendMsgThread(threading.Thread):

    def __init__(self, cs):
        super(ClientSendMsgThread, self).__init__()
        self.__cs = cs

    def run(self):
        self.send_msg()

    # 根据不同的输入格式来进行不同的聊天方式
    def send_msg(self):
        while True:
            msg = input()
            if msg is not None:
                self.__cs.sendall(bytes(msg + "\n", 'utf-8'))
                print("已发送")


tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 创建客户端套接字
tcpCliSock.connect(ADDR)  # 发起TCP连接
receive_thread = ClientReceiveThread(tcpCliSock)
receive_thread.start()
send_thread = ClientSendMsgThread(tcpCliSock)
send_thread.start()
while True:
    time.sleep(1)
    pass
    # data = input('> ')   #接收用户输入
    # if not data:  #如果用户输入为空，直接回车就会发送""，""就是代表false
    #     break
    # tcpCliSock.send(bytes(data + "\n", 'utf-8'))   #客户端发送消息，必须发送字节数组
    # print("已发送")
    # data = tcpCliSock.recv(BUFSIZ)   #接收回应消息，接收到的是字节数组
    # if not data:   #如果接收服务器信息失败，或没有消息回应
    #     break
    # print(data.decode('utf-8'))  #打印回应消息，或者str(data,"utf-8")

tcpCliSock.close()  # 关闭客户端socket
