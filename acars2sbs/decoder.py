from acars2sbs.basicthread import BasicThread
from acars2sbs.acars import ACARSDecoder
import queue

class Decoder(BasicThread):
    def __init__(self, console, inputqueue, dataqueue):
        super().__init__("decoder", console)
        self.inputqueue = inputqueue
        self.dataqueue = dataqueue
        self.msgdecoder = ACARSDecoder()

    def _run(self):
        try:
            msg = self.inputqueue.get(timeout=5)
            data = self.msgdecoder.decode(msg)
            if data:
                self.dataqueue.put(data)
                if 'undecoded' in data:
                    self.log('Undecoded msg: {}'.format(msg))
            else:
                self.log('Unexpected msg format: {}'.format(msg))
        except queue.Empty:
            pass
