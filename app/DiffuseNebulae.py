from app import create_app
import os
from app import db
import sys
import logging

class DiffuseNebulae(db.Model):
    __tablename__ = 'DiffuseNebulae'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    Name = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(64), unique=False)
    Image = db.Column(db.String(164), unique=False)
    EnglishLink = db.Column(db.String(164), unique=False)
    ChineseLink = db.Column(db.String(164), unique=False)
    JapaneseLink = db.Column(db.String(164), unique=False)
    ChineseName = db.Column(db.String(32), unique=False)
    JapaneseName = db.Column(db.String(32), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    ApparentMagnitude = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(32), unique=False)
    Constellation = db.Column(db.String(32), unique=False)


    def __init__(self,Dict):
        self.Name = Dict["Name"]
        self.title = Dict["title"]
        self.EnglishLink = Dict["EnglishLink"]
        self.Image = ""
        self.ChineseLink = ""
        self.JapaneseLink = ""
        self.RightAscension = ""
        self.Declination = ""
        self.ApparentMagnitude = ""
        self.Distance = ""
        self.Constellation = ""


    def diffuseDict(self):
        dict  ={}
        dict["Id"] = self.Id
        dict["Name"] = self.Name
        dict["title"] = self.title
        dict["Image"]  =self.Image
        dict["EnglishLink"] = self.EnglishLink
        dict["ChineseLink"]  = self.ChineseLink
        dict["JapaneseLink"] =  self.JapaneseLink
        dict["ChineseName"]  = self.ChineseName
        dict["JapaneseName"] = self.JapaneseName
        dict["RightAscension"] = self.RightAscension
        dict["Declination"] = self.Declination
        dict["ApparentMagnitude"] = self.ApparentMagnitude
        dict["Distance"]  = self.Distance
        dict["Constellation"] = self.Constellation
        return dict
