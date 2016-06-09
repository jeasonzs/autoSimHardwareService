__author__ = 'jeason'
#coding=utf-8

import random
import json
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from hardwareService import HardwareService
from uuid import uuid4



class IssueContrlHandler(tornado.web.RequestHandler):
    def get(self):
        hardwareService = HardwareService()
        data = dict()
        opt = self.get_argument('opt')
        num = self.get_argument('num')
        if opt == 'setIssue':
            type = self.get_argument('type')
            hardwareService.issueSet(int(num),int(type))
            print 'set ch'+num+'='+type
        if opt == 'getIssue':
            # data['type'] = random.randint(0,6)
            data['type'] = hardwareService.issueGet(int(num))
            print 'get ch'+num+'='+str(data['type'])
        if opt == 'clearIssue':
            print 'clear all issue'
            hardwareService.issueClear()
        self.write(json.dumps(data))

    def post(self):
        print self.request.body
        pass