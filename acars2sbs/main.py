from acars2sbs.basicthread import BasicThread
from acars2sbs.receiver import Receiver
from acars2sbs.decoder import Decoder
from acars2sbs.dispatcher import Dispatcher
from acars2sbs.sender import Sender
from acars2sbs.forwarder import Forwarder
import queue
import time

class Main(BasicThread):
    def __init__(self, console, srchost, srcport, dsthost, dstport, fwhost = None, fwport = None):
        super().__init__("main", console)
        inputqueue = queue.SimpleQueue()
        dataqueue = queue.SimpleQueue()
        outputqueue = queue.SimpleQueue()
        if fwhost:
            fwqueue = queue.SimpleQueue()
        else:
            fwqueue = None
        self.threads = []
        self.threads.append(Receiver(console, srchost, srcport, inputqueue, fwqueue))
        self.threads.append(Decoder(console, inputqueue, dataqueue))
        self.threads.append(Dispatcher(console, dataqueue, outputqueue))
        self.threads.append(Sender(console, outputqueue, dsthost, dstport))
        if fwqueue:
            self.threads.append(Forwarder(console, fwqueue, fwhost, fwport))

    def shutdown(self):
        for t in self.threads:
            t.shutdown()
        super().shutdown()

    def _pre_run(self):
        super()._pre_run()
        for t in self.threads:
            t.start()

    def _post_run(self):
        for t in self.threads:
            t.join()
        super()._post_run()

    def _run(self):
        time.sleep(1)
