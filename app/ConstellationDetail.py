from app import create_app
import os
from app import db
import sys
import logging

class ConstellationDetail(db.Model):
    __tablename__ = 'ConstellationDetail'
    shortname = db.Column(db.String(16), primary_key=True)
    EnglishLink = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)

    EnglishHTML = db.Column(db.LargeBinary, unique=False)
    ChineseHTML = db.Column(db.LargeBinary, unique=False)
    JapaneseHTML = db.Column(db.LargeBinary, unique=False)




    def __init__(self, name):
        self.shortname = name