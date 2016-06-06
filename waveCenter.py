__author__ = 'jeason'
#coding=utf-8

from common import  singleton



@singleton
class WaveCenter(object):
    def __init__(self):
        self.receivers = []
        pass
    def registerReceiver(self,receiver):
        self.receivers.append(receiver)

    def unregisterReceiver(self,receiver):
        if receiver in self.receivers:
            self.receivers.remove(receiver)

    def addWaveData(self,unit,sample,wave):
        self.__broadcastWave(unit,sample,wave)

    def __broadcastWave(self,unit,sample,wave):
        for receiver in self.receivers:
            receiver(unit,sample,wave)
