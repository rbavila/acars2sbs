from acars2sbs.basicthread import BasicThread
from acars2sbs.activeflight import ActiveFlightAgent
import datetime
import queue

IDLE_TIME = 180

class Dispatcher(BasicThread):
    def __init__(self, console, dataqueue, outputqueue):
        super().__init__("dispatcher", console)
        self.dataqueue = dataqueue
        self.outputqueue = outputqueue
        self.active_flights = {}

    def _run(self):
        # generate a timestamp
        now = datetime.datetime.now()

        # remove idle agents
        to_delete = []
        for (reg, agent) in self.active_flights.items():
            if (now - agent.last_updated).seconds >= IDLE_TIME:
                self.log("Flight {} is idle, terminating".format(agent.flight.callsign))
                agent.shutdown()
                agent.join()
                to_delete.append(reg)
        for i in to_delete:
                del self.active_flights[i]

        # check for new data, return if nothing new
        try:
            data = self.dataqueue.get(timeout=5)
        except queue.Empty:
            return

        # create new flight or update data if existing
        if not data['reg'] in self.active_flights:
            self.log('Creating flight {}'.format(data['callsign']))
            agent = ActiveFlightAgent(data['callsign'], self.console, self.outputqueue, data)
            self.active_flights[data['reg']] = agent
            agent.start()
        else:
            agent = self.active_flights[data['reg']]
            self.log('Updating flight {}'.format(data['callsign']))
            agent.update(data)

        self.log("Active flights: {}".format([x.flight.callsign for x in self.active_flights.values()]))
