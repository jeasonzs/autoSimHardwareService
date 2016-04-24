__author__ = 'jeason'
#coding=utf-8

import random
import json
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4



class IssueContrlHandler(tornado.web.RequestHandler):
    def get(self):
        data = dict()
        opt = self.get_argument('opt')
        num = self.get_argument('num')
        if opt == 'setIssue':
            type = self.get_argument('type')
            print 'set ch'+num+'='+type
        if opt == 'getIssue':
            data['type'] = random.randint(0,6)
            print 'get ch'+num+'='+str(data['type'])
        self.write(json.dumps(data))

    def post(self):
        print self.request.body
        pass