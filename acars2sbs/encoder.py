from acars2sbs.basicthread import BasicThread
from acars2sbs.sbs import SBSEncoder
import queue

class Encoder(BasicThread):
    def __init__(self, console, dataqueue, outputqueue):
        super().__init__("encoder", console)
        self.dataqueue = dataqueue
        self.outputqueue = outputqueue
        self.msgencoder = SBSEncoder()

    def _run(self):
        try:
            data = self.dataqueue.get(timeout=5)
            msgs = self.msgencoder.encode(data)
            for m in msgs:
                self.outputqueue.put(m)
                self.outputqueue.put(m)
                self.outputqueue.put(m)
        except queue.Empty:
            pass
