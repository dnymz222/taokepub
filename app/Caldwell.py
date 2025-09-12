from app import create_app
import os
from app import db
import sys
import logging

class Caldwell(db.Model):
    __tablename__ = 'Caldwell'
    number = db.Column(db.String(16), primary_key=True)
    NGCCIC_number = db.Column(db.String(64), unique=False)
    picture= db.Column(db.String(164), unique=False)
    commonName = db.Column(db.String(64), unique=False)
    obejectType = db.Column(db.String(64), unique=False)
    constellation = db.Column(db.String(64), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)
    Magnitude = db.Column(db.String(32), unique=False)
    Distance = db.Column(db.String(32), unique=False)
    EnglishLink = db.Column(db.String(128), unique=False)


    def __init__(self, dict):
        self.number = dict["number"]
        self.NGCCIC_number = dict["NGCCIC_number"]

        self.picture = dict["picture"]
        self.commonName = dict["commonName"]
        self.obejectType = dict["obejectType"]
        self.constellation = dict["constellation"]
        self.Declination = dict["Declination"]
        self.RightAscension = dict["RightAscension"]
        self.Magnitude = dict["Magnitude"]
        self.Distance = dict["Distance"]
        self.EnglishLink = dict["EnglishLink"]

    def caldwellDict(self):
        dict = {}
        dict["number"] = self.number
        dict["NGCCIC_number"] = self.NGCCIC_number
        dict["picture"] = self.picture
        dict["commonName"] = self.commonName
        dict["obejectType"] = self.obejectType
        dict["constellation"] = self.constellation
        dict["RightAscension"] = self.RightAscension
        dict["Declination"]  =self.Declination
        dict["Magnitude"] = self.Magnitude
        dict["Distance"] = self.Distance
        dict["EnglishLink"]   = self.EnglishLink
        return dict