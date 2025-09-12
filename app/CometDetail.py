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


    def stardict(self):
        dict = {}
        dict["number"] = self.number
        dict["EnglishLink"] = self.EnglishLink
        dict["ChineseLink"] = self.ChineseLink
        dict["JapaneseLink"] = self.JapaneseLink
        if self.EnglishHTML is not None:
            dict["EnglishHTML"] = self.EnglishHTML.decode()
        if self.ChineseHTML is not None:
            dict["ChineseHTML"] = self.ChineseHTML.decode()
        if self.JapaneseHTML is not None:
            dict["JapaneseHTML"] = self.JapaneseHTML.decode()

        return dict
