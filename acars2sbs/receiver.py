from acars2sbs.basicthread import BasicThread
import socket

class Receiver(BasicThread):
    def __init__(self, console, host, port, inputqueue, fwqueue = None):
        super().__init__("receiver", console)
        self.addr = (host, port)
        self.inputqueue = inputqueue
        self.fwqueue = fwqueue
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.socket.bind(self.addr)
        self.socket.settimeout(5)

    def _run(self):
        try:
            pdu = self.socket.recv(4096)
            msg = pdu.decode().rstrip()
            self.inputqueue.put(msg)
            if self.fwqueue:
                self.fwqueue.put(pdu)
        except socket.timeout:
            pass
