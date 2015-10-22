#!/usr/bin/env python
# encoding=utf8

import tornado.web

import tornado.ioloop

import Moter as M


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', IndexHandler), (r'/moter', MoterHandler)]
        settings = dict(debug=True, )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("moter site is active")


class MoterHandler(tornado.web.RequestHandler):
    def get(self):
        moter = M.MoterManager()

        action = self.get_argument("action")
        if action == 'start':
            if not moter.worker or not moter.isrunning():
                moter.start()
                self.write("start moter success")
            else:
                self.write("already running")
        elif action == 'run':
            tt = self.get_argument("t", 0)
            dd = self.get_argument("d", 0)
            try:
                t = int(tt)
                d = int(dd)
                moter.runfor(t, d)
                self.write("t=%s, d=%s, success" % (t, d))
            except Exception, e:
                self.write("fail" + e)
        elif action == 'stop':
            if moter.isrunning():
                moter.stop()
                self.write("stop success")
            else:
                self.write("not started")


if __name__ == "__main__":
    moter = M.MoterManager()
    app = Application()
    app.listen(8085)
    tornado.ioloop.IOLoop.instance().start()