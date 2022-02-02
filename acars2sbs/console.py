import threading

class Console:
    def __init__(self):
        self.mutex = threading.Lock()

    def log(self, msg):
        self.mutex.acquire()
        self._log(msg)
        self.mutex.release()

    def _log(self, msg):
        print(msg, flush=True)
