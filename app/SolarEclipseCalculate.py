from  app import SolarEclipse
import  math
from  typing import Dict,List,Union

pi = 3.14159265358979
class SolarEclipseCalculate:
    def __init__(self,latitude: float,longitude: float, altitude: float, hour: float, eclipse: SolarEclipse):
        self.obsvconst = [0] *7

        self.obsvconst[0] = pi * latitude / 180.0
        self.obsvconst[1] = -1 * longitude * pi / 180.0
        self.obsvconst[2] = altitude
        self.obsvconst[3] = -1 * hour
        tmp = math.atan(0.99664719 * math.tan(self.obsvconst[0]))

        self.obsvconst[4] = 0.99664719 * math.sin(tmp) + (self.obsvconst[2] / 6378140.0) * math.sin(self.obsvconst[0])
        self.obsvconst[5] = math.cos(tmp) + (self.obsvconst[2] / 6378140.0 * math.cos(self.obsvconst[0]))
        self.obsvconst[6] = 0

        self.elements = eclipse.elemenetsList()

        self.c1 =  [0] * 41
        self.c2 =  [0] * 41
        self.mid = [0] * 41
        self.c3 =  [0] * 41
        self.c4 =  [0] * 41

        self.magnitude = 0
        self.eclipseType = 0
        self.eclipse_v = 0


    def calculate(self):
        self.getall(self.elements)
        self.magnitude = self.mid[37]
        self.eclipseType = (int)(self.mid[39])
        if self.eclipseType  > 1:
            self.eclipse_v = 100
        elif 0 == self.eclipseType:
            self.eclipse_v = 0
        else:
            self.eclipse_v = self.magnitude * 100



    def timedependent(self,elements:  List[float], circumstances: List[float]):

        type = 0

        index = 0

        t = 0

        ans = 0

        t = circumstances[1]
        index = int(self.obsvconst[6])

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

    def timelocdependent(self, elements:List[float], circumstances:List[float]) :
          ans = 0
          index = 0
          type = 0

          self.timedependent(elements,circumstances)
          index = int( self.obsvconst[6])

          circumstances[16] = circumstances[7] - self.obsvconst[1] - (elements[index+5] / 13713.44)
          circumstances[17] = math.sin(circumstances[16])
          circumstances[18] =  math.cos(circumstances[16])

          circumstances[19] = self.obsvconst[5] * circumstances[17]

          circumstances[20] = self.obsvconst[4] * circumstances[6] - self.obsvconst[5] * circumstances[18] * circumstances[5]

          circumstances[21] = self.obsvconst[4] * circumstances[5] + self.obsvconst[5] * circumstances[18] * circumstances[6]

          circumstances[22] = circumstances[13] * self.obsvconst[5] * circumstances[18]

          circumstances[23] = circumstances[13] * circumstances[19] * circumstances[5] - circumstances[21] * circumstances[12]

          circumstances[24] = circumstances[2] - circumstances[19]

          circumstances[25] = circumstances[3] - circumstances[20]

          circumstances[26] = circumstances[10] - circumstances[22]

          circumstances[27] = circumstances[11] - circumstances[23]

          type = int(circumstances[0])
          if type == -2 or type == 0 or type == 2:
            circumstances[28] = circumstances[8] - circumstances[21] * elements[26+index]


          if type == -1 or  type == 0 or  type == 1 :
            circumstances[29] = circumstances[9] - circumstances[21] * elements[27+index]

          circumstances[30] = circumstances[26] * circumstances[26] + circumstances[27] * circumstances[27]


    def c1c4iterate(self, elements: List[float], circumstances:List[float]) :
          sign = 0
          iter = 0
          tmp = 0
          n = 0

          self.timelocdependent(elements,circumstances)
          if circumstances[0] < 0:
            sign = -1.0
          else:
            sign = 1.0

          tmp = 1.0
          iter = 0
          while (tmp > 0.000001 or tmp < -0.000001) and iter < 50 :
            n =  math.sqrt(circumstances[30])
            tmp = circumstances[26] * circumstances[25] - circumstances[24] * circumstances[27]
            tmp = tmp / n / circumstances[28]
            if 1.0 -  tmp * tmp < 0:
                tmp = 0
            else:
                tmp = sign * math.sqrt(1.0 - tmp * tmp) * circumstances[28] / n
            tmp = (circumstances[24] * circumstances[26] + circumstances[25] * circumstances[27]) / circumstances[30] - tmp
            circumstances[1] = circumstances[1] - tmp
            self.timelocdependent(elements,circumstances)
            iter = iter + 1


    def getc1c4(self,elements: List[float]) :

        tmp = 0

        n = 0

        n = math.sqrt(self.mid[30])
        tmp = self.mid[26] * self.mid[25] - self.mid[24] * self.mid[27]
        tmp = tmp / n / self.mid[28]
        tmp = math.sqrt(1.0 - tmp * tmp) * self.mid[28] / n
        self.c1[0] = -2
        self.c4[0] = 2
        self.c1[1] = self.mid[1] - tmp
        self.c4[1] = self.mid[1] + tmp
        self.c1c4iterate(elements, self.c1)
        self.c1c4iterate(elements,  self.c4)

    def c2c3iterate(self, elements:List[float],circumstances: List[float]) :
          sign = 0
          iter = 0
          tmp = 0
          n = 0

          self.timelocdependent(elements,circumstances)
          if circumstances[0] < 0 :
            sign = -1.0
          else :
            sign = 1.0

          if self.mid[29] < 0.0:
            sign  = -sign

          tmp = 1.0
          iter = 0
          while (tmp > 0.000001 or tmp < -0.000001) and iter < 50 :
            n = math.sqrt(circumstances[30])
            tmp = circumstances[26] * circumstances[25] - circumstances[24] * circumstances[27]
            tmp = tmp / n / circumstances[29]
            try:
                tmp = sign * math.sqrt(1.0 - tmp * tmp) * circumstances[29] / n
            except:
                tmp = 0
            tmp = (circumstances[24] * circumstances[26] + circumstances[25] * circumstances[27]) / circumstances[30] - tmp
            circumstances[1] = circumstances[1] - tmp
            self.timelocdependent(elements, circumstances)
            iter = iter + 1


    def getc2c3(self,elements: List[float]) :

        n = math.sqrt(self.mid[30])
        tmp = self.mid[26] * self.mid[25] - self.mid[24] * self.mid[27]
        tmp = tmp / n / self.mid[29]
        tmp = math.sqrt(1.0 - tmp * tmp) * self.mid[29] / n
        self.c2[0] = -1
        self.c3[0] = 1
        if self.mid[29] < 0.0:
            self.c2[1] = self.mid[1] + tmp
            self.c3[1] = self.mid[1] - tmp
        else:
            self.c2[1] = self.mid[1] - tmp
            self.c3[1] = self.mid[1] + tmp

        self.c2c3iterate(elements, self.c2)
        self.c2c3iterate(elements, self.c3)



    def observational(self,circumstances: List[float]) :

        contacttype= 0

        coslat= 0

        sinlat = 0


        if circumstances[0] == 0 :
            contacttype = 1.0
        else :
            if self.mid[39] == 3 and (circumstances[0] == -1 or circumstances[0] == 1) :
                contacttype = -1.0
            else :
                contacttype = 1.0


        circumstances[31] = math.atan2(contacttype * circumstances[24], contacttype * circumstances[25])

        sinlat = math.sin(self.obsvconst[0])
        coslat = math.cos(self.obsvconst[0])
        circumstances[32] = math.asin(circumstances[5] * sinlat + circumstances[6] * coslat * circumstances[18])
        try:
            circumstances[33] = math.asin(coslat * circumstances[17] / math.cos(circumstances[32]))
        except Exception as e:
            print(e)

        if circumstances[20] < 0.0 :
            circumstances[33] = pi - circumstances[33]


        circumstances[34] = circumstances[31] - circumstances[33]

        circumstances[35] = math.atan2(-1.0 * circumstances[17] * circumstances[6], circumstances[5] * coslat - circumstances[18] * sinlat * circumstances[6])

        if circumstances[32] > -0.00524:
            circumstances[40] = 0
        else:
             circumstances[40] = 1

    def midobservational(self):
          self.observational(self.mid)

          self.mid[36] = math.sqrt(self.mid[24]*self.mid[24] + self.mid[25]*self.mid[25])
          self.mid[37] = (self.mid[28] - self.mid[36]) / (self.mid[28] + self.mid[29])
          self.mid[38] = (self.mid[28] - self.mid[29]) / (self.mid[28] + self.mid[29])


    def getmid(self, elements:List[float]) :

          self.mid[0] = 0
          self.mid[1] = 0.0
          iter = 0
          tmp = 1.0
          self.timelocdependent(elements,self.mid)
          while (tmp > 0.000001 or tmp < -0.000001) and iter < 50:
            tmp = (self.mid[24] * self.mid[26] + self.mid[25] * self.mid[27]) / self.mid[30]
            self.mid[1] = self.mid[1] - tmp
            iter = iter + 1
            self.timelocdependent(elements,self.mid)


    def getsunriset(self, elements:List[float],  circumstances: List[float], riset:float) :
          h0 = 0

          diff = 1.0
          iter = 0
          while (diff > 0.00001 or diff < -0.00001) :
                iter = iter + 1
                if iter == 4:
                    return
                try:
                    h0 = math.acos((math.sin(-0.00524) - math.sin(self.obsvconst[0]) * circumstances[5])/math.cos(self.obsvconst[0])/circumstances[6])
                except Exception as e:
                    h0 = 0
                diff = (riset * h0 - circumstances[16])/circumstances[13]
                while diff >= 12.0:
                    diff -= 24.0
                while diff <= -12.0:
                    diff += 24.0
                circumstances[1] = circumstances[1] +  diff
                self.timelocdependent(elements,circumstances)

    def getsunrise(self, elements: List[float], circumstances:List[float]) :
        self.getsunriset(elements,circumstances,-1.0)


    def getsunset(self, elements: List[float], circumstances: List[float]) :
        self.getsunriset(elements,circumstances,1.0)

    def copycircumstances(self, circumstancesfrom:List[float], circumstancesto: List[float]) :

        for i in range(1,41):
            circumstancesto[i] = circumstancesfrom[i]


    def getall(self,elements: List[float]) :

            pattern = 0

            self.getmid(elements)
            self.midobservational()

            if self.mid[37] > 0.0:

                self.getc1c4(elements)
                if self.mid[36] < self.mid[29] or self.mid[36] < -1 * self.mid[29]:

                    self.getc2c3(elements)
                    if self.mid[29] < 0.0:
                        self.mid[39] = 3
                    else:
                        self.mid[39] = 2


                    self.observational(self.c1)
                    self.observational( self.c2)
                    self.observational( self.c3)
                    self.observational( self.c4)
                    self.c2[36] = 999.9
                    self.c3[36] = 999.9

                    pattern = 0
                    if self.c1[40] == 0:
                        pattern += 10000
                    if self.c2[40] == 0:
                        pattern += 1000
                    if self.mid[40] == 0:
                        pattern += 100
                    if self.c3[40] == 0:
                        pattern += 10
                    if self.c4[40] == 0:
                        pattern += 1

                    if pattern == 11110:
                        self.getsunset(elements, self.c4)
                        self.observational( self.c4)
                        self.c4[40] = 3
                    elif pattern == 11100:
                        self.getsunset(elements, self.c3)
                        self.observational( self.c3)
                        self.c3[40] = 3
                        self.copycircumstances(self.c3, self.c4)
                    elif pattern == 11000:
                        self.c3[40] = 4
                        self.getsunset(elements, self.mid)
                        self.midobservational()
                        self.mid[40] = 3
                        self.copycircumstances(self.mid, self.c4)
                    elif pattern == 10000:
                        self.mid[39] = 1
                        self.getsunset(elements, self.mid)
                        self.midobservational()
                        self.mid[40] = 3
                        self.copycircumstances(self.mid, self.c4)
                    elif pattern == 1111 :
                        self.getsunrise(elements, self.c1)
                        self.observational( self.c1)
                        self.c1[40] = 2
                    elif pattern == 111:
                        self.getsunrise(elements, self.c2)
                        self.observational( self.c2)
                        self.c2[40] = 2
                        self.copycircumstances(self.c2, self.c1)
                    elif pattern == 11:
                        self.c2[40] = 4
                        self.getsunrise(elements, self.mid)
                        self.midobservational()
                        self.mid[40] = 2
                        self.copycircumstances(self.mid, self.c1)
                    elif pattern == 1:
                        self.mid[39] = 1
                        self.getsunrise(elements, self.mid)
                        self.midobservational()
                        self.mid[40] = 2
                        self.copycircumstances(self.mid, self.c1)
                    elif pattern == 0:
                        self.mid[39] = 0


                else:
                    self.mid[39] = 1
                    pattern = 0
                    self.observational( self.c1)
                    self.observational( self.c4)
                    if self.c1[40] == 0:
                        pattern += 100
                    if self.mid[40] == 0:
                        pattern += 10
                    if self.c4[40] == 0:
                        pattern += 1
                    if pattern == 110:
                        self.getsunset(elements, self.c4)
                        self.observational( self.c4)
                        self.c4[40] = 3
                    elif pattern == 100:
                        self.getsunset(elements, self.mid)
                        self.midobservational()
                        self.mid[40] = 3
                        self.copycircumstances(self.mid, self.c4)
                    elif pattern == 11:
                        self.getsunrise(elements, self.c1)
                        self.observational( self.c1)
                        self.c1[40] = 2
                    elif pattern == 1:
                        self.getsunrise(elements, self.mid)
                        self.midobservational()
                        self.mid[40] = 2
                        self.copycircumstances(self.mid, self.c1)
                    elif pattern == 0:
                        self.mid[39]=0


            else:
                self.mid[39] = 0


            if self.mid[39] == 2 or self.mid[39] == 3:
                self.mid[37] = self.mid[38]




