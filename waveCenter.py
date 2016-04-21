__author__ = 'jeason'
#coding=utf-8


class WaveCenter(object):
    ins = ''
    def __init__(self):
        print 'init'
        pass

    @staticmethod
    def instance():
        if WaveCenter.ins == '':
            WaveCenter.ins = WaveCenter()
            WaveCenter.ins.receivers = []
        return WaveCenter.ins

    def registerReceiver(self,receiver):
        self.receivers.append(receiver)
        print self.receivers

    def unregisterReceiver(self,receiver):
        if receiver in self.receivers:
            self.receivers.remove(receiver)
        print self.receivers