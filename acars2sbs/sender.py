from acars2sbs.basicthread import BasicThread
import socket
import queue
import random
import time

class Sender(BasicThread):
    def __init__(self, console, outputqueue, host, port):
        super().__init__("sender", console)
        self.outputqueue = outputqueue
        self.addr = (host, port)
        self.socket = None

    def _connect(self):
        self.log("Connecting to {}".format(self.addr))
        self.socket = None
        while not self.socket and not self.done:
            try:
                self.socket = socket.create_connection(self.addr)
                self.socket.settimeout(5)
                self.log("Successfully connected to {}".format(self.addr))
            except OSError as e:
                self.log("Connection failed: {}".format(e))
                t = random.randint(2, 10)
                self.log("Retrying in {} seconds...".format(t))
                time.sleep(t)
                self.socket = None

    def _send(self, msg):
        sent = False
        while not sent and not self.done:
            try:
                self.socket.sendall(msg.encode())
                # self.log("Sent: {}".format(msg.rstrip()))
                sent = True
            except ConnectionError:
                self.log("Lost connection to {}, trying to reconnect".format(self.addr))
                self._connect()

    def _pre_run(self):
        super()._pre_run()
        self._connect()

    def _run(self):
        try:
            msg = self.outputqueue.get(timeout=5)
            self._send(msg)
        except queue.Empty:
            pass
