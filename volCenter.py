__author__ = 'jeason'
#coding=utf-8

from common import  singleton



@singleton
class VolCenter(object):
    def __init__(self):
        self.receivers = []
        pass
    def registerReceiver(self,receiver):
        self.receivers.append(receiver)

    def unregisterReceiver(self,receiver):
        if receiver in self.receivers:
            self.receivers.remove(receiver)
    def addVolData(self,unit,start,end,vol0,vol1):
        self.__broadcastVol(unit,start,end,vol0,vol1)

    def __broadcastVol(self,unit,start,end,vol0,vol1):
        for receiver in self.receivers:
            receiver(unit,start,end,vol0,vol1)
