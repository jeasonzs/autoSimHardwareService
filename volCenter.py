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
    def addVolData(self,volData):
        self.__broadcastVol(volData)

    def __broadcastVol(self,volData):
        for receiver in self.receivers:
            receiver(volData)
