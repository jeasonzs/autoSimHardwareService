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
        print self.receivers

    def unregisterReceiver(self,receiver):
        if receiver in self.receivers:
            self.receivers.remove(receiver)
        print self.receivers

    def addWaveData(self,waveData):
        self.broadcastWave(waveData)

    def broadcastWave(self,waveData):
        for receiver in self.receivers:
            receiver(waveData)
