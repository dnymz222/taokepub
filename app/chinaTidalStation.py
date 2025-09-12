#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime

class chinaTidalStation(db.Model):
    __tablename__ = 'chinaTidalStation'
    locationId = db.Column(db.String(100), primary_key=True)
    station = db.Column(db.String(100), unique=False)  # 站点名称
    province = db.Column(db.String(64), unique=False) #省份
    sealevel = db.Column(db.String(20), unique=False) #水位基准
    pinyin = db.Column(db.String(64), unique=False) #拼音
    lat =   db.Column(db.String(20), unique=False)
    lon =  db.Column(db.String(20), unique=False)
    locationkey = db.Column(db.String(32), unique=False)

    def __init__(self,dict):
        self.station = dict['station']
        self.locationId  = dict['locationId']
        self.province = dict['province']
        self.sealevel = dict['sealevel']
        self.pinyin = dict['pinyin']
        self.lat = dict['lat']
        self.lon = dict['lon']

    def chinastationdict(self):
        dict ={}
        dict["type"] = 1
        dict['station']  =self.station
        dict["stationId"]  = self.locationId
        dict['lat'] = float(self.lat)
        dict['lon'] = float(self.lon)
        dict['sealevel'] = self.sealevel
        dict["timezone"] = "Asia/Shanghai"
        return dict
