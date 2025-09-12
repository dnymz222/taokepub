#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging
import time
import datetime


class VipUser(db.Model):
    __tablename__ = 'VipUser'

    PhoneNumberApp = db.Column(db.String(64), primary_key=True)
    PhoneNumber = db.Column(db.String(32),unique=False)
    registerdate = db.Column(db.Date,unique=False)
    password = db.Column(db.String(80), unique=False)
    isvip  = db.Column(db.Boolean,unique=False)
    type = db.Column(db.Integer,unique=False)  #0.非会员 1.包年 2.终身
    startdate = db.Column(db.Date,unique=False)
    app = db.Column(db.String(32),unique=False)
    trade_no = db.Column(db.String(64), unique=False)


    def __init__(self,Phone,App):
        self.PhoneNumberApp = Phone + App
        self.PhoneNumber = Phone
        nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
        self.registerdate = nowTime
        self.isvip = False
        self.type = 0
        self.startdate = nowTime
        self.app = App
        self.password = ""
        self.trade_no = ""


    def vipDict(self):
        dict = {}
        dict["PhoneNumberApp"] = self.PhoneNumberApp
        dict["PhoneNumber"] = self.PhoneNumber
        dict["registerdate"]  = self.registerdate.strftime('%Y-%m-%d')
        dict["isvip"] = self.isvip
        dict["type"]  =self.type
        dict["startdate"] = self.startdate.strftime('%Y-%m-%d')
        dict["app"] = self.app
        if len(self.password) > 6:
            dict["haspassword"] = True
        else:
            dict["haspassword"] = False
        dict["trade_no"] = self.trade_no

        return dict







