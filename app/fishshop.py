#coding=utf8
from app import create_app
import os
from app import db
from app.utils.constvalue import couponUrl
import sys
import logging


class fishshop(db.Model):
    __tablename__ = 'fishshop'
    fishshopIndex = db.Column(db.String(32), primary_key=True)
    shop_id  =  db.Column(db.String(32), unique=False)
    shop_name  =  db.Column(db.String(64), unique=False)
    shop_des = db.Column(db.String(160), unique=False)
    shop_image = db.Column(db.String(240),unique=False)
    shop_url = db.Column(db.String(2400),unique=False)
    status = db.Column(db.Boolean,unique=False)
    index = db.Column(db.Integer,unique=False)
    source  = db.Column(db.String(120),unique=False)



    def fishshop_dict(self):
        dict={}
        dict['shop_id'] = self.shop_id
        dict['shop_name'] = self.shop_name
        dict['shop_des'] = self.shop_des
        dict['shop_image'] = self.shop_image
        dict['shop_url'] = self.shop_url
        dict['source'] = self.source


        return dict