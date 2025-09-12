from app import create_app
import os
from app import db
import sys
import logging

class SMSCode(db.Model):
    __tablename__ = 'SMSCode'
    phone_code  = db.Column(db.String(16),primary_key=True)
    phone = db.Column(db.String(11), unique=False)
    code = db.Column(db.String(4), unique=False)
    app = db.Column(db.String(16), unique=False)
    status = db.Column(db.Integer,unique=False)


    def __init__(self,phone,code,app):
        self.phone_code = phone + "_" + code
        self.phone = phone
        self.code = code
        self.app = app
        self.status = 0

    def codedict(self):
        dict = {}
        dict["phone"] = self.phone
        dict["code"] = self.code
        dict["app"] = self.app
        return  dict