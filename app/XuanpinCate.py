#coding=utf8
from app import create_app
import os
from app import db
import base64


class XuanpinCate(db.Model):
    __tablename__ = 'xuanpincate'
    cate_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(32), unique=False) #搜索URL
    picture =  db.Column(db.String(320), unique=False)  #品牌logo
    url = db.Column(db.String(320), unique=False)  #
    type = db.Column(db.SmallInteger, unique=False) #分类级别

    parent_id = db.Column(db.String(32), unique=False) #一级分类：钓竿category
    search_id = db.Column(db.String(320), unique=False) #搜索ID
    index  = db.Column(db.SmallInteger, unique=False) #排序



    def __init__(self,cate_id,name,type,search_id,parent_id,index):
        self.cate_id = cate_id
        self.name = name
        self.picture = ""
        self.url = ""
        self.type = type
        self.parent_id = parent_id
        self.index = index
        self.search_id = search_id


    def XuanpincateDict(self):
        dict ={}
        dict["cateId"] = self.cate_id
        dict["name"] = self.name
        dict["searchId"] = self.search_id
        dict["parentId"] = self.parent_id
        dict["url"] = "/xunquan/search/cat/"
        dict["type"] = self.type
        return dict




