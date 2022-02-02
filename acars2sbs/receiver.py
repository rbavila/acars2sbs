from acars2sbs.basicthread import BasicThread
import socket

class Receiver(BasicThread):
    def __init__(self, console, host, port, inputqueue):
        super().__init__("receiver", console)
        self.addr = (host, port)
        self.inputqueue = inputqueue
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.socket.bind(self.addr)
        self.socket.settimeout(5)

    def _run(self):
        try:
            msg = self.socket.recv(4096).decode().rstrip()
            self.inputqueue.put(msg)
        except socket.timeout:
            pass
