#coding=utf8
from app import create_app
import os
from app import db
import datetime

class qianggou(db.Model):
    num_iid = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(200), unique=False)
    click_url = db.Column(db.String(320), unique=False)
    pic_url = db.Column(db.String(160), unique=False)
    category_name = db.Column(db.String(100), unique=False)
    cateId = db.Column(db.String(32), unique=False)
    reserve_price = db.Column(db.String(32), unique=False)
    sold_num = db.Column(db.Integer, unique=False)
    zk_final_price = db.Column(db.String(60), unique=False)
    total_amount = db.Column(db.Integer, unique=False)
    left_amount = db.Column(db.Integer, unique=False)
    start_time = db.Column(db.DateTime, unique=False, index=True)
    end_time = db.Column(db.DateTime, unique=False, index=True)
    hasCoupon = db.Column(db.SmallInteger, unique=False)
    hasCheck = db.Column(db.SmallInteger, unique=False)
    couponPromotUrl = db.Column(db.String(320), unique=False)
    couponDenomination = db.Column(db.Integer, unique=False)

    def __init__(self,dict):
        self.num_iid = dict['num_iid']
        self.title = dict['title']
        self.click_url = dict['click_url']
        self.pic_url = dict['pic_url']
        self.category_name = dict['category_name']
        self.cateId =''
        self.reserve_price = dict['reserve_price']
        self.sold_num = dict['sold_num']
        self.zk_final_price = dict['zk_final_price']
        self.total_amount =dict['total_amount']
        self.left_amount = self.total_amount - self.sold_num
        self.start_time = dict['start_time']
        self.end_time =dict['end_time']
        self.hasCoupon = 0
        self.hasCheck = 0
        self.couponDenomination = 0
        self.couponPromotUrl =''

    def qianggoudict(self,cateId):
        dict = {}
        dict['cateId'] = cateId
        dict['num_iid'] =self.num_iid
        dict['title'] = self.title
        dict['click_url'] = self.click_url
        dict['pic_url'] = self.pic_url+'_250x250'
        dict['category_name'] = self.category_name
        dict['reserve_price']= self.reserve_price
        dict['sold_num'] = self.sold_num
        if self.hasCoupon:
            dict['zk_final_price'] =  str(float(self.zk_final_price) - self.couponDenomination)
        else:
            dict['zk_final_price'] = self.zk_final_price
        dict['total_amount'] = self.total_amount
        dict['left_amount'] = self.total_amount - self.sold_num
        dict['start_time'] = self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        dict['end_time'] = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        dict['hasCoupon'] = self.hasCoupon
        if self.hasCoupon == 1:

            coupondict = {}
            coupondict['couponPromotUrl'] = self.couponPromotUrl
            coupondict['couponDenomination'] = self.couponDenomination
            dict['coupon'] = coupondict


        return dict

    def qianggouolddict(self,cateId):
        dict = {}
        dict['cateId'] = cateId
        dict['num_iid'] =self.num_iid
        dict['title'] = self.title
        dict['pic_url'] = self.pic_url+'_250x250'
        if self.hasCoupon:
             dict['click_url'] = self.couponPromotUrl
             dict['zk_final_price'] = str(float(self.zk_final_price) - self.couponDenomination)
             dict['end_time'] = self.end_time.strftime('%m-%d %H:%M') + ' 【'+str(self.couponDenomination)+'元券】'
             dict['start_time'] = self.end_time.strftime('%m-%d %H:%M') + ' 【'+str(self.couponDenomination)+'元券】'
        else:
            dict['click_url'] = self.click_url
            dict['zk_final_price'] = self.zk_final_price
            dict['end_time'] = self.end_time.strftime('%m-%d %H:%M') 
            dict['start_time'] = self.end_time.strftime('%m-%d %H:%M') 
            
        dict['category_name'] = self.category_name
        dict['reserve_price']= self.reserve_price
        dict['sold_num'] = self.sold_num
        dict['total_amount'] = self.total_amount
        dict['left_amount'] = self.total_amount - self.sold_num
        
        dict['hasCoupon'] = self.hasCoupon
       

        return dict


