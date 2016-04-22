__author__ = 'jeason'
#coding=utf-8


import threading
import math
import json

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


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

cnt = 0

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/wavePush.py', WavePushHandler),
            (r'/volPush.py', VolPushHandler),
            (r'/issueContrl.py', IssueContrlHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

def startTimer():
    global cnt
    timer = threading.Timer(1, startTimer)
    timer.start()
    waveCenter = WaveCenter()
    data = dict()
    data['unit'] = 1
    data['wave'] = []
    wave = data['wave']
    for i in range(0,5000):
        tmp = 1.3 * 1000 *math.sin((2*i+cnt) * math.pi / 180)
        wave.append(int(tmp))

    cnt += 20
    # print str

    waveCenter.addWaveData(data)

if __name__ == '__main__':
    startTimer()
    tornado.options.parse_command_line()
    app = Application()
    print 'autoSimHardWareService start on port:'+str(options.port)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

