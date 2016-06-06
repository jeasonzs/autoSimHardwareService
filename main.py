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
import sys,threading,time;
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
    cnt += 5
#start timer
    timer = threading.Timer(1, startTimer)
    timer.start()
#the wave
    wave = []
    for i in range(0,5000):
        tmp = 1.3 * 1000 *math.sin((2*i+cnt) * math.pi / 180)
        wave.append(int(tmp))
    waveCenter = WaveCenter()
    waveCenter.addWaveData(1,1,wave)
#vols
    vol0 = []
    vol1 = []
    for i in range(0,40):
        vol0.append(random.randint(0,20000))
        vol1.append(random.randint(0,20000))
    volCenter = VolCenter()
    volCenter.addVolData(1,0,39,vol0,vol1)


def onceTimer():
    hardwareService = HardwareService()
    # hardwareService.staticStop()
    # hardwareService.waveStart(0,10,40)
    # hardwareService.staticStart()
    # hardwareService.volStart(0,10)
    # hardwareService.volStop(0,10)
    hardwareService.waveStop(0,2,40)
if __name__ == '__main__':
    # port = serial.Serial('com3', 115200, timeout=5)
    # print port.isOpen()
    # data = port.read(1)
    # n = port.inWaiting()
    # data += port.read(n)
    # print data
    # port.close()
    # pass


    hardwareService = HardwareService()
    # timer = threading.Timer(3, onceTimer)
    # timer.start()


    # startTimer()
    tornado.options.parse_command_line()
    app = Application()
    print 'autoSimHardWareService start on port:'+str(options.port)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

