import re

CONV_LATLON = 1
CONV_LATLON2 = 2
CONV_LATLON3 = 4
CONV_SPD_MACH = 8

class ACARSDecoder:
    def __init__(self):
        self.decoders = []

        # common preamble with reg and callsign
        preamble = r"AC2 {2,3}([\w-]+) . .. . .... (\w{6})"

        # common patterns that appear on several messages
        num = r"\d+"
        alphanum = r"\w+"
        decimal = r'\d+\.\d+'

        # AC2  PR-TYF ! 16 6 M75A JJ4613 POS /CS TAM4613/TN .PR-TYF/POS S 29.312 W 51.122/TIM 184312/ALT 18243/SPD 284/FOB 75/ETA 2008/DST SBGR
        # extract:
        # - reg (PR-TYF)
        # - callsign (JJ4613)
        # - lat (S 29.312)
        # - lon (W 51.122)
        # - time (184312)
        # - alt (18243)
        # - speed (284)
        exp = preamble + r'.+/POS ([NS] {}) ([WE] {})/TIM ({})/ALT ({})/SPD ({}).*'.format(
            decimal, # number part of latitude
            decimal, # number part of longitude
            num, # time
            num, # alt
            num, # speed
        )
        fields = ['reg', 'callsign', 'lat', 'lon', 'time', 'alt', 'speed']
        self.decoders.append((re.compile(exp), fields, CONV_LATLON))

        # AC2  CC-BEJ ! 80 2 M51A LA0771 3N01 POSRPT 0771/20 SBGL/SCEL .CC-BEJ  /POS S26504W052007/ALT +35981/MCH 780/FOB 011954/ETA 0151
        # AC2  PR-YRH ! 80 0 M56A AD4925 3N01 POSRPT 4925/20 SBPA/SBKP .PR-YRH  /POS S28371W050318/ALT 21754/MCH 0756/FOB   5986/ETA 0140
        # extract (examples in 1st msg):
        # - reg (CC-BEJ)
        # - callsign (LA0771)
        # - lat (S26504)
        # - lon (W052007)
        # - alt (35981)
        # - speed (780)
        exp = preamble + r'.+POSRPT .+ /POS ([NS]{})([WE]{})/ALT \+?({})/MCH ({}).+$'.format(
            num, # number part of latitude
            num, # number part of longitude
            num, # altitude
            num, # speed
        )
        fields = ['reg', 'callsign', 'lat', 'lon', 'alt', 'speed']
        self.decoders.append((re.compile(exp), fields,
            CONV_LATLON2 | CONV_SPD_MACH))

        # AC2  PR-AYN ! H1 6 F06A AD4367 #M1BPOSS29595W051202,,232254,26,ISEPA,232351,SH11,P25,13718,83,/TS232254,20012279BB
        # AC2  PR-AYG ! H1 1 F51A AD4556 #M1BPOSS28292W050109,,234142,259,VUKMO,234426,VAGAL,M20,10411,81,/TS234142,2001227E65
        # AC2  PR-AYG ! H1 5 F54A AD4556 #M1BPOSS29596W051130,,000306,6,RW11,000359,,P26,10321,72,/TS000306,21012251CF
        # AC2  PR-AYN ! H1 8 F09A AD4022 #M2BPOSS29597W051091,,002855,6,NETPI,003024,SUKSU,P25,11519,146,/TS002855,21012219B1
        # extract (examples in 1st msg):
        # - reg (PR-AYN)
        # - callsign (AD4367)
        # - lat (S29595)
        # - lon (W051202)
        # - alt? (13718)
        exp = preamble + r' #M.BPOS([NS]{})([WE]{}).+,({}),.+,.+,.+$'.format(
            num, # number part of latitude
            num, # number part of longitude
            num, # altitude
        )
        fields = ['reg', 'callsign', 'lat', 'lon', 'alt']
        self.decoders.append((re.compile(exp), fields, CONV_LATLON2))

        # AC2  LV-GVE ! 16 7 M36A AR1242 192129,39000,2043, 134,S 29.248 W 51.089
        # AC2  LV-FSK ! 16 9 M53A AR1220 234211,37000,0256, 233,S 31.300 W 52.834
        # extract (examples in 1st msg):
        # - reg (LV-GVE)
        # - callsign (AR1242)
        # - alt (39000)
        # - lat (S 29.248)
        # - lon (W 51.089)
        exp = preamble + r' {},({}),.+,([NS] {}) ([WE] {})$'.format(
            num, # time stamp? (ignored anyway)
            num, # altitude
            decimal, # latitude
            decimal, # longitude
        )
        fields = ['reg', 'callsign', 'alt', 'lat', 'lon']
        self.decoders.append((re.compile(exp), fields, CONV_LATLON))

        # AC2  PR-GUJ ! H1 8 D34A G37648 #DFBR12  H1PR-GUJ28012218210900007648061203487122510-SBGLSABE  H236002773-120255-004248111100000000000  C1S280822W0485170-398247060182109.098.001  D1T10782248460402
        # extract:
        # - reg (PR-GUJ)
        # - callsign (G37648)
        # - lat (S280822)
        # - lon (W0485170)
        # - alt (36002, right after 'H2')
        exp = preamble + r'.+ H2(\d{5}).+C1([NS]\d{6})([WE]\d{7})'
        fields = ['reg', 'callsign', 'alt', 'lat', 'lon']
        self.decoders.append((re.compile(exp), fields, CONV_LATLON3))

        # AC2  PR-MBH ! Q0 5 S30A JJ3291
        # AC2  PR-MBH ! SA 8 S33A JJ3291 0EV182338V
        # extract:
        # - reg (PR-MBH)
        # - callsign (JJ3291)
        exp = preamble + r'( {})?$'.format(
            alphanum, # time stamp? (ignored anyway)
        )
        r = re.compile(exp)
        fields = ['reg', 'callsign', 'dummy']
        self.decoders.append((r, fields, 0))

        # AC2  PR-MBH ! Q0 5 S30A JJ3291 etc. etc.
        # ha varias mensagens diferentes que começam com este prefixo
        # a ideia eh que esta regex seja um fallback, pra pegar pelo menos o reg e o callsign
        # exp = r"^{} ({}) . .. . .... ({})".format(
        #     preamble,
        #     reg, # reg
        #     alphanum, # callsign
        # )
        # r = re.compile(exp)
        # fields = ['reg', 'callsign']
        # self.decoders.append((r, fields, 0))

    def decode(self, msg):
        for (r, fields, flags) in self.decoders:
            match = r.match(msg)
            if match:
                # print(match.groups())
                return self._build_data(fields, match.groups(), flags)
        return None

    def _build_data(self, fields, groups, flags):
        data = dict(zip(fields, groups))

        if flags & CONV_LATLON:
            lat = self._conv_latlon(data['lat'])
            lon = self._conv_latlon(data['lon'])
            data['lat'] = lat
            data['lon'] = lon

        if flags & CONV_LATLON2:
            lat = self._conv_latlon2(data['lat'])
            lon = self._conv_latlon2(data['lon'])
            data['lat'] = lat
            data['lon'] = lon

        if flags & CONV_LATLON3:
            lat = self._conv_latlon3(data['lat'])
            lon = self._conv_latlon3(data['lon'])
            data['lat'] = lat
            data['lon'] = lon

        if flags & CONV_SPD_MACH:
            spd = self._conv_spd_mach(data['speed'])
            data['speed'] = spd

        return data

    def _conv_latlon(self, latlon):
        r = r'([NSWE])\s?(.+)'
        match = re.match(r, latlon)
        (cp, v) = match.groups()
        if cp == 'N' or cp == 'E':
            return float(v)
        else:
            return -1 * float(v)

    def _conv_latlon2(self, latlon):
        r = r'([NSWE])(.+)'
        match = re.match(r, latlon)
        (cp, v) = match.groups()
        if cp == 'N' or cp == 'E':
            return int(v) / 1000
        else:
            return -1 * int(v) / 1000

    def _conv_latlon3(self, latlon):
        r = r'([NSWE])(.+)'
        match = re.match(r, latlon)
        (cp, v) = match.groups()
        if cp == 'N' or cp == 'E':
            return int(v) / 10000
        else:
            return -1 * int(v) / 10000

    def _conv_spd_mach(self, spd):
        knots = int(spd) / 1000 * 666
        return knots

