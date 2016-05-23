__author__ = 'jeason'
#coding=utf-8


import threading
import math
import json
import  random

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

from wavePush   import WavePushHandler
from volPush import  VolPushHandler
from issueContrl     import IssueContrlHandler
from waveCenter import  WaveCenter
from volCenter import  VolCenter
from hardwareService import HardwareService

import serial

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

cnt = 0

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/service/wavePush.py', WavePushHandler),
            (r'/service/volPush.py', VolPushHandler),
            (r'/service/issueContrl.py', IssueContrlHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

def startTimer():
    global cnt
    timer = threading.Timer(2, startTimer)
    timer.start()

    data = dict()
    data['unit'] = 1
    data['wave'] = []
    wave = data['wave']
    for i in range(0,5000):
        tmp = 1.3 * 1000 *math.sin((2*i+cnt) * math.pi / 180)
        wave.append(int(tmp))

    cnt += 20
    waveCenter = WaveCenter()
    waveCenter.addWaveData(data)

    volData = dict()
    volData['unit'] = 1
    volData['vol'] = []
    ch0 = []
    ch1 = []
    for i in range(0,40):
        ch0.append(random.randint(0,20000))
        ch1.append(random.randint(0,20000))
    volData['vol'].append(ch0)
    volData['vol'].append(ch1)
    volCenter = VolCenter()
    volCenter.addVolData(volData)
    hardwareService = HardwareService()
    # hardwareService.staticStart()
    hardwareService.waveStart(0,100,40)

def onceTimer():
    hardwareService = HardwareService()
    # hardwareService.staticStop()
    # hardwareService.waveStart(0,10,40)
    # hardwareService.staticStart()
    # hardwareService.volStart(0,10)
    # hardwareService.volStop(0,10)
    hardwareService.waveStop(0,2,40)
if __name__ == '__main__':
    hardwareService = HardwareService()
    timer = threading.Timer(3, onceTimer)
    timer.start()


    # startTimer()
    tornado.options.parse_command_line()
    app = Application()
    print 'autoSimHardWareService start on port:'+str(options.port)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

