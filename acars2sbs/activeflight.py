from acars2sbs.basicthread import BasicThread
from acars2sbs.sbs import SBSEncoder
import datetime
import hashlib
import queue
import time

DATA_VALIDITY = 60

class ActiveFlight:
    def __init__(self, reg, callsign):
        self.reg = reg
        self.callsign = callsign
        self.pos = None
        self.track = 0
        self.alt = None
        self.speed = None
        self.pos_last_updated = None
        self.speed_last_updated = None

        # generate a fake ICAO hex-code from ident
        h = hashlib.md5()
        h.update(reg.encode())
        self.icao = 'ACA' + h.digest().hex()[-3:]

    def update_position(self, lat, lon, alt):
        self.pos = (lat, lon)
        self.alt = alt
        self.pos_last_updated = datetime.datetime.now()

    def update_speed(self, speed):
        self.speed = speed
        self.speed_last_updated = datetime.datetime.now()

    def position_is_valid(self):
        if not self.pos_last_updated:
            return False
        else:
            now = datetime.datetime.now()
            return (now - self.pos_last_updated).seconds <= DATA_VALIDITY

    def speed_is_valid(self):
        if not self.speed_last_updated:
            return False
        else:
            now = datetime.datetime.now()
            return (now - self.speed_last_updated).seconds <= DATA_VALIDITY

    def spin(self):
        self.track = (self.track + 45) % 360


class ActiveFlightAgent(BasicThread):
    def __init__(self, name, console, outputqueue, flight_data):
        super().__init__(name, console)
        self.outputqueue = outputqueue
        self.dataqueue = queue.SimpleQueue()
        self.last_updated = datetime.datetime.now()
        self.flight = ActiveFlight(flight_data['reg'], flight_data['callsign'])
        self.update(flight_data)
        self.sbsencoder = SBSEncoder(self.flight.icao)

    def update(self, data):
        if 'lat' in data and 'lon' in data and 'alt' in data:
            self.flight.update_position(data['lat'], data['lon'], data['alt'])
        if 'speed' in data:
            self.flight.update_speed(data['speed'])
        self.log("Flight info updated")

    def _run(self):
        msg = self.sbsencoder.encode_msg1(self.flight.callsign)
        self.outputqueue.put(msg)
        if self.flight.position_is_valid():
            gs = self.flight.speed if self.flight.speed_is_valid() else 333
            msg = self.sbsencoder.encode_msg4(gs, self.flight.track, 0)
            self.outputqueue.put(msg)
            self.flight.spin() # :-)
            msg = self.sbsencoder.encode_msg3(self.flight.alt, *self.flight.pos)
            self.outputqueue.put(msg)
            msg = self.sbsencoder.encode_msg5(self.flight.alt)
            self.outputqueue.put(msg)
        if self.flight.speed_is_valid():
            msg = self.sbsencoder.encode_msg4(self.flight.speed, self.flight.track, 0)
            self.outputqueue.put(msg)
        time.sleep(1)


if __name__ == "__main__":
    f = ActiveFlight("PT-ABC", "FF1234")
    print(f.icao)
    print(f.position_is_valid())
    print(f.speed_is_valid())
