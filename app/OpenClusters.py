from app import create_app
import os
from app import db
import sys
import logging

class OpenClusters(db.Model):
    __tablename__ = 'OpenClusters'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    Identifier = db.Column(db.String(36), unique=True)
    EnglishLink  = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)
    ChineseName = db.Column(db.String(32), unique=False)
    JapaneseName = db.Column(db.String(32), unique=False)
    Image = db.Column(db.String(256), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Constellation = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(16), unique=False)
    Age = db.Column(db.String(16), unique=False)
    ApparentMagnitude = db.Column(db.String(16), unique=False)
    Diameter = db.Column(db.String(16), unique=False)


    def __init__(self,dict):
        self.Identifier = dict["Identifier"]
        self.EnglishLink = dict["EnglishLink"]
        self.JapaneseLink = ""
        self.ChineseLink = ""
        self.RightAscension = dict["RightAscension"]
        self.Declination = dict["Declination"]
        self.Constellation = dict["Constellation"]
        self.ApparentMagnitude = dict["ApparentMagnitude"]
        self.Diameter = dict["Diameter"]
        self.Age = dict["Age"]
        self.Distance = dict["Distance"]
        self.Image = ""

    def openclusterDict(self):
        dict = {}
        dict["Id"] = self.Id
        dict["Identifier"] = self.Identifier
        dict["EnglishLink"] = self.EnglishLink
        dict["JapaneseLink"] = self.JapaneseLink
        dict["ChineseLink"] = self.ChineseLink
        dict["RightAscension"] = self.RightAscension
        dict["ChineseName"] = self.ChineseName
        dict["JapaneseName"] = self.JapaneseName
        dict["Declination"] = self.Declination
        dict["Constellation"] = self.Constellation
        dict["ApparentMagnitude"] = self.ApparentMagnitude
        dict["Diameter"]  =self.Diameter
        dict["Age"] = self.Age
        dict["Distance"] = self.Distance
        dict["Image"] = self.Image
        return dict
