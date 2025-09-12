from app import create_app
import os
from app import db
import sys
import logging

class Constellation(db.Model):
    __tablename__ = 'Constellation'
    shortname = db.Column(db.String(16), primary_key=True)
    englishname = db.Column(db.String(32), unique=False)
    chinesename = db.Column(db.String(32), unique=False)
    japanesename = db.Column(db.String(32), unique=False)
    latinname = db.Column(db.String(32), unique=False)
    nasashortname = db.Column(db.String(32), unique=False)

    englishLink = db.Column(db.String(128), unique=False)
    chineseLink = db.Column(db.String(128), unique=False)
    japaneseLink = db.Column(db.String(128), unique=False)

    RightAscension = db.Column(db.String(32), unique=False)
    Declination = db.Column(db.String(32), unique=False)

    size = db.Column(db.String(32), unique=False)
    quadrant = db.Column(db.String(32), unique=False)
    family = db.Column(db.String(32), unique=False)
    brightest_ch = db.Column(db.String(32), unique=False)
    brightest_en = db.Column(db.String(32), unique=False)
    brightest_jp = db.Column(db.String(32), unique=False)

    genitive = db.Column(db.String(32), unique=False)
    oringin_en = db.Column(db.String(32), unique=False)
    meaning_en = db.Column(db.String(32), unique=False)

    oringin_jp = db.Column(db.String(32), unique=False)
    meaning_jp = db.Column(db.String(32), unique=False)
    boundary = db.Column(db.LargeBinary, unique=False)
    lines = db.Column(db.String(1000), unique=False)




    def __init__(self,dict):
        self.shortname = dict["shortname"]
        if  "englishname" in dict:
            self.englishname = dict["englishname"]
        else:
            self.englishname = ""

        if  "chinesename" in dict:
            self.chinesename = dict["chinesename"]
        else:
            self.chinesename = ""

        if  "japanesename" in dict:
            self.japanesename = dict["japanesename"]
        else:
            self.japanesename = ""

        if "englishLink" in dict:
            self.englishLink = dict["englishLink"]
        else:
            self.englishLink = ""

        if "chineseLink" in dict:
            self.chineseLink = dict["chineseLink"]
        else:
            self.chineseLink = ""

        if "japaneseLink" in dict:
            self.japaneseLink= dict["japaneseLink"]
        else:
            self.japaneseLink = ""


        if  "nasashortname" in dict:
            self.nasashortname = dict["nasashortname"]
        else:
            self.nasashortname = ""

        self.latinname = dict["latinname"]
        self.RightAscension = dict["RightAscension"]
        self.Declination = dict["Declination"]
        self.size = dict["size"]
        self.quadrant = dict["quadrant"]
        self.family = dict["family"]
        self.brightest_ch  =dict["brightest_ch"]
        self.brightest_en = ""
        self.brightest_jp = ""
        self.genitive = ""
        self.oringin_en  =""
        self.meaning_en = ""
        self.oringin_jp = ""
        self.meaning_jp = ""

    def constellationDict(self):
         dict = {}
         dict["shortname"] = self.shortname
         dict["englishname"] = self.englishname
         dict["chinesename"] = self.chinesename
         dict["japanesename"] = self.japanesename
         dict["latinname"] = self.latinname
         dict["nasashortname"] = self.nasashortname
         dict["RightAscension"] = self.RightAscension
         dict["Declination"] = self.Declination
         dict["size"] = self.size
         dict["quadrant"] = self.quadrant
         dict["family"] = self.family
         dict["englishLink"]  =self.englishLink
         dict["chineselink"] = self.chineseLink
         dict["japaneselink"] = self.japaneseLink

         dict["brightest_ch"] = self.brightest_ch
         dict["brightest_en"] = self.brightest_en
         dict["brightest_jp"] = self.brightest_jp
         dict["boundary"] = self.boundary.decode()
         dict["lines"] = self.lines

         dict["genitive"] = self.genitive
         dict["oringin_en"] = self.oringin_en
         dict["meaning_en"] = self.meaning_en
         dict["oringin_jp"] = self.oringin_jp
         dict["meaning_jp"] = self.meaning_jp




         return dict

    def constellationSummnaryDict(self):
         dict = {}
         dict["shortName"] = self.shortname
         dict["englishName"] = self.englishname
         dict["latinName"] = self.latinname
         dict["RightAscension"] = self.RightAscension
         dict["Declination"] = self.Declination



         return dict