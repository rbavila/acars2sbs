import datetime

class SBSEncoder:
    def __init__(self, icao):
        self.icao = icao

    def encode(self, data):
        # set common parameters
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%Y/%m/%d')
        time = now.strftime('%H:%M:%S') + '.000'

        # process fields and generate corresponding messages
        msgs = []

        if 'callsign' in data:
            m = self._basemsg(self.icao, date, time)
            m[1] = '1'
            m[10] = data['callsign']
            s = ",".join(m) + '\n'
            msgs.append(s)

        if 'lat' in data and 'lon' in data and 'alt' in data:
            m = self._basemsg(self.icao, date, time)
            m[1] = '3'
            m[11] = str(data['alt'])
            m[14] = str(data['lat'])
            m[15] = str(data['lon'])
            m[18] = m[19] = m[20] = m[21] = '0'
            s = ",".join(m) + '\n'
            msgs.append(s)

        if 'speed' in data:
            m = self._basemsg(self.icao, date, time)
            m[1] = '4'
            m[12] = str(data['speed'])
            m[13] = '135' # track
            m[16] = '0'
            s = ",".join(m) + '\n'
            msgs.append(s)

        return msgs

    def encode_ident(self, callsign):
        # set common parameters
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%Y/%m/%d')
        time = now.strftime('%H:%M:%S') + '.000'
        m = self._basemsg(self.icao, date, time)
        m[1] = '1'
        m[10] = callsign
        s = ",".join(m) + '\n'
        return s

    def encode_position(self, lat, lon, alt):
        # set common parameters
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%Y/%m/%d')
        time = now.strftime('%H:%M:%S') + '.000'
        m = self._basemsg(self.icao, date, time)
        m[1] = '3'
        m[11] = str(alt)
        m[14] = str(lat)
        m[15] = str(lon)
        m[18] = m[19] = m[20] = m[21] = '0'
        s = ",".join(m) + '\n'
        return s

    def encode_speed(self, speed):
        # set common parameters
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%Y/%m/%d')
        time = now.strftime('%H:%M:%S') + '.000'
        m = self._basemsg(self.icao, date, time)
        m[1] = '4'
        m[12] = str(speed)
        m[13] = m[16] = '0'
        s = ",".join(m) + '\n'
        return s

    def _basemsg(self, icao, date, time):
        basemsg = [''] * 22
        basemsg[0] = 'MSG'
        basemsg[4] = icao
        basemsg[6] = basemsg[8] = date
        basemsg[7] = basemsg[9] = time
        return basemsg
