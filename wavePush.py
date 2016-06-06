__author__ = 'jeason'
#coding=utf-8

import threading
import json
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4
from waveCenter import  WaveCenter

class WavePushHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.waveCenter = WaveCenter()
        self.waveCenter.registerReceiver(self.push)
        self.sample = 1
        print 'open'

    def on_close(self):
        self.waveCenter.unregisterReceiver(self.push)
        print 'close'

    def on_message(self, message):
        print 'message='+message
        ctrl = json.loads(message)
        self.sample = ctrl['sample']


    def push(self,unit,sample,wave):
        data = dict()
        data['unit'] = unit
        data['sample'] = sample
        data['wave'] = wave[0::self.sample][0:800]

        strJson = json.dumps(data)
        self.write_message(strJson)

