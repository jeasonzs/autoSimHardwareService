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
        print 'open'

    def on_close(self):
        self.volCenter.unregisterReceiver(self.push)
        print 'close'

    def on_message(self, message):
        print 'message='+message


    def push(self,data):
        str = json.dumps(data)
        self.write_message(str)

