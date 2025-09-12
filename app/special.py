#coding=utf8
from app import create_app
import os
from app import db

class special(db.Model):
    __tablename__ = 'special'
    taobaoId = db.Column(db.String(32), primary_key=True)
    specialId = db.Column(db.String(16), primary_key=False)
    goodsName = db.Column(db.String(200), unique=False)
    image = db.Column(db.String(320), unique=False)
    price = db.Column(db.String(32), unique=False)
    finalPrice = db.Column(db.String(32), unique=False)
    couponDenomination = db.Column(db.Integer, unique=False)
    shopName = db.Column(db.String(60), unique=False)
    endTime = db.Column(db.Date, unique=False, index=True)
    onTime = db.Column(db.Date, unique=False, index=True)
    couponPromotUrl = db.Column(db.String(320), unique=False)
    sellCount = db.Column(db.Integer, unique=False)


    def specialdict(self):
        dict = {}
        dict['taobaoId'] = self.taobaoId
        dict['specialId'] = self.specialId
        dict['goodsName'] = self.goodsName
        dict['image'] = self.image + '_250x250'
        dict['price'] = self.price
        dict['finalPrice'] = self.finalPrice
        dict['couponDenomination'] = self.couponDenomination
        dict['couponPromotUrl'] = self.couponPromotUrl
        dict['shopName'] = self.shopName
        return dict
