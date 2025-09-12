from app import create_app
import os
from app import db
import sys
import logging

class DeepskyDetail(db.Model):
    __tablename__ = 'DeepskyDetail'
    Identifier = db.Column(db.String(32), primary_key=True)
    EnglishLink = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)

    EnglishHTML = db.Column(db.LargeBinary, unique=False)
    ChineseHTML = db.Column(db.LargeBinary, unique=False)
    JapaneseHTML = db.Column(db.LargeBinary, unique=False)


    def __init__(self,Identifier):
        self.Identifier = Identifier

    def stardict(self):
        dict = {}

        dict["Identifier"] = self.Identifier
        dict["EnglishLink"] = self.EnglishLink
        dict["ChineseLink"] = self.ChineseLink
        dict["JapaneseLink"] = self.JapaneseLink

        if self.ChineseHTML is not None:
            dict["ChineseHTML"] = self.ChineseHTML.decode()
        if self.EnglishHTML is not None:
            dict["EnglishHTML"] = self.EnglishHTML.decode()
        if self.JapaneseHTML is not None:
            dict["JapaneseHTML"] = self.JapaneseHTML.decode()

        return dict