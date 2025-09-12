#coding=utf8
from app import create_app
import os
from app import db

class sharecoupon(db.Model):
    __tablename__ = 'sharecoupon'

    scene = db.Column(db.String(64), primary_key=True)
    pid =  db.Column(db.String(32), primary_key=False)
    taobaoId = db.Column(db.String(32), primary_key=False)
    goodsName = db.Column(db.String(200), unique=False)
    image = db.Column(db.String(160), unique=False)
    price = db.Column(db.String(32), unique=False)
    finalPrice = db.Column(db.String(32), unique=False)
    couponDenomination = db.Column(db.Integer, unique=False)
    shareTime = db.Column(db.Integer, unique=False)
    couponPromotUrl = db.Column(db.String(320), unique=False)


    def __init__(self,dict):
        self.scene = dict['scene']
        self.pid = dict['pid']
        self.taobaoId = dict['taobaoId']
        self.goodsName = dict['goodsName']
        self.image = dict['image']
        self.price = dict['price']
        self.finalPrice = dict['finalPrice']
        self.couponDenomination = dict['couponDenomination']
        self.couponPromotUrl = dict['couponPromotUrl']
        self.shareTime = dict['shareTime']



    def sharedict(self):
        dict = {}
        dict['pid'] = self.pid
        dict['taobaoId'] = self.taobaoId
        dict['goodsName'] = self.goodsName
        dict['image'] = self.image
        dict['price'] = self.price
        dict['finalPrice'] = self.finalPrice
        dict['couponDenomination '] = self.couponDenomination
        dict['couponPromotUrl'] = self.couponPromotUrl
        dict['shareTime'] = self.shareTime

        return dict







