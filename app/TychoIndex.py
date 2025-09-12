from app import create_app
import os
from app import db
import sys
import logging

class TychoIndex(db.Model):
    __tablename__ = 'TychoIndex'
    rec_t2 = db.Column(db.String(16),primary_key=True)
    rec_s2 = db.Column(db.String(16),unique=False)
    RAmin = db.Column(db.String(16),unique=False)
    RAmax = db.Column(db.String(16),unique=False)
    DEmin = db.Column(db.String(16),unique=False)
    DEmax = db.Column(db.String(16),unique=False)

    def __init__(self,Line):
        self.rec_t2 =Line[0:7]
        self.rec_s2 = Line[8:14]
        self.RAmin = Line[15:21]
        self.RAmax = Line[22:28]
        self.DEmin = Line[29:35]
        self.DEmax = Line[36:42]

    def tychoindexDict(self):
        dict = {}
        dict["rec_t2"] = self.rec_t2
        dict["rec_s2"] = self.rec_s2
        dict["RAmin"]  = self.RAmin
        dict["RAmax"] = self.RAmax
        dict["DEmin"] = self.DEmin
        dict["DEmax"] = self.DEmax

        return dict










