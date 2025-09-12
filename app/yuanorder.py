#coding=utf8
from app import create_app
import os
from app import db
import base64


class yuanorder(db.Model):
    __tablename__ = 'yuanorder'

    nameNum = db.Column(db.String(100), primary_key=True)
    sheet = db.Column(db.String(100), unique=False)
    table = db.Column(db.String(64), unique=False)
    name = db.Column(db.String(64), unique=False)
    num= db.Column(db.String(64),unique=False)
    verycode = db.Column(db.String(32),unique=False)
    date = db.Column(db.String(32),unique=False)
    price = db.Column(db.String(32),unique=False)
    status = db.Column(db.String(100), unique=False)
    chatnum= db.Column(db.String(32), unique=False)
    goodsname= db.Column(db.String(320), unique=False)
    note = db.Column(db.String(320), unique=False)
    onTime = db.Column(db.Date, unique=False, index=True)




    def __init__(self,dict):

        self.nameNum= dict['nameNum']
        self.sheet = dict['sheet']
        self.name  = dict['name']
        self.num = dict['num']
        self.date = dict['date']
        self.price = dict['price']
        self.status = dict['status']
        self.chatnum = dict['chatnum']
        self.goodsname = dict['goodsname']
        self.note = dict['note']
        self.onTime = dict['onTime']
        codestr = base64.encodestring(self.name)
        self.verycode = codestr[0:6]
        self.table = ''


    def yuandict(self):
        dict ={}
        dict['cateId'] = self.cateId
        dict['parentId'] = self.parentId
        dict['name'] = self.name


        return dict

