#coding=utf8
from app import create_app
import os
import sys
from app import db



class appconfig(db.Model):
    __tablename__ = 'appconfig'
    source= db.Column(db.String(60), primary_key=True)
    sourceName = db.Column(db.String(60), unique=False)
    defalutPid = db.Column(db.String(60), unique=False)
    accessToken = db.Column(db.String(160), unique=False)
    accessTime =  db.Column(db.Integer, unique=False)
    currentVersion = db.Column(db.String(20), unique=False)
    sourceUrl = db.Column(db.String(160), unique=False)
    showdiscount = db.Column(db.Integer, unique=False)  #小程序显示淘口令
    appkey = db.Column(db.String(32), unique=False)
    appsecret = db.Column(db.String(100), unique=False)
    taokeAppkey = db.Column(db.String(32), unique=False)
    toakeSecret = db.Column(db.String(100), unique=False)
    openTaobao = db.Column(db.Integer, unique=False)
    type = db.Column(db.Integer, unique=False)  #0.小程序 1.iOS  2.安卓  3.网站
    token = db.Column(db.String(64), unique=False)
    image = db.Column(db.String(240), unique=False)
    open = db.Column(db.Integer, unique=False)
    message = db.Column(db.String(60), unique=False)





    def configdict(self):
        dict ={}
        dict['source'] = self.source
        dict['soucename'] = self.sourceName
        dict['defalutPid'] =self.defalutPid
        dict['accessToken'] = self.accessToken
        dict['accessTime'] =self.accessTime
        dict['type'] = self.type
        dict['currentVersion'] = self.currentVersion
        dict['sourceUrl'] = self.sourceUrl
        dict['showdiscount'] = self.showdiscount
        dict['openTaobao'] = self.openTaobao
        dict['accessToken'] =self.accessToken
        dict['token'] = self.token
        dict['image']  =self.image
        dict['open'] = self.open
        dict['message'] = self.message
        return dict

    def configtokendict(self):
        dict = {}
        dict['accessToken'] = self.acessToken
        dict['accessTime'] = self.accessTime
        return dict


