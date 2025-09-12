#coding=utf8
from app import create_app
import os
from app import db
class water(db.Model):
    __tablename__ = 'water'
    staname = db.Column(db.String(160), primary_key=True)
    propertysta = db.Column(db.String(160), unique=False)
    status = db.Column(db.String(16), unique=False)
    sta_do_l = db.Column(db.String(16), unique=False)
    sta_pp_l = db.Column(db.String(16), unique=False)
    sta_an_l = db.Column(db.String(16), unique=False)
    sta_toc_v = db.Column(db.Float, unique=False)
    sta_ph_l = db.Column(db.String(16), unique=False)
    sta_toc_l = db.Column(db.String(16), unique=False)
    sta_ph_v = db.Column(db.Float, unique=False)
    sta_do_v = db.Column(db.Float, unique=False)
    lat = db.Column(db.Float, unique=False)
    lng = db.Column(db.Float, unique=False)
    sta_time = db.Column(db.String(64), unique=False)
    valley = db.Column(db.String(64), unique=False)
    sta_pp_v= db.Column(db.Float, unique=False)
    sta_an_v = db.Column(db.Float, unique=False)

    # itemId = db.Column(db.String(16), unique=True)
    # plat = db.Column(db.SmallInteger, unique=False) #1:ios 2:andriod 0:all
    # app =  db.Column(db.String(16), unique=False)  #app
    # type = db.Column(db.SmallInteger, unique=False) #3:直接跳转url 2:通过专场Id打开专场 1.分类
    # itemId= db.Column(db.String(16), unique=True)
    # url =  db.Column(db.String(160), unique=False)
    # image= db.Column(db.String(160), unique=False) #图片规格 180X180
    # index = db.Column(db.Float, unique=False)


    def __init__(self,dict):
        self.staname = dict['staname']
        self.propertysta = dict['propertysta']
        self.status = dict['status']
        self.sta_do_l = dict['sta_do_l']
        self.sta_pp_l = dict['sta_pp_l']
        self.sta_an_l  = dict['sta_an_l']
        self.sta_toc_v = dict['sta_toc_v']
        self.sta_ph_l = dict['sta_ph_l']
        self.sta_toc_l = dict['sta_toc_l']
        self.sta_ph_v = dict['sta_ph_v']
        self.sta_do_v  = dict['sta_do_v']
        self.lat = dict['lat']
        self.lng = dict['lng']
        self.sta_time =dict['sta_time']
        self.valley = dict['valley']
        self.sta_pp_v = dict['sta_pp_v']
        self.sta_an_v = dict['sta_an_v']

    def columndict(self):
        dict = {}
        dict['staname'] = self.staname
        dict['propertysta'] = self.propertysta
        dict['status'] = self.status
        dict['sta_do_l'] = self.sta_do_l
        dict['sta_pp_l'] = self.sta_pp_l
        dict['sta_an_l'] = self.sta_an_l
        dict['sta_toc_v'] = self.sta_toc_v
        dict['sta_ph_l'] = self.sta_ph_l
        dict['sta_toc_l'] = self.sta_toc_l
        dict['sta_ph_v'] = self.sta_ph_v
        dict['sta_do_v'] = self.sta_do_v
        dict['lat'] = self.lat
        dict['lng'] = self.lng
        dict['sta_time'] = self.sta_time
        dict['valley'] = self.valley
        dict['sta_pp_v'] = self.sta_pp_v
        dict['sta_an_v'] = self.sta_an_v

        return dict
