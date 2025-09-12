#coding=utf8
from app import create_app
import os
from app import db
import base64


class Xuanpin(db.Model):
    __tablename__ = 'xuanpinku'
    favorites_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(32), unique=False)
    picture =  db.Column(db.String(320), unique=False)  #品牌logo
    url = db.Column(db.String(320), unique=False)  #旗舰店url
    type = db.Column(db.SmallInteger, unique=False) #1.精选 2.专区 3.品牌
    app = db.Column(db.SmallInteger, unique=False)   #1.钓鱼 2.摄影
    category = db.Column(db.String(32), unique=False) #一级分类：钓竿
    categoryId = db.Column(db.String(32), unique=False) #一级分类ID
    index  = db.Column(db.SmallInteger, unique=False) #排序
    day =  db.Column(db.String(32), unique=False)
    json = db.Column(db.LargeBinary, unique=False)


    def __init__(self):
        pass


    def xuanpin2dict(self):
        dict = {}
        dict["favorites_id"] = self.favorites_id
        dict["name"] = self.name
        dict["picture"] = self.picture
        dict["url"] = self.url
        dict["category"] = self.category
        dict["categoryId"] = self.categoryId
        return  dict