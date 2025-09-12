#coding=utf8
from app import create_app
import os
from app import db
class appuser(db.Model):
    __tablename__ = 'appuser'
    deviceId = db.Column(db.String(64), primary_key=True)
    userId = db.Column(db.String(64), unique=False)
    userName = db.Column(db.String(64), unique=False)
    taobaoId= db.Column(db.String(64), unique=False)
    phone = db.Column(db.String(32), unique=False)
    pwd = db.Column(db.String(64), unique=False)
    icon = db.Column(db.String(160), unique=False)
    sex = db.Column(db.Integer, unique=False)
    age = db.Column(db.Integer, unique=False)
    city = db.Column(db.String(32), unique=False)
    appVersion= db.Column(db.String(32), unique=False)
    fromPid = db.Column(db.String(32), unique=False)
    promotionar = db.Column(db.BOOLEAN, unique=False)
    promnotionPid = db.Column(db.String(32), unique=False)
    promotionCode = db.Column(db.String(32), unique=False)
    channel = db.Column(db.String(32), unique=False)
    os = db.Column(db.String(16), unique=False)
    deviceName = db.Column(db.String(32), unique=False)
    osVersion  =  db.Column(db.String(32), unique=False)
    devicetoken = db.Column(db.String(64), unique=False)
    gid = db.Column(db.String(32), unique=False)


    def __init__(self,deviceId):
        self.deviceId = deviceId
        self.userId = ''
        self.userName = ''
        self.taobaoId = ''
        self.phone = ''
        self.pwd = ''
        self.icon = ''
        self.sex = 0
        self.age = 1
        self.city = ''
        self.appVersion = ''
        self.fromPid = ''
        self.promotionar = False
        self.promnotionPid = ''
        self.promotionCode = ''
        self.channel = ''
        self.os = ''
        self.deviceName = ''
        self.osVersion = ''
        self.devicetoken = ''
        self.gid = ''


