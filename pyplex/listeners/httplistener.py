import threading
import socket
import urllib2
import tornado.ioloop, tornado.web
from pyplexlogger.logger import pyPlexLogger

class listenerClass(tornado.web.RequestHandler):

    def initialize(self, queue):
        self.queue = queue

    def get(self):
        self.l = pyPlexLogger('httplistener').logger
        string = self.get_argument("command")
        front = string.index("(")
        end = string.rindex(")")
        command = string[:front]
        commandargs = string[front+1:end].split(';')
        self.queue.put((command, commandargs))
        self.write("received")

class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, World')

class httplistener(threading.Thread):
    def __init__(self, queue):
        super(httplistener, self).__init__()
        self.error = False
        self.l = pyPlexLogger('httplistener').logger
        self.queue = queue
        self._stop = threading.Event()
        self.app = tornado.web.Application([(r'/xbmcCmds/xbmcHttp', listenerClass, dict(queue=queue)), (r'/', hello)])
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.l.info("HTTP Init done")

    def run(self):
        try:
            self.app.listen(3000)
            self.l.info("Started HTTP listener")
        except Exception, e:
            self.l.error(e)
            self.error = True
        self.ioloop.start()

    def ioloop_stop(self):
        self.ioloop.stop()

    def stop(self):
        self.ioloop.add_callback(self.ioloop_stop)
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
