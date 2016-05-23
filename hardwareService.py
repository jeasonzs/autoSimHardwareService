__author__ = 'jeason'
#coding=utf-8

from common import  singleton
from socket import *
import threading
import struct
class HardwareSocket(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
    def __del__(self):
        self.stop()
        self.tcpClientSock.close()
    def __connect(self):
        try:
            addr = ('107.170.213.190',9201)
            self.tcpClientSock = socket(AF_INET, SOCK_STREAM)
            self.tcpClientSock.connect(addr)
        except:
            print 'connect error!!'

    def __recv(self):
        data = []
        try:
            data = self.tcpClientSock.recv(1024)
        except:
            print 'recv error!!'
        return data

    def run(self):
        self.__connect()
        while True:
            data = self.__recv()
            if len(data) <= 0:
                self.__connect()
                continue
            self.receiver(data)

    def registerReceiver(self,receiver):
        self.receiver = receiver

    def send(self,data):
        try:
            data = self.tcpClientSock.sendall(data)
        except:
            print 'send error!!'


@singleton
class HardwareService(object):
    def __init__(self):
        self.hardwareSocket = HardwareSocket()
        self.hardwareSocket.registerReceiver(self.__onHardReceive)
        self.hardwareSocket.start()
        pass

    def xorCheck(self,data):
        xor = 0x00
        for i in range(0, len(data)):
            xor = xor^ord(data[i])
        lenStr = str(len(data))

        ret = struct.pack(lenStr+'sB',data,xor)
        return ret


    def __onHardReceive(self,data):
        print repr(data)

    def test(self):
        data = struct.pack('8B',1,2,3,4,5,6,7,8)
        dat = list(struct.unpack('3B',data[0:3])[0:-1])
        print  dat
        self.hardwareSocket.send(self.xorCheck(data))


    def waveStart(self,pos,num,sample):
        data = struct.pack('2B2H3B',0xb1,0xa5,pos,num,sample,0,0)
        self.hardwareSocket.send(self.xorCheck(data))

    def waveStop(self,pos,num,sample):
        data = struct.pack('2B2H3B',0xb1,0x00,pos,num,sample,0,0)
        self.hardwareSocket.send(self.xorCheck(data))

    def staticStart(self):
        data = struct.pack('9B',0xc1,0xa5,0,0,0,0,0,0,0)
        self.hardwareSocket.send(self.xorCheck(data))

    def staticStop(self):
        data = struct.pack('9B',0xc1,0x00,0,0,0,0,0,0,0)
        self.hardwareSocket.send(self.xorCheck(data))

    def volStart(self,start,end):
        data = struct.pack('2B2H3B',0xd1,0xa5,start,end,0,0,0)
        self.hardwareSocket.send(self.xorCheck(data))

    def volStop(self,start,end):
        data = struct.pack('2B2H3B',0xd1,0x00,start,end,0,0,0)
        self.hardwareSocket.send(self.xorCheck(data))

    def issueSet(self,num,type):
        data = struct.pack('9B',0xe1,0xa5,0,num,type,0,0,0,0)
        self.hardwareSocket.send(self.xorCheck(data))