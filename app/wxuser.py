#coding=utf8
from app import create_app
import os
from app import db

class wxuser(db.Model):
    __tablename__ = 'wxuser'
    userId = db.Column(db.String(60), primary_key=True)
    userName = db.Column(db.String(60), unique=False)
    sex = db.Column(db.Integer, unique=False)
    age = db.Column(db.Integer, unique=False)
    city =  db.Column(db.String(60), unique=False)
    usernumber =  db.Column(db.String(60), unique=False)
    fromPid = db.Column(db.String(60), unique=False)
    fromuserId = db.Column(db.String(60), unique=False)
    channel = db.Column(db.String(60), unique=False)
    promotionar = db.Column(db.Boolean, unique=False)
    promnotionPid = db.Column(db.String(32), unique=False)
    wxversion = db.Column(db.String(32), unique=False)



