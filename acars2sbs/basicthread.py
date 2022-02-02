import threading

class BasicThread(threading.Thread):
    def __init__(self, name, console):
        super().__init__(name=name, daemon=True)
        self.console = console
        self.done = False

    def shutdown(self):
        self.log("Shutting down")
        self.done = True

    def run(self):
        self._pre_run()
        while not self.done:
            self._run()
        self._post_run()

    def _pre_run(self):
        self.log("Starting")

    def _run(self):
        pass

    def _post_run(self):
        self.log("Done")

    def log(self, msg):
        self.console.log("[{}] {}".format(self.name, msg))
