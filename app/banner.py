#coding=utf8
from app import create_app
import os
from app import db

class banner(db.Model):
    __tablename__ = 'banner'
    bannerId = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64), unique=False)
    plat = db.Column(db.SmallInteger, unique=False)  #0.寻券 1.辣妈 2.钓鱼 3.日月
    starTime =db.Column(db.Date, unique=False, index=True)
    endTime = db.Column(db.Date, unique=False, index=True)
    type = db.Column(db.SmallInteger, unique=False) #0:直接跳转url 1:通过专场Id打开专场 2.官方推广(阿里百川打开url)
    specialId= db.Column(db.String(16), unique=True)
    bannerUrl =  db.Column(db.String(64), unique=False)
    imageUrl= db.Column(db.String(160), unique=False) #图片规格 440X180
    index = db.Column(db.Integer, unique=False)
    apps = db.Column(db.String(160), unique=False)


    def promotiondict(self):
        dict = {}
        dict['bannerId'] = self.bannerId
        dict['type'] = self.type
        dict['title'] = self.title
        dict['bannerUrl'] = self.bannerUrl
        dict['imageUrl'] = self.imageUrl
        dict['specialId'] = self.specialId

        return dict


