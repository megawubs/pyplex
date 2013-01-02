import threading
import socket
from pyplexlogger.logger import pyPlexLogger

class udplistener(threading.Thread):
    def __init__(self, queue):
        super(udplistener, self).__init__()
        self.l = pyPlexLogger('udplistener').logger
        self.queue = queue
        self._stop = threading.Event()
        self.error = False

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        try:
            sock.bind(("0.0.0.0",9777))
            self.l.info("Started UDP listener")
        except Exception, e:
            self.l.error(e)
            self.error = True

        sock.settimeout(2)
        while not self.stopped():
            try:
                data, addr = sock.recvfrom(1024)
                index = data.rindex("\x02");
                command = data[index+1:-1]
                # self.l.info("Got UDP Command %s" % command)
                self.queue.put((command, [u'']))
            except socket.timeout:
                pass

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
