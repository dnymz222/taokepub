from app import create_app
import os
from app import db
import sys
import logging
class Hefengtide(db.Model):
    __tablename__ = 'Hefengtide'
    locationId = db.Column(db.String(24), primary_key=True)
    localName = db.Column(db.String(100), unique=False)
    englishName = db.Column(db.String(100), unique=False)
    chineseName = db.Column(db.String(100), unique=False)
    latitude = db.Column(db.String(24), unique=False)
    longitude = db.Column(db.String(24), unique=False)
    code = db.Column(db.String(24), unique=False)
    datum = db.Column(db.String(10),unique=False)
    areaId = db.Column(db.String(64), unique=False)
    tcode = db.Column(db.String(10), unique=False)
    area = db.Column(db.String(32), unique=False)


    def __init__(self,dict):
        self.locationId = dict['locationId']
        self.localName = dict['localName']
        self.englishName = dict['englishName']
        self.chineseName = dict['chineseName']
        self.latitude = dict["latitude"]
        self.longitude = dict["longitude"]
        self.code = dict["code"]
        self.datum = "0"
        self.areaId = ""
        self.tcode = ""
        self.area  =""


    def locationdict(self):
        dict = {}
        dict["locationId"] = self.locationId
        dict["localName"] = self.localName
        dict["englishName"] = self.englishName
        dict["chineseName"] = self.chineseName
        dict["latitude"] = self.latitude
        dict["longitude"] = self.longitude
        dict["code"] = self.tcode
        dict["datum"] = self.datum
        dict["area"] = self.area
        dict["areaId"] = self.areaId
        return dict
