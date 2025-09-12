#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime

class welfare(db.Model):
    __tablename__ = 'welfare'
    welfareId = db.Column(db.String(32), primary_key=True)

    name = db.Column(db.String(200), unique=False)
    image = db.Column(db.String(320), unique=False)
    status = db.Column(db.SmallInteger, unique=False)  # 0:失效 1：有效
    type = db.Column(db.SmallInteger, unique=False)  # 0:没有安装app进行推广  1：有安装app打开链接
    endTime = db.Column(db.Date, unique=False, index=True)
    onTime = db.Column(db.Date, unique=False, index=True)
    activeUrl = db.Column(db.String(320), unique=False) #跳转协议
    welfareUrl = db.Column(db.String(2000), unique=False)#打开连接

    def welfareDict(self):
        dict ={}
        dict['welfareId'] = self.welfareId
        dict['name'] = self.name
        dict['image'] = self.image
        dict['status'] = self.status
        dict['endTime'] = self.endTime.strftime('%Y-%m-%d')
        dict['onTime']  = self.onTime.strftime('%Y-%m-%d')
        dict['activeUrl']  = self.activeUrl
        dict['welfareUrl'] = self.welfareUrl
        dict['type']  =self.type
        return dict