if __name__ == "__main__":
    test_msgs = [
        'AC2  PR-TYF ! 16 6 M75A JJ4613 POS /CS TAM4613/TN .PR-TYF/POS S 29.312 W 51.122/TIM 184312/ALT 18243/SPD 284/FOB 75/ETA 2008/DST SBGR',
        'AC2  CC-BEJ ! 80 2 M51A LA0771 3N01 POSRPT 0771/20 SBGL/SCEL .CC-BEJ  /POS S26504W052007/ALT +35981/MCH 780/FOB 011954/ETA 0151',
        'AC2  PR-YRH ! 80 0 M56A AD4925 3N01 POSRPT 4925/20 SBPA/SBKP .PR-YRH  /POS S28371W050318/ALT 21754/MCH 0756/FOB   5986/ETA 0140',
        'AC2  PR-AYN ! H1 6 F06A AD4367 #M1BPOSS29595W051202,,232254,26,ISEPA,232351,SH11,P25,13718,83,/TS232254,20012279BB',
        'AC2  PR-AYG ! H1 1 F51A AD4556 #M1BPOSS28292W050109,,234142,259,VUKMO,234426,VAGAL,M20,10411,81,/TS234142,2001227E65',
        'AC2  PR-AYG ! H1 5 F54A AD4556 #M1BPOSS29596W051130,,000306,6,RW11,000359,,P26,10321,72,/TS000306,21012251CF',
        'AC2  PR-AYN ! H1 8 F09A AD4022 #M2BPOSS29597W051091,,002855,6,NETPI,003024,SUKSU,P25,11519,146,/TS002855,21012219B1',
        'AC2  PR-MBH ! Q0 5 S30A JJ3291',
        'AC2  PR-MBH ! SA 8 S33A JJ3291 0EV182338V',
        'AC2   PRODF ! SA 8 S33A JJ3291 0EV182338V',
        'AC2  LV-FSK ! 16 9 M53A AR1220 234211,37000,0256, 233,S 31.300 W 52.834',
        'AC2  PR-GXE ! H1 8 D31A G31176 #DFBR12  H1PR-GXE28012218354400001176061203531124817-SBGRSBPA  H223997609-027257-003239111011000000000  C1S284638W0502231-214290041183544+098+001  D1T06038239376361',
    ]
    d = ACARSDecoder()

    for msg in test_msgs:
        data = d.decode(msg)
        print(data)
