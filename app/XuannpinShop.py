#coding=utf8
from app import create_app
import os
from app import db
import base64


class XuanpinShop(db.Model):
    __tablename__ = 'xuanpinshop'
    seller_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(60), unique=False)
    pinpai = db.Column(db.String(64), unique=False)
    picture =  db.Column(db.String(320), unique=False)  #品牌logo
    url = db.Column(db.String(640), unique=False)  #旗舰店url
    isTmall = db.Column(db.Boolean, unique=False)
    category = db.Column(db.String(32), unique=False) #主要级分类：钓竿
    category_id = db.Column(db.String(32), unique=False) #一级分类ID
    index  = db.Column(db.Integer, unique=False) #排序
    keyword = db.Column(db.String(64), unique=False)
    province = db.Column(db.String(32), unique=False)
    city = db.Column(db.String(32), unique=False)
    page = db.Column(db.Integer, unique=False)



    def __init__(self,dict):
        self.seller_id = dict["seller_id"]
        self.name = dict["name"]
        self.pinpai = dict["pinpai"]
        self.picture = dict["picture"]
        self.url = dict["url"]
        self.category= dict["category"]
        self.category_id = dict["category_id"]
        self.isTmall = True
        self.index = dict["index"]
        self.province = dict["province"]
        self.city = dict["city"]
        self.keyword = dict["keyword"]
        self.page = dict["page"]


    def xuanpinshopdict(self):
        dict = {}
        dict["seller_id"] = self.seller_id
        dict["name"] = self.name
        dict["pinpai"] = self.pinpai
        dict["picture"] = self.picture
        dict["url"] = self.url
        dict["province"] = self.province
        dict["city"] = self.city
        dict["keyword"] = self.keyword
        dict["category"] = self .category

        return dict

