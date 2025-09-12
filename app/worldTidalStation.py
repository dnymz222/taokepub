#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime

class worldTidalStation(db.Model):
    __tablename__ = 'worldTidalStation'
    stationName = db.Column(db.String(100), primary_key=True)  # 站点名称
    bigStateName = db.Column(db.String(64), unique=False) #大洲
    countryName = db.Column(db.String(64), unique=False) #国家
    lat =   db.Column(db.String(20), unique=False)
    long =  db.Column(db.String(20), unique=False)
    locationkey = db.Column(db.String(32), unique=False)

    def __init__(self,dict):
        self.stationName = dict["stationName"]
        self.bigStateName  = ""
        self.countryName = dict['countryName']
        self.lat = dict['lat']
        self.long = dict['long']


    def worldstationdict(self):
        dict ={}
        dict["type"] = 2
        dict['station']  =self.stationName
        dict['country'] = self.countryName
        dict['lat'] = float(self.lat)
        dict['lon'] = float(self.long)
        dict["province"] = ""
        dict["sealevel"] = ""
        return dict





