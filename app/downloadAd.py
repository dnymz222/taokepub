#coding=utf8
from app import create_app
import os
from app import db


class downloadAd(db.Model):
    __tablename__ = 'download_ad'
    adId = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=False)
    packagename = db.Column(db.String(64), unique=False)
    downloadurl = db.Column(db.String(160), unique=False)
    des = db.Column(db.String(160), unique=False)
    subtext = db.Column(db.String(64), unique=False)
    action = db.Column(db.String(16), unique=False)
    icon = db.Column(db.String(160), unique=False)
    plat = db.Column(db.Integer, unique=False)
    status = db.Column(db.SmallInteger, unique=False)  # 0:失效 1：有效
    index = db.Column(db.Integer, unique=False)
    channel = db.Column(db.String(64),unique=False)




    def downloaddict(self):
        dict = {}
        dict["name"] = self.name
        dict["packagename"] = self.packagename
        dict['downloadurl'] = self.downloadurl
        dict['icon'] = self.icon
        dict['des']  = self.des
        dict["action"] = self.action
        dict["subtext"] = self.subtext
        dict["adId"] = self.adId
        return dict

        