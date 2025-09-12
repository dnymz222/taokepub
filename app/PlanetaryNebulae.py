from app import create_app
import os
from app import db
import sys
import logging

class PlanetaryNebulae(db.Model):
    __tablename__ = 'PlanetaryNebulae'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    Image = db.Column(db.String(164),unique=False)
    EnglishLink = db.Column(db.String(164), unique=False)
    ChineseLink = db.Column(db.String(164), unique=False)
    JapaneseLink = db.Column(db.String(164), unique=False)
    ChineseName = db.Column(db.String(32), unique=False)
    JapaneseName = db.Column(db.String(32), unique=False)
    Name = db.Column(db.String(64),unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Messier = db.Column(db.String(32),unique=False)
    NGC = db.Column(db.String(32), unique=False)
    Other = db.Column(db.String(32), unique=False)
    DateDiscove = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(32), unique=False)
    ZONE = db.Column(db.String(32), unique=False)
    ApparentMagnitude = db.Column(db.String(32), unique=False)
    Constellation = db.Column(db.String(32), unique=False)

    def __init__(self,Dict):
        self.ZONE = Dict["Zone"]
        self.Image  = Dict["Image"]
        self.Name =  Dict["Name"]
        self.EnglishLink = Dict["EnglishLink"]
        self.ChineseLink = self.ChineseLink
        self.JapaneseLink = self.JapaneseLink

        self.Messier = Dict["Messier"]
        self.NGC = Dict["NGC"]
        self.Other = Dict["Other"]
        self.DateDiscove = Dict["DateDiscove"]
        self.Distance = Dict["Distance"]
        self.ApparentMagnitude = Dict["ApparentMagnitude"]
        self.Constellation = Dict["Constellation"]
        self.RightAscension = ""
        self.Declination = ""
    def planetarynebulaeDict(self):
        dict  = {}
        dict["ZONE"] = self.ZONE
        dict["Image"] = self.Image
        dict["EnglishLink"] = self.EnglishLink
        dict["ChineseLink"] = self.ChineseLink
        dict["JapaneseLink"] = self.JapaneseLink
        dict["Name"] = self.Name
        dict["RightAscension"]  = self.RightAscension
        dict["Declination"] = self.Declination
        dict["Messier"] = self.Messier
        dict["NGC"] = self.NGC
        dict["Other"] = self.Other
        dict["DateDiscove"] = self.DateDiscove
        dict["Distance"] = self.Distance
        dict["ApparentMagnitude"] = self.ApparentMagnitude
        dict["Constellation"] = self.Constellation
        dict["ChineseName"] = self.ChineseName
        dict["JapaneseName"] = self.JapaneseName

        return dict

