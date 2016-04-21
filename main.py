__author__ = 'jeason'
#coding=utf-8



import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

from dataPush   import DataPushHandler
from contrl     import ContrlHandler
from waveCenter import  WaveCenter


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/dataPush.py', DataPushHandler),
            (r'/contrl.py', ContrlHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == '__main__':
    # tornado.options.parse_command_line()
    # app = Application()
    # print 'autoSimHardWareService start on port:'+str(options.port)
    # server = tornado.httpserver.HTTPServer(app)
    # server.listen(options.port)
    # tornado.ioloop.IOLoop.instance().start()

    WaveCenter.instance().registerReceiver('dasd')
    WaveCenter.instance().registerReceiver('dasd')

    WaveCenter.instance().unregisterReceiver('dasd')