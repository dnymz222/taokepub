#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime

class ChinaCounty(db.Model):
    __tablename__ = 'ChinaCounty'
    countyCode = db.Column(db.String(32), primary_key=True)
    countyName = db.Column(db.String(64),unique=False)
    hefengLocationId = db.Column(db.String(64),unique=False)
    accuLocationKey = db.Column(db.String(64),unique=False)
    xinzhiPort = db.Column(db.String(64),unique=False)
    lon = db.Column(db.String(16),unique = False)
    lat = db.Column(db.String(16),unique = False)
    elevation  = db.Column(db.Integer,unique = False)
    cityName = db.Column(db.String(64),unique=False)
    cityCode = db.Column(db.String(32),unique=False)
    provinceCode = db.Column(db.String(64),unique=False)
    provinceName = db.Column(db.String(64),unique=False)

    def __init__(self):
        self.hefengLocationId = ""
        self.accuLocationKey = ""
        self.xinzhiPort= ""
        self.lon = ""
        self.lat = ""
        self.elevation = 0