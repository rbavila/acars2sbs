from acars2sbs.basicthread import BasicThread
import socket
import queue
import random
import time

class Forwarder(BasicThread):
    def __init__(self, console, fwqueue, host, port):
        super().__init__("forwarder", console)
        self.addr = (socket.gethostbyname(host), port)
        self.fwqueue = fwqueue
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.socket.settimeout(5)

    def _run(self):
        try:
            msg = self.fwqueue.get(timeout=5)
            self._send(msg)
        except queue.Empty:
            return

    def _send(self, msg):
        bytes_sent = 0
        while bytes_sent == 0 and not self.done:
            try:
                bytes_sent = self.socket.sendto(msg, self.addr)
            except socket.gaierror as e:
                self.log("Error sending message: {}".format(e))
                t = random.randint(2, 10)
                self.log("Retrying in {} seconds...".format(t))
                time.sleep(t)
