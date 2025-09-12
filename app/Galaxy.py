from app import create_app
import os
from app import db
import sys
import logging

class Galaxy(db.Model):
    __tablename__ = 'Galaxy'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    EnglishName = db.Column(db.String(64), unique=True)

    EnglishLink  = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    ChineseName = db.Column(db.String(32), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)
    JapaneseName = db.Column(db.String(32), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Constellation = db.Column(db.String(32), unique=False)
    OriginOfName = db.Column(db.String(320), unique=False)
    Distance = db.Column(db.String(64), unique=False)
    Image = db.Column(db.String(256), unique=False)
    ApparentMagnitude = db.Column(db.String(16), unique=False)


    def __init__(self,dict):
        self.EnglishName = dict["EnglishName"]
        self.EnglishLink = dict["EnglishLink"]
        self.ChineseLink = ""
        self.ChineseName = ""
        self.JapaneseLink = ""
        self.JapaneseName = ""
        self.RightAscension = ""
        self.Declination  =""
        self.Constellation = dict["Constellation"]
        self.OriginOfName = dict["OriginOfName"]
        self.Distance = ""
        self.Image = dict["Image"]
        self.ApparentMagnitude = ""

    def galaxydict(self):
        dict = {}
        dict["Id"] = self.Id
        dict["EnglishName"]  = self.EnglishName
        dict["EnglishLink"]  = self.EnglishLink
        dict["ChineseLink"]  = self.ChineseLink
        dict["ChineseName"]  = self.ChineseName
        dict["JapaneseLink"] = self.JapaneseLink
        dict["JapaneseName"]  = self.JapaneseName
        dict["RightAscension"]  =self.RightAscension
        dict["Declination"]  = self.Declination
        dict["Constellation"]  =self.Constellation
        dict["OriginOfName"] = self.OriginOfName
        dict["Distance"]  = self.Distance
        dict["Image"]  =self.Image
        dict["ApparentMagnitude"]  =self.ApparentMagnitude
        return dict


