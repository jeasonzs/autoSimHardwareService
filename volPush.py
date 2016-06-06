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
from volCenter import  VolCenter

class VolPushHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.volCenter = VolCenter()
        self.volCenter.registerReceiver(self.push)
        self.sample = 1
        print 'vol open'

    def on_close(self):
        self.volCenter.unregisterReceiver(self.push)
        print 'vol close'

    def on_message(self, message):
        print 'vol message='+message


    def push(self,unit,start,end,vol0,vol1):
        data = dict()
        data['unit'] = unit
        data['start'] = start
        data['end'] = end
        data['vol'] = []
        data['vol'].append(vol0)
        data['vol'].append(vol1)

        str = json.dumps(data)
        self.write_message(str)

