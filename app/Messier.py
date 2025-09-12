from app import create_app
import os
from app import db
import sys
import logging

class Messier(db.Model):
    __tablename__ = 'Messier'
    number = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(32), unique=False)
    NGCCIC_number = db.Column(db.String(64), unique=False)
    englishLink = db.Column(db.String(128), unique=False)
    chineseLink = db.Column(db.String(128), unique=False)
    japaneseLink = db.Column(db.String(128), unique=False)
    picture= db.Column(db.String(128), unique=False)
    commonName = db.Column(db.String(64), unique=False)
    obejectType = db.Column(db.String(64), unique=False)
    constellation = db.Column(db.String(64), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Magnitude = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(32), unique=False)

    def __init__(self,dict):
        self.number = dict["number"]
        self.title = dict["title"]
        self.NGCCIC_number  = dict["NGCCIC_number"]
        self.englishLink = dict["englishLink"]
        if "chineseLink" in dict:
            self.chineseLink =dict["chineseLink"]
        else:
            self.chineseLink = ""
        if "japaneseLink" in dict :
            self.japaneseLink = dict["japaneseLink"]
        else:
            self.japaneseLink = ""
        self.picture = dict["picture"]
        self.commonName = dict["commonName"]
        self.obejectType  =dict["obejectType"]
        self.constellation = dict["constellation"]
        self.Declination = dict["Declination"]
        self.RightAscension = dict["RightAscension"]
        self.Magnitude = dict["Magnitude"]
        self.Distance = dict["Distance"]

    def messierdict(self):
        dict = {}
        dict["number"] = self.number
        dict["title"] = self.title
        dict["NGCCIC_number"] = self.NGCCIC_number
        dict["picture"] = self.picture
        dict["commonName"]  =self.commonName
        dict["obejectType"] = self.obejectType
        dict["constellation"] = self.constellation
        dict["RightAscension"] = self.RightAscension
        dict["Declination"] = self.Declination
        dict["Magnitude"] = float(self.Magnitude)
        dict["Distance"] = self.Distance
        dict["englishLink"]  =self.englishLink



        return dict