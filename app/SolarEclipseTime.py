from  app.SolarEclipse import SolarEclipse
import  math
from  typing import Dict,List,Union
from  app.SolarEclipseCalculate import SolarEclipseCalculate

pi = 3.14159265358979


class SolarEclipseTime:

    def __init__(self, t: float, eclipse: SolarEclipse):
        self.t = t
        self.eclipse = eclipse
        self.elements = eclipse.elemenetsList()
        self.centetlatitude = 0
        self.centetlongitude = 0
        self.year = 1
        self.month = 1
        self.day = 1
        self.hour = 0
        self.minute = 0
        self.second = 0

        self.maxmagnitude = 0
        self.vlist = []
        self.calculatecenter()
        self.getdatetime()
        self.calculatevlist()



    def calculatevlist(self):
        for i in range(0, 360 * 10 + 1):
            for j in range(-90 * 10, 90 * 10 + 1):
                latitude = j / 10.0
                longitude = i / 10.0
                if longitude > 180:
                    longitude = longitude - 360
                try:
                    self.vlist.append(self.calculateEclipse(latitude=latitude,longitude=longitude))
                except:
                    self.vlist.append(0)
                    





    def calculateEclipse(self,latitude:float,longitude:float) ->float:


        obsvconst = [0] * 7

        obsvconst[0] = pi * latitude / 180.0
        obsvconst[1] = -1 * longitude * pi / 180.0
        obsvconst[2] = 0
        obsvconst[3] = 0
        tmp = math.atan(0.99664719 * math.tan(obsvconst[0]))

        obsvconst[4] = 0.99664719 * math.sin(tmp) + (obsvconst[2] / 6378140.0) * math.sin(obsvconst[0])
        obsvconst[5] = math.cos(tmp) + (obsvconst[2] / 6378140.0 * math.cos(obsvconst[0]))
        obsvconst[6] = 0


        circumstances = [0] * 41
        circumstances[1] = self.t

        self.timedependent(elements=self.elements,circumstances=circumstances)
        self.timelocdependent(elements=self.elements,circumstances=circumstances,obsvconst=obsvconst)
        altitude = circumstances[32]
        if altitude < -0.00524:
            return 0



        solarCalculate = SolarEclipseCalculate(latitude, longitude, 0, 0, self.eclipse)
        solarCalculate.calculate()


        if 0 == solarCalculate.eclipseType:
            return 0


        self.midobservational(circumstances=circumstances,obsvconst=obsvconst,mid=solarCalculate.mid)
        magnitude = circumstances[37]
        eclipseType = 0
        if 1 == solarCalculate.eclipseType:
            if self.t > solarCalculate.c4[1] or self.t < solarCalculate.c1[1] :
                eclipseType = 0
                return 0
            else:
                eclipseType = 1

                if magnitude > self.maxmagnitude:
                    self.maxmagnitude = magnitude
                    self.centetlatitude = latitude
                    self.centetlongitude = longitude

                return magnitude * 100
        else:
            if self.t > solarCalculate.c4[1] or self.t < solarCalculate.c1[1] :
                eclipseType = 0

                return 0
            elif self.t > solarCalculate.c3[1] or self.t < solarCalculate.c2[1]:
                eclipseType = 1
                if magnitude > self.maxmagnitude:
                    self.maxmagnitude = magnitude
                    self.centetlatitude = latitude
                    self.centetlongitude = longitude

                return magnitude * 100
            else :
                eclipseType = solarCalculate.eclipseType

                magnitude = circumstances[38]

                if magnitude > self.maxmagnitude:
                    self.maxmagnitude = magnitude
                    self.centetlatitude = latitude
                    self.centetlongitude = longitude

                return 100


    def calculatecenter(self):
        circumstances = [0] * 41
        circumstances[1] = self.t
        self.timedependent(elements=self.elements,circumstances=circumstances)
        index = 0
        circumstances[16] = circumstances[7] - (self.elements[index + 5] / 13713.44)


        delta = circumstances[4]
        hourange = circumstances[16]
        latitude = delta * 180.0 / pi
        longitude = -1 * hourange * 180.0 / pi

        if longitude < -180 :
            longitude  = longitude + 360


        if longitude > 180 :
            longitude = longitude - 360

        self.centetlatitude = latitude
        self.centetlongitude = longitude




    def timedependent(self,elements:  List[float], circumstances: List[float]):

        type = 0

        index = 0

        t = 0

        ans = 0

        t = circumstances[1]
        index = 0

        ans = elements[9 + index] * t + elements[8 + index]
        ans = ans * t + elements[7 + index]
        ans = ans * t + elements[6 + index]
        circumstances[2] = ans


        ans = 3.0 * elements[9 + index] * t + 2.0 * elements[8 + index]
        ans = ans * t + elements[7 + index]
        circumstances[10] = ans

        ans = elements[13 + index] * t + elements[12 + index]
        ans = ans * t + elements[11 + index]
        ans = ans * t + elements[10 + index]
        circumstances[3] = ans

        ans = 3.0 * elements[13 + index] * t + 2.0 * elements[12 + index]
        ans = ans * t + elements[11 + index]
        circumstances[11] = ans

        ans = elements[16 + index] * t + elements[15 + index]
        ans = ans * t + elements[14 + index]
        ans = ans * pi / 180.0
        circumstances[4] = ans

        circumstances[5] = math.sin(ans)
        circumstances[6] = math.cos(ans)

        ans = 2.0 * elements[16 + index] * t + elements[15 + index]
        ans = ans * pi / 180.0
        circumstances[12] = ans

        ans = elements[19 + index] * t + elements[18 + index]
        ans = ans * t + elements[17 + index]
        if ans >= 360.0:
            ans = ans - 360.0

        ans = ans * pi / 180.0
        circumstances[7] = ans

        ans = 2.0 * elements[19 + index] * t + elements[18 + index]
        ans = ans * pi / 180.0
        circumstances[13] = ans

        type = int(circumstances[0])
        if type == -2 or type == 0 or type == 2:
            ans = elements[22 + index] * t + elements[21 + index]
            ans = ans * t + elements[20 + index]
            circumstances[8] = ans
            circumstances[14] = 2.0 * elements[22 + index] * t + elements[21 + index]


        if type == -1 or type == 0 or type == 1:

            ans = elements[25 + index] * t + elements[24 + index]
            ans = ans * t + elements[23 + index]
            circumstances[9] = ans
            circumstances[15] = 2.0 * elements[25 + index] * t + elements[24 + index]

    def timelocdependent(self, elements:List[float], circumstances:List[float],obsvconst:List[float]) :
          ans = 0
          index = 0
          type = 0

          self.timedependent(elements,circumstances)
          index = int( obsvconst[6])

          circumstances[16] = circumstances[7] - obsvconst[1] - (elements[index+5] / 13713.44)
          circumstances[17] = math.sin(circumstances[16])
          circumstances[18] =  math.cos(circumstances[16])

          circumstances[19] = obsvconst[5] * circumstances[17]

          circumstances[20] = obsvconst[4] * circumstances[6] - obsvconst[5] * circumstances[18] * circumstances[5]

          circumstances[21] = obsvconst[4] * circumstances[5] + obsvconst[5] * circumstances[18] * circumstances[6]

          circumstances[22] = circumstances[13] * obsvconst[5] * circumstances[18]

          circumstances[23] = circumstances[13] * circumstances[19] * circumstances[5] - circumstances[21] * circumstances[12]

          circumstances[24] = circumstances[2] - circumstances[19]

          circumstances[25] = circumstances[3] - circumstances[20]

          circumstances[26] = circumstances[10] - circumstances[22]

          circumstances[27] = circumstances[11] - circumstances[23]

          sinlat = math.sin(obsvconst[0])
          coslat = math.cos(obsvconst[0])
          circumstances[32] = math.asin(circumstances[5] * sinlat + circumstances[6] * coslat * circumstances[18])

          type = int(circumstances[0])
          if type == -2 or type == 0 or type == 2:
            circumstances[28] = circumstances[8] - circumstances[21] * elements[26+index]


          if type == -1 or  type == 0 or  type == 1 :
            circumstances[29] = circumstances[9] - circumstances[21] * elements[27+index]

          circumstances[30] = circumstances[26] * circumstances[26] + circumstances[27] * circumstances[27]

    def observational(self, circumstances: List[float],obsvconst:List[float],mid:List[float]):

        contacttype = 0

        sinlat = math.sin(obsvconst[0])
        coslat = math.cos(obsvconst[0])

        if circumstances[0] == 0:
            contacttype = 1.0
        else:
            if mid[39] == 3 and (circumstances[0] == -1 or circumstances[0] == 1):
                contacttype = -1.0
            else:
                contacttype = 1.0

        circumstances[31] = math.atan2(contacttype * circumstances[24], contacttype * circumstances[25])


        try:
            circumstances[33] = math.asin(coslat * circumstances[17] / math.cos(circumstances[32]))
        except Exception as e:
            print(e)

        if circumstances[20] < 0.0:
            circumstances[33] = pi - circumstances[33]

        circumstances[34] = circumstances[31] - circumstances[33]

        circumstances[35] = math.atan2(-1.0 * circumstances[17] * circumstances[6],
                                       circumstances[5] * coslat - circumstances[18] * sinlat * circumstances[6])

        if circumstances[32] > -0.00524:
            circumstances[40] = 0
        else:
            circumstances[40] = 1


    def midobservational(self,circumstances: List[float],obsvconst:List[float],mid:List[float]):
          self.observational(circumstances,obsvconst,mid)

          circumstances[36] = math.sqrt(circumstances[24]*circumstances[24] + circumstances[25]*circumstances[25])
          circumstances[37] = (circumstances[28] - circumstances[36]) / (circumstances[28] + circumstances[29])
          circumstances[38] = (circumstances[28] - circumstances[29]) / (circumstances[28] + circumstances[29])


    def getdatetime(self):
        obsvconst = [0] * 7
        c = [0] * 41
        c[1] = self.t
        self.gettime(c,obsvconst,self.elements)
        self.getdate(c,obsvconst,self.elements)

    def gettime(self,circumstances: List[float],obsvconst:List[float],elements:List[float] ):

        t = 0

        index  = 0

        t = circumstances[1] + elements[1 + index] - obsvconst[3] - (elements[4 + index] - 0.5) / 3600.0
        if t < 0.0:

            t = t + 24.0

        if t >= 24.0:
            t = t - 24.0

        hour  = int(math.floor(t))

        minuteb = (t - math.floor(t)) * 60.0

        minute = int(math.floor(minuteb))

        secondb = (minuteb - math.floor(minuteb)) * 60

        second = int(math.floor(secondb))
        self.hour = hour
        self.minute = minute
        self.second = second


    def getdate(self,circumstances: List[float],obsvconst:List[float],elements:List[float]):


        t = 0

        jd = 0

        a = 0

        b = 0

        c  = 0

        d  = 0

        e  = 0

        index  = 0


        jd = math.floor(elements[index] - (elements[1+index] / 24.0))

        t = circumstances[1] + elements[1+index] - obsvconst[3] - (elements[4+index] - 0.5) / 3600.0
        if t < 0.0 :
            jd =  jd - 1;

        if t >= 24.0:
            jd = jd + 1;

        if jd >= 2299160.0:
            a = math.floor((jd - 1867216.25) / 36524.25)
            a = jd + 1 + a - math.floor(a / 4)
        else:
            a = jd;

        b = a + 1525.0
        c =  int(math.floor((b-122.1) / 365.25))
        d = int( math.floor(365.25 * c))
        e = int(math.floor((b - d) / 30.6001))
        d = int( b - d - math.floor(30.6001 * e) )
        if e < 13.5:
            e = e - 1
        else :
            e = e - 13

        year  = 0
        if e > 2.5:
            year = c - 4716
        else :
            year = c - 4715

        self.year = year
        self.month = e
        self.day = d


