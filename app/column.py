#coding=utf8
from app import create_app
import os
from app import db


class column(db.Model):
    __tablename__ = 'column'
    columnId = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=False)
    status = db.Column(db.SmallInteger, unique=False)  # 0:下线 1:上线
    plat = db.Column(db.SmallInteger, unique=False) #1:ios 2:andriod 0:all
    app =  db.Column(db.String(16), unique=False)  #app
    type = db.Column(db.SmallInteger, unique=False) #3:阿里百川直接跳转url 2:通过专场Id打开专场 1.分类 4.url打开单个专场  6.拼多多
    itemId= db.Column(db.String(16), unique=True)
    url =  db.Column(db.String(160), unique=False)
    image= db.Column(db.String(160), unique=False) #图片规格 180X180
    index = db.Column(db.Integer, unique=False)



    def columndict(self):
        dict = {}
        dict['type'] = self.type
        dict['name'] = self.name
        dict['url'] = self.url
        dict['image'] = self.image
        dict['itemId'] = self.itemId
        return dict
