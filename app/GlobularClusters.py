from app import create_app
import os
from app import db
import sys
import logging

class GlobularClusters(db.Model):
    __tablename__ = 'GlobularClusters'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    Identifier = db.Column(db.String(32), unique=True)
    EnglishLink  = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)
    ChineseName = db.Column(db.String(32), unique=False)
    JapaneseName = db.Column(db.String(32), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Constellation = db.Column(db.String(32), unique=False)
    Region = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(16), unique=False)
    Image = db.Column(db.String(256), unique=False)
    ApparentMagnitude = db.Column(db.String(16), unique=False)
    Diameter = db.Column(db.String(16), unique=False)
    Galaxy = db.Column(db.String(16), unique=False)

    # def __init__(self,dict):
    #     self.Identifier = dict["Identifier"]
    #     self.EnglishLink = dict["EnglishLink"]
    #     self.JapaneseLink = ""
    #     self.ChineseLink = ""
    #     self.RightAscension = dict["RightAscension"]
    #     self.Declination = dict["Declination"]
    #     self.Constellation = dict["Constellation"]
    #     self.Region = dict["Region"]
    #     self.ApparentMagnitude = dict["ApparentMagnitude"]
    #     self.Diameter = dict["Diameter"]
    #     self.Distance = ""
    #     self.Image = ""
    #     self.Galaxy = ""

    def __init__(self,dict):
        self.Identifier = dict["Identifier"]
        self.EnglishLink = dict["EnglishLink"]
        self.JapaneseLink = ""
        self.ChineseLink = ""
        self.RightAscension = dict["RightAscension"]
        self.Declination = dict["Declination"]
        self.Constellation = ""
        self.Region = dict["Region"]
        self.ApparentMagnitude = dict["ApparentMagnitude"]
        self.Diameter = dict["Diameter"]
        self.Distance = ""
        self.Image = ""
        self.Galaxy = dict["Galaxy"]

    def gloubarclusterDict(self):
        dict = {}
        dict["Id"]  =self.Id
        dict["Identifier"] = self.Identifier
        dict["EnglishLink"] = self.EnglishLink
        dict["JapaneseLink"] = self.JapaneseLink
        dict["ChineseLink"] = self.ChineseLink
        dict["ChineseName"] = self.ChineseName
        dict["JapaneseName"] = self.JapaneseName
        dict["RightAscension"] = self.RightAscension
        dict["Declination"] = self.Declination
        dict["Constellation"] = self.Constellation
        dict["Region"] = self.Region
        dict["ApparentMagnitude"] = self.ApparentMagnitude
        dict["Diameter"]  =self.Diameter
        dict["Image"] = self.Image
        dict["Distance"]  = self.Distance
        dict["Galaxy"] = self.Galaxy
        return dict


