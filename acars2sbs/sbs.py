import datetime

class SBSEncoder:
    def __init__(self, icao):
        self.icao = icao

    def encode_msg1(self, callsign):
        m = self._basemsg()
        m[1] = '1'
        m[10] = '@' + callsign
        s = ",".join(m) + '\n'
        return s

    def encode_msg3(self, alt, lat, lon):
        m = self._basemsg()
        m[1] = '3'
        m[11] = str(alt)
        m[14] = str(lat)
        m[15] = str(lon)
        m[18] = m[19] = m[20] = m[21] = '0'
        s = ",".join(m) + '\n'
        return s

    def encode_msg4(self, gs, track, vr):
        m = self._basemsg()
        m[1] = '4'
        m[12] = str(gs)
        m[13] = str(track)
        m[16] = str(vr)
        s = ",".join(m) + '\n'
        return s

    def encode_msg5(self, alt):
        m = self._basemsg()
        m[1] = '5'
        m[11] = str(alt)
        m[18] = m[20] = m[21] = '0'
        s = ",".join(m) + '\n'
        return s

    def _basemsg(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        basemsg = [''] * 22
        basemsg[0] = 'MSG'
        basemsg[4] = self.icao
        basemsg[6] = basemsg[8] = now.strftime('%Y/%m/%d')
        basemsg[7] = basemsg[9] = now.strftime('%H:%M:%S') + '.000'
        return basemsg
