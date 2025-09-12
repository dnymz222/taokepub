#coding=utf8
from app import create_app
import os
from app import db
from app.utils.constvalue import couponUrl
import sys
import logging


class lunitidalsite(db.Model):
    __tablename__ = 'lunitidalsite'
    siteId = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(100), unique=False)
    url = db.Column(db.String(500), unique=False)
    index= db.Column(db.Integer, unique=False)
    status = db.Column(db.SmallInteger,unique=False)

    def lunitidalsiteDict(self):
        dict = {}
        dict['siteId']  = self.siteId
        dict['name'] = self.name
        dict['url'] = self.url
        return dict
