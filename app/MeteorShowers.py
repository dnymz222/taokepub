from app import create_app
import os
from app import db
import sys
import logging

class MeteorShowers(db.Model):
    __tablename__ = 'MeterShowers'
    showerId =  db.Column(db.String(20),primary_key=True)
    shortname = db.Column(db.String(16))
    
    classlevel =  db.Column(db.SmallInteger, unique=False)
    englishname = db.Column(db.String(32), unique=False)
    chinesename = db.Column(db.String(32), unique=False)
    japanesename = db.Column(db.String(32), unique=False)
    ActivityPeriod = db.Column(db.String(32), unique=False)
    SL= db.Column(db.String(32), unique=False)
    Maximum = db.Column(db.String(32), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Velocity = db.Column(db.String(32), unique=False)
    r = db.Column(db.String(16), unique=False)
    ZHR = db.Column(db.String(32), unique=False)
    time = db.Column(db.String(32), unique=False)
    moon= db.Column(db.String(32), unique=False)
    englishLink = db.Column(db.String(128), unique=False)
    chineseLink = db.Column(db.String(128), unique=False)
    japaneseLink = db.Column(db.String(128), unique=False)
    show = db.Column(db.Boolean, unique=False)
    year = db.Column(db.String(32), unique=False)
    index = db.Column(db.Integer,unique=False)

    def __init__(self,dict):
        self.shortname = dict["shortname"]
        self.classlevel = dict["classlevel"]
        self.englishname = dict["englishname"]
        self.chinesename = dict["chinesename"]
        self.japanesename = dict["japanesename"]
        self.ActivityPeriod = dict["ActivityPeriod"]
        self.SL = str(dict["SL"])
        self.Maximum = dict["Maximum"]
        self.RightAscension = dict["RightAscension"]
        self.Declination = dict["Declination"]
        self.Velocity = dict["Velocity"]
        self.r = str(int(dict["r"]))
        self.ZHR = str(int(dict["ZHR"]))
        self.time =str(int(dict["time"]))
        self.moon  =str(int(dict["moon"]))
        self.englishLink = ""
        self.chineseLink  =""
        self.japaneseLink = ""
        self.show = dict["show"]
        self.year =str(int(dict["year"]))
        self.index = dict["index"]
        self.showerId  = self.shortname+"_"+self.year

    def meteoshowersDict(self):
        dict = {}
        dict["shortname"]  =self.shortname
        dict["classlevel"] = self.classlevel
        dict["englishname"]  = self.englishname
        dict["chinesename"] = self.chinesename
        dict["japanesename"] = self.japanesename
        dict["ActivityPeriod"]  =self.ActivityPeriod
        dict["SL"] = self.SL
        dict["Maximum"] = self.Maximum
        dict["RightAscension"]  =self.RightAscension
        dict["Declination"]  =self.Declination
        dict["Velocity"]  =self.Velocity
        dict["r"]  =self.r
        dict["ZHR"]  =self.ZHR
        dict["time"] = self.time
        dict["moon"]  =self.moon
        dict["englishLink"]  =self.englishLink
        dict["chineseLink"] = self.chineseLink
        dict["japaneseLink"] = self.japaneseLink
        dict["show"] = self.show
        dict["year"] = self.year

        return dict






