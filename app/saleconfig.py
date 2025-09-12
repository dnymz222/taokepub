#coding=utf8
from app import create_app
import os
import sys
from app import db





class saleconfig(db.Model):
    __tablename__ = 'saleconfig'
    config_id= db.Column(db.String(60), primary_key=True)

    title = db.Column(db.String(64), unique=False)
    plat = db.Column(db.SmallInteger, unique=False)
    source =  db.Column(db.String(64), unique=False)

    starTime = db.Column(db.Date, unique=False, index=True)
    endTime = db.Column(db.Date, unique=False, index=True)

    status = db.Column(db.SmallInteger, unique=False)  #0：无,1:有提示，  2:有降价

    price = db.Column(db.String(16), unique=False)

    oldprice = db.Column(db.String(16), unique=False)



    purchase_tip =  db.Column(db.String(64), unique=False)

    shop_tip  = db.Column(db.String(64), unique=False)

    purchase_note = db.Column(db.String(320), unique=False)



    def __init__(self):

        pass

    def saleconfigdict(self):
        dict = {}
        dict["config_id"] = self.config_id
        dict["title"] = self.title
        dict["price"] = self.price
        dict["status"] = self.status
        dict["oldprice"] = self.oldprice
        dict["purchase_tip"] = self.purchase_tip
        dict["shop_tip"] = self.shop_tip
        dict["endTime"] = self.endTime.strftime('%Y-%m-%d')
        dict["starTime"] =  self.starTime.strftime('%Y-%m-%d')
        dict["purchase_note"] = self.purchase_note
        return dict






