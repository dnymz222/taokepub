from app import create_app
import os
from app import db
import sys
import logging

class Star(db.Model):
    __tablename__ = 'star'

    CombinedId = db.Column(db.String(64), primary_key=True)

    BaierId = db.Column(db.String(32), unique=False)
    HDId =db.Column(db.String(32), unique=False)
    HIPId = db.Column(db.String(32), unique=False)
    ChineseName = db.Column(db.String(64), unique=False)
    JapaneseName = db.Column(db.String(64), unique=False)
    EnglishName = db.Column(db.String(64), unique=False)
    ShortName = db.Column(db.String(32), unique=False)
    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)

    ConsetellationName = db.Column(db.String(32), unique=False)
    Magnitude = db.Column(db.String(32), unique=False)
    AbsoluteMagnitude = db.Column(db.String(32), unique=False)
    Distance= db.Column(db.String(32), unique=False)
    SpectralType =  db.Column(db.String(32), unique=False)
    EnglishLink = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)




    def __init__(self, dict):
        self.CombinedId = dict['CombinedId']
        self.BaierId = dict["BaierId"]
        self.HDId = dict["HDId"]
        self.HIPId = dict["HIPId"]
        # self.ChineseName = dict['ChineseName']
        # self.JapaneseName = dict["JapaneseName"]
        self.EnglishName = dict["EnglishName"]
        self.ShortName = dict["ShortName"]
        self.ConsetellationName = dict["ConsetellationName"]
        self.Magnitude = dict["Magnitude"]
        self.AbsoluteMagnitude = dict["AbsoluteMagnitude"]
        self.SpectralType = dict["SpectralType"]
        self.RightAscension = dict["RightAscension"]
        self.Declination = dict["Declination"]
        self.EnglishLink = dict['EnglishLink']
        # self.ChineseLink = dict['ChineseLink']
        # self.JapaneseLink = dict["JapaneseLink "]
        self.Distance = dict["Distance"]
        self.ChineseLink =""
        self.ChineseName =""
        self.JapaneseLink = ""
        self.JapaneseName =""

    def starsummarydict(self):
        dict ={}
        dict['CombinedId'] = self.CombinedId

        dict["EnglishName"] = self.EnglishName

        dict["ShortName"] = self.ShortName

        dict["Magnitude"] =  float(self.Magnitude)

        dict["ConsetellationName"] = self.ConsetellationName

        dict["RightAscension"] = self.RightAscension
        dict["Declination"] = self.Declination
        dict["Distance"] = self.Distance



        return dict

    def stardict(self):
        dict ={}
        dict['CombinedId'] = self.CombinedId
        dict["BaierId"] = self.BaierId
        dict["HDId"]  =self.HDId
        dict["HIPId"] = self.HIPId
        dict["EnglishName"] = self.EnglishName
        # dict["ChineseName"]  =self.ChineseName
        # dict["JapaneseName"]  = self.JapaneseName
        dict["ShortName"] = self.ShortName
        dict["ConsetellationName"] = self.ConsetellationName
        dict["Magnitude"] =  float(self.Magnitude)
        dict["AbsoluteMagnitude"] = self.AbsoluteMagnitude
        dict["SpectralType"] = self.SpectralType
        dict["RightAscension"] = self.RightAscension
        dict["Declination"] = self.Declination
        dict["Distance"] = self.Distance

        dict["EnglishLink"] = self.EnglishLink
        # link = ""
        # if  len(self.EnglishLink) > 5:
        #     link = link +"1"
        # else:
        #     link = link +"0"
        #
        # if len(self.ChineseLink) > 5:
        #     link = link + "1"
        # else:
        #     link = link + "0"
        #
        # if len(self.JapaneseLink) > 5:
        #     link = link + "1"
        # else:
        #     link = link + "0"
        #
        # dict["L"] = link



        return dict


    def starshortdict(self):
        dict ={}
        dict['C'] = self.CombinedId
       # dict["B"] = self.BaierId
       #  dict["H"]  =self.HDId
       #  dict["HI"] = self.HIPId
        dict["En"] = self.EnglishName
        dict["Ch"]  =self.ChineseName
        dict["Ja"]  = self.JapaneseName
        # dict["Sh"] = self.ShortName
        # dict["Co"] = self.ConsetellationName
        dict["Ma"] = self.Magnitude
        # dict["A"] = self.AbsoluteMagnitude
        # dict["S"] = self.SpectralType
        dict["RA"] = self.RightAscension
        dict["D"] = self.Declination
        # dict["D"] = self.Distance
        # link = ""
        # if  len(self.EnglishLink) > 5:
        #     link = link +"1"
        # else:
        #     link = link +"0"
        #
        # if len(self.ChineseLink) > 5:
        #     link = link + "1"
        # else:
        #     link = link + "0"
        #
        # if len(self.JapaneseLink) > 5:
        #     link = link + "1"
        # else:
        #     link = link + "0"
        #
        # dict["L"] = link
        return dict









