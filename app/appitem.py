#coding=utf8
from app import create_app
import os
from app import db


class appitem(db.Model):
    __tablename__ = 'appitem'
    appId = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64), unique=False)
    plat = db.Column(db.SmallInteger, unique=False)  #1.android 2.iOS
    image = db.Column(db.String(160), unique=False)
    description = db.Column(db.String(160), unique=False)
    url = db.Column(db.String(160), unique=False)
    index = db.Column(db.Integer,unique=False)
    packagename = db.Column(db.String(64), unique=False)



    def appitemDict(self):
        dict ={}
        dict['title'] = self.title
        dict['image'] = self.image
        dict['url'] =  self.url
        dict['description'] = self.description
        dict['packagename'] = self.packagename
        return dict




