__author__ = 'jeason'
#coding=utf-8

from common import  singleton
from socket import *
import threading
import struct
from waveCenter import  WaveCenter
from volCenter import VolCenter
import serial


class HardwareSocket(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
    def __del__(self):
        self.stop()
        self.tcpClientSock.close()
    def __connect(self):
        try:
            # addr = ('107.170.213.190',9201)
            addr = ('127.0.0.1',9201)
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
            self.tcpClientSock.sendall(data)
        except:
            print 'send error!!'

class HardwareSerial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = serial.Serial('com3', 115200, timeout=4)
        pass
    def __del__(self):
        self.stop()
        self.port.close()

    def __recv(self):
        data = ''
        data = self.port.read(1)
        n = self.port.inWaiting()
        data += self.port.read(n)
        return data

    def run(self):
        while True:
            data = self.__recv()
            if len(data) <= 0:
                continue
            self.receiver(data)

    def registerReceiver(self,receiver):
        self.receiver = receiver

    def send(self,data):
        self.port.write(data)



@singleton
class HardwareService(object):
    def __init__(self):
        self.hardware = HardwareSerial()
        self.hardware.registerReceiver(self.__onHardReceive)
        self.hardware.start()
        self.buf = ''
        pass

    def xorCheck(self,data):
        xor = 0x00
        for i in range(0, len(data)):
            xor = xor^ord(data[i])
        lenStr = str(len(data))

        ret = struct.pack(lenStr+'sB',data,xor)
        return ret


    def __onHardReceive(self,data):
        data = self.buf+data
        self.buf = ''
        size = len(data)
        pos = 0
        print 'len='+str(size)+repr(data)
        while size-pos > 0:
            cmd = ord(data[pos])
            if cmd == 0xb0:
                if size-pos < 6:
                    self.buf = data[pos:]
                    break
                head,ch,num,sample = struct.unpack('>B2HB',data[pos:pos+6])
                print head,ch,num,sample
                if 6+num*2+1 > size-pos:
                    self.buf = data[pos:]
                    break
                pos += 6
                wave = struct.unpack('>'+str(num)+'H',data[pos:pos+num*2])
                print wave
                pos += num*2+1
                waveCenter = WaveCenter()
                waveCenter.addWaveData(1,sample,wave)
            elif cmd == 0xd0:
                if size-pos < 5:
                    self.buf = data[pos:]
                    break
                head,start,end = struct.unpack('>B2H',data[pos:pos+5])
                print head,start,end
                num = end-start+1
                print 'num='+str(num)
                if 5+num*2+1 > size-pos:
                    self.buf = data[pos:]
                    break
                pos += 5
                vol = struct.unpack('>'+str(num)+'H',data[pos:pos+num*2])
                print vol
                pos += num*2+1
                volCenter = VolCenter()
                volCenter.addVolData(1,0,39,vol,vol)

            else:
                pos += 1
        print 'hande end'






    def test(self):
        data = struct.pack('8B',1,2,3,4,5,6,7,8)
        dat = list(struct.unpack('3B',data[0:3])[0:-1])
        print  dat
        self.hardware.send(self.xorCheck(data))


    def waveStart(self,pos,num,sample):
        self.waveNum = num
        data = struct.pack('>2B2H3B',0xb1,0xa5,pos,num,sample,0,0)
        self.hardware.send(self.xorCheck(data))

    def waveStop(self,pos,num,sample):
        data = struct.pack('>2B2H3B',0xb1,0x00,pos,num,sample,0,0)
        self.hardware.send(self.xorCheck(data))

    def staticStart(self):
        data = struct.pack('>9B',0xc1,0xa5,0,0,0,0,0,0,0)
        self.hardware.send(self.xorCheck(data))

    def staticStop(self):
        data = struct.pack('>9B',0xc1,0x00,0,0,0,0,0,0,0)
        self.hardware.send(self.xorCheck(data))

    def volStart(self,start,end):
        data = struct.pack('>2B2H3B',0xd1,0xa5,start,end,0,0,0)
        self.hardware.send(self.xorCheck(data))

    def volStop(self,start,end):
        data = struct.pack('>2B2H3B',0xd1,0x00,start,end,0,0,0)
        self.hardware.send(self.xorCheck(data))

    def issueSet(self,num,type):
        data = struct.pack('>9B',0xe1,0xa5,0,num,type,0,0,0,0)
        self.hardware.send(self.xorCheck(data))