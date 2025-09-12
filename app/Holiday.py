#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging
import json

class Holiday(db.Model):
    __tablename__ = 'Holiday'
    uuid = db.Column(db.String(64), primary_key=True)
    date = db.Column(db.String(16), unique=False)
    observed = db.Column(db.String(16), unique=False) #是否顺延
    name = db.Column(db.String(169), unique=False)
    region = db.Column(db.String(64), unique=False)
    regionCode = db.Column(db.String(64), unique=False)
    type =  db.Column(db.Integer, unique=False)  #1.公共假日 0.非公共假日 2.周末调休成工作日
    year = db.Column(db.Integer, unique=False)
    month = db.Column(db.Integer, unique=False)
    code = db.Column(db.String(64), unique=False)

    enName = db.Column(db.String(160), unique=False)
    frName = db.Column(db.String(160), unique=False)
    jaName = db.Column(db.String(160), unique=False)
    esName = db.Column(db.String(160), unique=False)
    ptName = db.Column(db.String(160), unique=False)
    ruName = db.Column(db.String(160), unique=False)
    deName = db.Column(db.String(160), unique=False)
    itName = db.Column(db.String(160), unique=False)
    koName = db.Column(db.String(160), unique=False)
    vtName =  db.Column(db.String(160), unique=False)
    zhName =  db.Column(db.String(160), unique=False)
    zhtName = db.Column(db.String(160), unique=False)
    maName =  db.Column(db.String(160), unique=False)



    def __init__(self,dict):

        self.date = dict["date"]



    def  hoildaydict(self):
        dict = {}
        dict["date"] = self.date
        dict["code"] =  self.code
        dict["year"] = self.year
        dict["localName"] = self.localName
        dict["name"] = self.name
        dict["region"] = self.region
        dict["regionCode"] = self.regionCode
        dict["fixed"]  = self.fixed
        dict["isglobal"] = self.isglobal
        dict["regions"]  =self.regions
        dict["launchYear"]  =self.launchYear
        dict["type"]  =self.type
        return dict


