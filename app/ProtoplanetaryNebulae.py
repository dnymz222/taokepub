from app import create_app
import os
from app import db
import sys
import logging

class ProtoplanetaryNebulae(db.Model):
    __tablename__ = 'ProtoplanetaryNebulae'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    Image = db.Column(db.String(164),unique=False)
    EnglishLink = db.Column(db.String(164), unique=False)
    ChineseLink = db.Column(db.String(164), unique=False)
    JapaneseLink = db.Column(db.String(164), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Name = db.Column(db.String(64),unique=False)
    ChineseName = db.Column(db.String(32), unique=False)
    JapaneseName = db.Column(db.String(32), unique=False)
    Messier = db.Column(db.String(32),unique=False)
    NGC = db.Column(db.String(32), unique=False)
    Other = db.Column(db.String(32), unique=False)
    DateDiscove = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(32), unique=False)
    ApparentMagnitude = db.Column(db.String(32), unique=False)
    Constellation = db.Column(db.String(32), unique=False)

    def __init__(self,Dict):
        self.Image  = Dict["Image"]
        self.EnglishLink = Dict["EnglishLink"]
        self.ChineseLink = ""
        self.JapaneseLink = ""
        self.RightAscension  =""
        self.Declination = ""
        self.Name = Dict["Name"]
        self.Messier = ""
        self.NGC = ""
        self.Other = Dict["Other"]
        self.DateDiscove = Dict["DateDiscove"]
        self.Distance = Dict["Distance"]
        self.ApparentMagnitude = ""
        self.Constellation = ""

    def protoplanetarynebulaeDict(self):
        dict = {}
        dict["Id"] = self.Id
        dict["Image"] = self.Image
        dict["EnglishLink"] = self.EnglishLink
        dict["ChineseLink"] = self.ChineseLink
        dict["JapaneseLink"] = self.JapaneseLink
        dict["RightAscension"]  =self.RightAscension
        dict["Declination"] = self.Declination
        dict["Name"]   = self.Name
        dict["JapaneseName"] = self.JapaneseName
        dict["ChineseName"] = self.ChineseName
        dict["Messier"]  =  self.Messier
        dict["NGC"] = self.NGC
        dict["Other"] = self.Other
        dict["DateDiscove"] = self.DateDiscove
        dict["Distance"] = self.Distance
        dict["ApparentMagnitude"] = self.ApparentMagnitude
        dict["Constellation"] = self.Constellation

        return dict

