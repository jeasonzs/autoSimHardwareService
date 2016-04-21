__author__ = 'jeason'
#coding=utf-8

import threading

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class DataPushHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.timer = threading.Timer(2, self.sendWave)
        self.timer.start()
        print 'open'

    def on_close(self):
        print 'close'

    def on_message(self, message):
        print 'message='+message

    def sendWave(self):
        print 'wave'
        self.write_message('wave')
        self.timer = threading.Timer(2, self.sendWave)
        self.timer.start()

