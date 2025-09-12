#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging
import time
import datetime


class WannaSurf(db.Model):
    __tablename__ = 'wannasurf'

    surfhref = db.Column(db.String(200),primary_key=True)
    surfspot = db.Column(db.String(100), unique=False)
    lat = db.Column(db.String(64), unique=False)
    lng = db.Column(db.String(64), unique=False)

    timezone = db.Column(db.String(64), unique=False)

    wave_type = db.Column(db.String(100),
                          unique=False)  # 1.Beach-break 2.Sand-bar 3.Point-break 4.Reef-coral 5.Reef-rocky 6.Reef-artificial 7.Rivermouth 8.breakwater/jetty "":Don't know
    wave_direction = db.Column(db.String(100), unique=False)  # 1.Right 2.Left 3.Right and left "".Don't know
    wave_quality = db.Column(db.String(100),
                             unique=False)  # 1.Totally Epic 2.World Class 3.Regional Classic 4.Normal 5.Sloppy 6.Choss "".Don't know
    wave_experience = db.Column(db.String(100),
                                unique=False)  # 1.Beginners wave 2.All surfers 3.Experienced surfers 4.Pros or kamikaze only... 5.Don't know
    wave_power = db.Column(db.String(100),
                           unique=False)  # 1.Hollow 2.Fast 3. Powerful 4.Ordinary 5.Fun 6.Powerless 7.Ledgey 8.Slab """
    wave_frequency = db.Column(db.String(100),
                               unique=False)  # 1.Rarely break (5day/year) 2.Sometimes break 3.Regular 4.Very consistent (15"" day/year) "".Don't know

    tideswellwind_startworking = db.Column(db.String(100),
                                           unique=False)  # 1.Less than 1m / 3ft, 2:1.""m-1.5m / 3ft-5ft, 3:1.5m-2m /5ft-6ft, 4:2m-2.5m / 6ft-8ft,5:2.5m-3m / 8ft-1""ft 6:3m-3.5m / 1""ft-12ft 7:Over 3.5m / 12ft 8:Don't know
    tideswellwind_holdupsto = db.Column(db.String(100),
                                        unique=False)  # 1:1m+ / 3ft+, 2:2m+ / 6ft+ 3:2.5m+ / 8ft+ 4:3m+ / 1""ft+ 5:4m+ / 12ft 6:5m / 16 ft and over 7:Don't know
    tideswellwind_goodwelldirection = db.Column(db.String(100),
                                                unique=False)  # 1:North 2:NorthWest 3:West 4:SouthWest 5:South 6:SouthEast 7:East 8:NorthEast "":Don't know
    tideswellwind_goodwinddirection = db.Column(db.String(100),
                                                unique=False)  # 1:North 2:NorthWest 3:West 4:SouthWest 5:South 6:SouthEast 7:East 8:NorthEast "":Don't know

    surfspot_bottom = db.Column(db.String(100),
                                unique=False)  # 1.Sandy 2.Sandy with rock 3.Flat rocks 4.Flat rocks with sand 5.Boulders 6.Reef (coral, sharp rocks etc..) 7.Reef (coral,sharp rocks etc..) with sand "":Don't know
    surfspot_danger = db.Column(db.String(100),
                                unique=False)  # 1.Urchins 2.Rips / undertow 3.Rocks 4.Man-made danger (buoys etc..) 5.Private beach 6.Localism 7.Pollution 8.Sharks 9:Shark protected 1"":Nudist colony (France only!) 11:Mines (Angola only !)
    surfspot_normallength = db.Column(db.String(100),
                                      unique=False)  # 1.Short (< 5""m) 2:Normal (5"" to 15""m) 3:Long (15"" to 3"""" m) 4:Very Long (3"""" to 5"""" m) 5:Exceptional (>5""""m) "":Don't know
    surfspot_gooddaylength = db.Column(db.String(100),
                                       unique=False)  # 1. Short (< 5""m) 2:Normal (5"" to 15""m) 3:Long (15"" to 3"""" m) 4:Very Long (3"""" to 5"""" m) 5:Exceptional (>5""""m) "":Don't know
    surfspot_besttideposition = db.Column(db.String(100),
                                          unique=False)  # 1.All tides 2.Low tide only 3.High tide only 4.Mid tide 5.Mid and high tide 6.Low and mid tide 7.Don't know
    surfspot_besttidemovement = db.Column(db.String(100),
                                          unique=False)  # 1.Rising tide 2:Falling tide 3:Rising and falling tides 4:Don't know
    surfspot_weekcrowd = db.Column(db.String(100),
                                   unique=False)  # 1.Empty 2.Few surfers 3.Crowded 4.Ultra crowded 5.Don't know
    surfspot_weekendcrowd = db.Column(db.String(100),
                                      unique=False)  # 1.Empty 2.Few surfers 3.Crowded 4.Ultra crowded 5.Don't know


    def __init__(self,surfspt,href):
        self.surfspot  = surfspt
        self.surfhref = href
        self.lat = ""
        self.lng = ""
        self.timezone = ""

        self.wave_type = ""
        self.wave_direction = ""
        self.wave_experience = ""
        self.wave_quality = ""
        self.wave_power = ""
        self.wave_frequency = ""

        self.tideswellwind_startworking = ""
        self.tideswellwind_holdupsto = ""
        self.tideswellwind_goodwelldirection = ""
        self.tideswellwind_goodwinddirection = ""

        self.surfspot_bottom = ""
        self.surfspot_danger = ""
        self.surfspot_normallength = ""
        self.surfspot_gooddaylength = ""
        self.surfspot_besttideposition = ""
        self.surfspot_besttidemovement = ""
        self.surfspot_weekcrowd = ""
        self.surfspot_weekendcrowd = ""

    def wannasurfdict(self):
        dict = {}
        dict["surfspot"]  = self.surfspot
        dict["surfhref"] = self.surfhref
        return dict
        
        


