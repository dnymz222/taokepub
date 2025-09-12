from app import create_app
import os
from app import db
import sys
import logging

class NGCC(db.Model):
    __tablename__ = 'NGCC'
    number = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(32), unique=False)
    englishLink =db.Column(db.String(128), unique=False)
    chineseLink = db.Column(db.String(128), unique=False)
    japaneseLink =  db.Column(db.String(128), unique=False)

    otherName = db.Column(db.String(64), unique=False)
    obejectType = db.Column(db.String(64), unique=False)
    constellation = db.Column(db.String(64), unique=False)
    RightAscension = db.Column(db.String(64), unique=False)
    Declination = db.Column(db.String(64), unique=False)
    Magnitude = db.Column(db.String(64), unique=False)


    def __init__(self,dict):
        self.number = dict["number"]
        self.otherName  = dict["otherName"]
        self.obejectType = dict["obejectType"]
        self.constellation = dict["constellation"]
        self.RightAscension = dict["RightAscension"]
        self.Declination = dict["Declination"]
        self.Magnitude = dict["Magnitude"]
        self.title = dict["title"]
        self.englishLink = dict["englishLink"]
        self.japaneseLink = ""
        self.chineseLink = ""

    def NGCCDict(self):
        dict = {}
        dict['number']  =self.number
        dict["otherName"] = self.otherName
        dict["obejectType"] = self.obejectType
        dict["constellation"]  =self.constellation
        dict["RightAscension"]  =self.RightAscension
        dict["Declination"]  =self.Declination
        dict["Magnitude"] = self.Magnitude
        dict["title"] = self.title
        dict["englishLink"]  =self.englishLink
        dict["japaneseLink"]  =self.japaneseLink
        dict["chineseLink"] = self.chineseLink
        return dict
