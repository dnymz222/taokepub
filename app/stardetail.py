from app import create_app
import os
from app import db
import sys
import logging

class stardetail(db.Model):
    __tablename__ = 'stardetail'

    CombinedId = db.Column(db.String(64), primary_key=True)

    EnglishLink = db.Column(db.String(128), unique=False)
    ChineseLink = db.Column(db.String(128), unique=False)
    JapaneseLink = db.Column(db.String(128), unique=False)

    EnglishHTML = db.Column(db.LargeBinary, unique=False)
    ChineseHTML = db.Column(db.LargeBinary, unique=False)
    JapaneseHTML= db.Column(db.LargeBinary, unique=False)

    def __init__(self,Id):
        self.CombinedId = Id

    def stardict(self):
        dict = {}
        dict["CombinedId"] = self.CombinedId
        dict["EnglishLink"] = self.EnglishLink
        dict["ChineseLink"] = self.ChineseLink
        dict["JapaneseLink"] = self.JapaneseLink
        if self.EnglishHTML is not  None:
            dict["EnglishHTML"] = self.EnglishHTML.decode()
        if self.ChineseHTML is not None:
            dict["ChineseHTML"] = self.ChineseHTML.decode()
        if self.JapaneseHTML is not None:
            dict["JapaneseHTML"] = self.JapaneseHTML.decode()

        return dict


