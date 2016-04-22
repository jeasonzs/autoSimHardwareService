__author__ = 'jeason'
#coding=utf-8



import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4



class IssueContrlHandler(tornado.web.RequestHandler):
    def get(self):
        data = []
        str = json.dumps(data)
        self.write('hello world!')
    def post(self):
        pass