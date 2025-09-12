#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging

class Comet(db.Model):
    __tablename__ = 'Comet'
    number = db.Column(db.String(32), primary_key=True)
    Englishname = db.Column(db.String(32), unique=False)
    Chinesename = db.Column(db.String(32), unique=False)
    Japanesename = db.Column(db.String(32), unique=False)
    EnglishLink = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)


    OrbitalPeriod = db.Column(db.String(32), unique=False) #period
    SemeMajorAxis = db.Column(db.String(32), unique=False) #a
    Inclination = db.Column(db.String(32), unique=False)  #i
    Ecc = db.Column(db.String(32), unique=False)   #e
    PerihelionDistance = db.Column(db.String(32), unique=False)  #q
    LongitudeAscendingNode = db.Column(db.String(32), unique=False) #node
    PerihelionArgument = db.Column(db.String(32), unique=False) #peri
    MeanAnomaly = db.Column(db.String(32), unique=False) #M
    PerihelionPassageTime = db.Column(db.String(32), unique=False) #tp
    MeanMotion = db.Column(db.String(32), unique=False) #n
    AphelionDistance = db.Column(db.String(32), unique=False) #Q

    Epoch = db.Column(db.String(32), unique=False) #
    MotionType = db.Column(db.SmallInteger,unique=False) #1.椭圆 2.抛物线 3.准抛物线
    TotalMagnitude = db.Column(db.String(32), unique=False) #M1
    TotalMagnitudeSlope = db.Column(db.String(32), unique=False)  # K1



    Magnitude = db.Column(db.String(16), unique=False)
    Classname = db.Column(db.String(16), unique=False)
    NEC = db.Column(db.Boolean,unique = False)
    Ref = db.Column(db.String(128), unique=False)


    def __init__(self,dict):
        self.number = dict["number"]
        self.Englishname = dict["number"]
        self.Chinesename = self.Englishname
        self.Japanesename = self.Englishname
        self.EnglishLink = ""
        self.ChineseLink = ""
        self.JapaneseLink =""

        self.OrbitalPeriod = str(dict["OrbitalPeriod"])
        self.SemeMajorAxis = str(dict["SemeMajorAxis"])
        self.Inclination = str(dict["Inclination"])
        self.Ecc = str( dict["Ecc"])
        self.Epoch = str(dict["Epoch"])
        self.PerihelionDistance =str( dict["PerihelionDistance"])
        self.LongitudeAscendingNode = str( dict["LongitudeAscendingNode"])
        self.PerihelionArgument = str(dict["PerihelionArgument"])
        self.MeanAnomaly = str(dict["MeanAnomaly"])
        self.PerihelionPassageTime = str(dict["PerihelionPassageTime"])
        self.MeanMotion = str(dict["MeanMotion"])
        self.AphelionDistance =str( dict["AphelionDistance"])
        self.TotalMagnitude = str(dict["TotalMagnitude"])
        self.TotalMagnitudeSlope =str(dict["TotalMagnitudeSlope"])
        self.MotionType  = dict["MotionType"]


        self.Magnitude  = ""
        self.Classname = ""
        self.NEC = False
        self.Ref = ""



    def cometDict(self):
        dict = {}
        dict["number"]  =self.number
        dict["Englishname"]  = self.Englishname
        dict["Chinesename"] = self.Chinesename
        dict["Japanesename"]  =self.Japanesename
        dict["EnglishLink"]  = self.EnglishLink
        dict["ChineseLink"] = self.ChineseLink
        dict["JapaneseLink"] = self.JapaneseLink
        dict["OrbitalPeriod"]  = self.OrbitalPeriod
        dict["SemeMajorAxis"]  =self.SemeMajorAxis
        dict["Inclination"] = self.Inclination
        dict["Ecc"] = self.Ecc
        dict["PerihelionDistance"] =  self.PerihelionDistance
        dict["LongitudeAscendingNode"] = self.LongitudeAscendingNode
        dict["PerihelionArgument"] = self.PerihelionArgument
        dict["MeanAnomaly"] = self.MeanAnomaly
        dict["PerihelionPassageTime"] = self.PerihelionPassageTime
        dict["MeanMotion"] = self.MeanMotion
        dict["AphelionDistance"] = self.AphelionDistance
        dict["Epoch"] = self.Epoch
        dict["MotionType"] = self.MotionType
        dict["TotalMagnitude"] = self.TotalMagnitude
        dict["TotalMagnitudeSlope"] = self.TotalMagnitudeSlope

        dict["Magnitude"] = self.Magnitude
        dict["Classname"] = self.Classname
        dict["NEC"] = self.NEC
        dict["Ref"] = self.Ref
        return dict









