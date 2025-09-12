#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime

class chinaLunitidal(db.Model):
    __tablename__ = 'chinaLunitidal'
    imageId = db.Column(db.String(100), primary_key=True)
    url = db.Column(db.String(160), unique=False)  # 站点名称
    index = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(80), unique=False)  # 站点名称


    def chinaLunitidalImagedict(self):
       dict = {}
       dict['imageId'] = self.imageId
       dict['url'] = self.url
       dict['index'] = self.index
       dict['name'] = self.name

       return dict