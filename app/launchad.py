#coding=utf8
from app import create_app
import os
from app import db
from app.utils.constvalue import couponUrl
import sys
import logging


class launchad(db.Model):
    __tablename__ = 'launchad'
    launchadId = db.Column(db.String(32), primary_key=True)

    name = db.Column(db.String(200), unique=False)
    image = db.Column(db.String(320), unique=False)
    status = db.Column(db.SmallInteger, unique=False)  # 0:失效 1：有效
    type = db.Column(db.SmallInteger, unique=False)  # 0:没有安装app进行推广  1：有安装app打开链接
    endTime = db.Column(db.Date, unique=False, index=True)
    onTime = db.Column(db.Date, unique=False, index=True)
    os =  db.Column(db.String(16), unique=False) #操作系统
    activeUrl = db.Column(db.String(320), unique=False) #跳转协议
    launchUrl = db.Column(db.String(2000), unique=False)#打开连接
    appId = db.Column(db.String(64), unique=False) #appid
    interval = db.Column(db.Integer, unique=False) #时间间隔 秒
    tbopen = db.Column(db.Boolean,unique=False) #是否要打开淘宝,tmall,pingduoduo

    def launchadDict(self):
        dict ={}
        dict['launchadId'] = self.launchadId
        dict['name'] = self.name
        dict['image'] = self.image
        dict['status'] = self.status
        dict['endTime'] = self.endTime.strftime('%Y-%m-%d')
        dict['onTime']  = self.onTime.strftime('%Y-%m-%d')
        dict['activeUrl']  = self.activeUrl
        dict['launchUrl'] = self.launchUrl
        dict['type']  =self.type
        dict['os'] = self.os
        dict['interval'] = self.interval
        dict['appId'] = self.appId
        dict['tbopen']  = self.tbopen

        return dict

