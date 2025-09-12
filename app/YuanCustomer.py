#coding=utf8
from app import create_app
import os
from app import db
import base64


class  YuanCustomer(db.Model):
    __tablename__ = 'YuanCustomer'

    index = db.Column(db.String(100), primary_key=True)
    date = db.Column(db.String(64), unique=False)
    wechat_number = db.Column(db.String(64), unique=False)
    wechat_name = db.Column(db.String(64), unique=False)
    wangwang_num= db.Column(db.String(64),unique=False)
    company_name = db.Column(db.String(100),unique=False)
    shop_name = db.Column(db.String(64),unique=False)
    wechat_special = db.Column(db.String(32),unique=False)
    detect_company = db.Column(db.String(64), unique=False)
    note= db.Column(db.String(640), unique=False)
    from_excel = db.Column(db.SmallInteger,unique=False)  #1,0


    def __init__(self,dict):
        self.index = dict["index"]
        self.date = dict["date"]
        self.wechat_name  =  dict["wechat_name"]
        self.wechat_number = dict["wechat_number"]
        self.wechat_special =  dict["wechat_special"]
        self.wangwang_num = dict['wangwang_num']
        self.company_name = dict["company_name"]
        self.shop_name = dict["shop_name"]
        self.detect_company = dict["detect_company"]
        self.note =  dict["note"]
        self.from_excel = dict["from_excel"]


    def YuanCustomerDict(self):
        dict = {}
        dict["index"] = self.index
        dict['date'] = self.date
        dict["wechat_name"] = self.wechat_name
        dict["wechat_number"] = self.wechat_number
        dict["wechat_special"] = self.wechat_special
        dict["wangwang_num"] = self.wangwang_num
        dict["company_name"] = self.company_name
        dict["shop_name"] = self.shop_name
        dict["detect_company"] = self.detect_company
        dict["note"] = self.note
        dict["from_excel"] = self.from_excel
        return dict
