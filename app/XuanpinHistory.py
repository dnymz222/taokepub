#coding=utf8
from app import create_app
import os
from app import db
import base64



class XuanpinHistory(db.Model):
    __tablename__ = 'xuanpinhistory'
    log_id = db.Column(db.String(64), primary_key=True)
    item_id = db.Column(db.String(32), unique=False)
    reserve_price = db.Column(db.String(32), unique=False)   #原价
    zk_final_price = db.Column(db.String(32), unique=False)  # 折扣价
    coupon_amount = db.Column(db.Integer, unique=False)
    kuadian_rate = db.Column(db.Float, unique=False)
    kuadian_info = db.Column(db.String(32), unique=False)
    final_price = db.Column(db.Float, unique=False)  #到手价
    update_day = db.Column(db.String(32), unique=False)  # 价格更新日期
    time = db.Column(db.Integer,unique=False)  #时间
    price_score = db.Column(db.Float, unique=False) #评分


    def __init__(self,xuanpincoupon,time):
        self.item_id = xuanpincoupon.item_id
        self.update_day= xuanpincoupon.update_day
        self.kuadian_info = xuanpincoupon.kuadian_promotion_info
        self.kuadian_rate =xuanpincoupon.kudian_rate
        self.reserve_price = xuanpincoupon.reserve_price
        self.zk_final_price  = xuanpincoupon.zk_final_price
        self.coupon_amount = xuanpincoupon.coupon_amount
        self.final_price = xuanpincoupon.final_price
        self.price_score =xuanpincoupon.price_score
        self.log_id = self.item_id +"_"+self.update_day
        self.time = time

    def XuanpinHistoryDict(self):
        dict = {}
        dict["item_id"] = self.item_id
        dict["reserve_price"] = self.reserve_price
        dict["zk_final_price"] = self.zk_final_price
        dict["coupon_amount"] = self.coupon_amount
        dict["kuadian_rate"] = self.kuadian_rate
        dict["kuadian_info"] = self.kuadian_info
        dict["final_price"] = self.final_price
        dict["update_day"] = self.update_day
        dict["time"] = self.time
        dict["price_score"]  = self.price_score
        return dict