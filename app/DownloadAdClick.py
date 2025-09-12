#coding=utf8
from app import create_app
import os
from app import db


class downloadAdClick(db.Model):
    __tablename__ = 'download_ad_click'
    logId = db.Column(db.Integer, primary_key=True,autoincrement=True)
    adId = db.Column(db.String(16), unique=False)
    day = db.Column(db.String(16), unique=False)
    app = db.Column(db.String(16), unique=False)
    type = db.Column(db.String(16), unique=False)



    def __init__(self,day,adId,app):
        self.adId = adId
        self.day = day
        self.app = app
        self.type = "1"


    def downloadclickdict(self):
        dict = {}
        dict["adId"] = self.adId
        dict["app"] = self.app
        dict['day'] = self.day
        dict["type"] = self.type

        return dict


