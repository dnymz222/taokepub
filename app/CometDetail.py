from app import create_app
import os
from app import db
import sys
import logging

class CometDetail(db.Model):
    __tablename__ = 'CometDetail'
    number = db.Column(db.String(32), primary_key=True)
    EnglishLink = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)

    EnglishHTML = db.Column(db.LargeBinary, unique=False)
    ChineseHTML = db.Column(db.LargeBinary, unique=False)
    JapaneseHTML = db.Column(db.LargeBinary, unique=False)


    def __init__(self,number):
        self.number = number