#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging

class Asteroid(db.Model):
    __tablename__ = 'Asteroid'
    number = db.Column(db.String(32), primary_key=True)
    Englishname = db.Column(db.String(32), unique=False)
    Chinesename = db.Column(db.String(32), unique=False)
    Japanesename = db.Column(db.String(32), unique=False)



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

    Epoch = db.Column(db.String(32), unique=False)
    MotionType = db.Column(db.SmallInteger,unique=False) #1.椭圆 2.抛物线 3.准抛物线
    TotalMagnitude = db.Column(db.String(32), unique=False) #M1
    TotalMagnitudeSlope = db.Column(db.String(32), unique=False)  # K1



    Ref = db.Column(db.String(128), unique=False)


    def __init__(self,dict):
        self.number = dict["number"]
        self.Englishname = dict["Englishname"]
        self.Chinesename = ""
        self.Japanesename = ""
        self.EnglishLink = dict["EnglishLink"]
        self.ChineseLink = ""
        self.JapaneseLink =""
        self.OrbitalPeriod = dict["OrbitalPeriod"]
        self.SemeMajorAxis = dict["SemeMajorAxis"]
        self.Inclination = dict["Inclination"]
        self.Ecc = dict["Ecc"]
        self.Magnitude  = dict["Magnitude"]
        self.Classname = dict["Classname"]
        self.NEC = dict["NEC"]
        self.Ref = dict["Ref"]

    def asteroidDict(self):
        dict = {}
        dict["number"]  =self.number
        dict["Englishname"]  = self.Englishname
        dict["Chinesename"] = self.Chinesename
        dict["Japanesename"]  =self.Japanesename


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


        return dict
