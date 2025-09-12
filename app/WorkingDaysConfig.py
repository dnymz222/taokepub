#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime
import json

class WorkingDaysConfig(db.Model):
    __tablename__ = 'workingdaysconfig'
    configId = db.Column(db.String(64), primary_key=True)  #
    code =  db.Column(db.String(16), unique=False)
    configurations = db.Column(db.String(800), unique=False)  #
    default_configuration = db.Column(db.String(64), unique=False)
    website = db.Column(db.String(64), unique=False)
    flag = db.Column(db.String(160), unique=False)


    def __init__(self,dict):
        self.configId = dict["configId"]
        self.code = dict["code"]
        self.configurations = dict["configurations"]
        self.default_configuration = dict["default_configuration"]
        self.website = dict["website"]
        self.flag = ""

    def workingdayconfigdict(self):
        dict = {}
        dict["configId"] = self .configId
        dict["code"] = self.code
        dict["website"] = self.website
        dict["flag"] = self.flag
        dict["configurations"] = json.loads(self.configurations)
        dict["default_configuration"] = self.default_configuration
        return dict

