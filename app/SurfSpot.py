from app import create_app
import os
from app import db
import sys
import logging

class SurfSpot(db.Model):
    __tablename__ = 'SurfSpot'
    spot_id= db.Column(db.Integer, primary_key=True)
    magicsea_id = db.Column(db.Integer, unique=False)
    lat = db.Column(db.Float, unique=False)
    lng = db.Column(db.Float, unique=False)
    magicsea_guide = db.Column(db.String(128), unique=False)
    magicsea_forecast = db.Column(db.String(128), unique=False)
    magicsea_name = db.Column(db.String(128), unique=False)
    spot_name = db.Column(db.String(128), unique=False)
    timezone = db.Column(db.String(64), unique=False)

    wave_type = db.Column(db.Integer, unique=False)  #1.Beach-break 2.Sand-bar 3.Point-break 4.Reef-coral 5.Reef-rocky 6.Reef-artificial 7.Rivermouth 8.breakwater/jetty 0:Don't know
    wave_direction = db.Column(db.Integer, unique=False) #1.Right 2.Left 3.Right and left 0.Don't know
    wave_quality= db.Column(db.Integer, unique=False) #1.Totally Epic 2.World Class 3.Regional Classic 4.Normal 5.Sloppy 6.Choss 0.Don't know
    wave_experience  = db.Column(db.Integer, unique=False) # 1.Beginners wave 2.All surfers 3.Experienced surfers 4.Pros or kamikaze only... 5.Don't know
    wave_power  = db.Column(db.Integer, unique=False) #1.Hollow 2.Fast 3. Powerful 4.Ordinary 5.Fun 6.Powerless 7.Ledgey 8.Slab 0"
    wave_frequency = db.Column(db.Integer, unique=False)# 1.Rarely break (5day/year) 2.Sometimes break 3.Regular 4.Very consistent (150 day/year) 0.Don't know

    tideswellwind_startworking = db.Column(db.Integer, unique=False) #1.Less than 1m / 3ft, 2:1.0m-1.5m / 3ft-5ft, 3:1.5m-2m /5ft-6ft, 4:2m-2.5m / 6ft-8ft,5:2.5m-3m / 8ft-10ft 6:3m-3.5m / 10ft-12ft 7:Over 3.5m / 12ft 8:Don't know
    tideswellwind_holdupsto =  db.Column(db.Integer, unique=False) #1:1m+ / 3ft+, 2:2m+ / 6ft+ 3:2.5m+ / 8ft+ 4:3m+ / 10ft+ 5:4m+ / 12ft 6:5m / 16 ft and over 7:Don't know
    tideswellwind_goodwelldirection =  db.Column(db.Integer, unique=False) #1:North 2:NorthWest 3:West 4:SouthWest 5:South 6:SouthEast 7:East 8:NorthEast 0:Don't know
    tideswellwind_goodwinddirection = db.Column(db.Integer,unique=False)  # 1:North 2:NorthWest 3:West 4:SouthWest 5:South 6:SouthEast 7:East 8:NorthEast 0:Don't know

    surfspot_bottom = db.Column(db.Integer, unique=False) #1.Sandy 2.Sandy with rock 3.Flat rocks 4.Flat rocks with sand 5.Boulders 6.Reef (coral, sharp rocks etc..) 7.Reef (coral,sharp rocks etc..) with sand 0:Don't know
    surfspot_danger = db.Column(db.Integer, unique=False) #1.Urchins 2.Rips / undertow 3.Rocks 4.Man-made danger (buoys etc..) 5.Private beach 6.Localism 7.Pollution 8.Sharks 9:Shark protected 10:Nudist colony (France only!) 11:Mines (Angola only !)
    surfspot_normallength  = db.Column(db.Integer, unique=False) # 1.Short (< 50m) 2:Normal (50 to 150m) 3:Long (150 to 300 m) 4:Very Long (300 to 500 m) 5:Exceptional (>500m) 0:Don't know
    surfspot_gooddaylength   =db.Column(db.Integer, unique=False) # 1. Short (< 50m) 2:Normal (50 to 150m) 3:Long (150 to 300 m) 4:Very Long (300 to 500 m) 5:Exceptional (>500m) 0:Don't know
    surfspot_besttideposition =  db.Column(db.Integer, unique=False) #1.All tides 2.Low tide only 3.High tide only 4.Mid tide 5.Mid and high tide 6.Low and mid tide 7.Don't know
    surfspot_besttidemovement = db.Column(db.Integer, unique=False) #1.Rising tide 2:Falling tide 3:Rising and falling tides 4:Don't know
    surfspot_weekcrowd = db.Column(db.Integer, unique=False)#1.Empty 2.Few surfers 3.Crowded 4.Ultra crowded 5.Don't know
    surfspot_weekendcrowd = db.Column(db.Integer,unique=False)  # 1.Empty 2.Few surfers 3.Crowded 4.Ultra crowded 5.Don't know





    def __init__(self,dict):

        self.spot_name = ""
        self.magicsea_id  = dict["id"]
        self.spot_id = self.magicsea_id/100*330+ 22*(self.magicsea_id%100)/10 + self.magicsea_id%10 * 2
        self.magicsea_name = dict["name"]
        self.lat = dict["lat"]
        self.lng = dict["lon"]
        self.magicsea_forecast = dict["forecast"]
        self.magicsea_guide = dict["guide"]
        self.timezone = dict["timezone"]

        self.wave_type = 0
        self.wave_direction = 0
        self.wave_experience = 0
        self.wave_quality = 0
        self.wave_power = 0
        self.wave_frequency = 0

        self.tideswellwind_startworking = 0
        self.tideswellwind_holdupsto  = 0
        self.tideswellwind_goodwelldirection = 0
        self.tideswellwind_goodwinddirection = 0

        self.surfspot_bottom = 0
        self.surfspot_danger = 0
        self.surfspot_normallength = 0
        self.surfspot_gooddaylength = 0
        self.surfspot_besttideposition = 0
        self.surfspot_besttidemovement = 0
        self.surfspot_weekcrowd = 0
        self.surfspot_weekendcrowd = 0

    def __init__(self,spot_id,spot_name,lat,lng):

        self.spot_name = spot_name
        self.magicsea_id  =0
        self.spot_id = spot_id
        self.magicsea_name = ""
        self.lat = lat
        self.lng = lng
        self.magicsea_forecast = ""
        self.magicsea_guide =""
        if spot_id> 100020:
            self.timezone = "Asia/Taipei"
        else:
            self.timezone = "Asia/Shanghai"

        self.wave_type = 0
        self.wave_direction = 0
        self.wave_experience = 0
        self.wave_quality = 0
        self.wave_power = 0
        self.wave_frequency = 0

        self.tideswellwind_startworking = 0
        self.tideswellwind_holdupsto  = 0
        self.tideswellwind_goodwelldirection = 0
        self.tideswellwind_goodwinddirection = 0

        self.surfspot_bottom = 0
        self.surfspot_danger = 0
        self.surfspot_normallength = 0
        self.surfspot_gooddaylength = 0
        self.surfspot_besttideposition = 0
        self.surfspot_besttidemovement = 0
        self.surfspot_weekcrowd = 0
        self.surfspot_weekendcrowd = 0


    def surfspotDict(self):
        dict = {}
        dict["stationId"] =  str(10000000+ self.spot_id)
        dict["station"] = self.spot_name
        dict["lat"] = self.lat
        dict["lon"] = self.lng

        dict["timezone"] = self.timezone
        dict["sealevel"] = 0
        dict["type"] = 3
        return dict




