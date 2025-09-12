from app import create_app
import os
from app import db
import sys
import logging

class NGCCStar(db.Model):
    __tablename__ = 'NGCCStar'
    Name = db.Column(db.String(16), primary_key=True)
    Type  = db.Column(db.String(16), unique=False)
    RAh = db.Column(db.String(16), unique=False)
    RAm = db.Column(db.String(16), unique=False)
    RAB2000 = db.Column(db.FLOAT, unique=False)
    DE_ = db.Column(db.String(16), unique=False)
    DEd = db.Column(db.String(16), unique=False)
    DEm = db.Column(db.String(16), unique=False)
    DEB2000 = db.Column(db.FLOAT, unique=False)
    Source = db.Column(db.String(16), unique=False)
    Const = db.Column(db.String(16), unique=False)
    l_size = db.Column(db.String(16), unique=False)
    size  = db.Column(db.String(16), unique=False)
    mag = db.Column(db.String(16), unique=False)
    n_mag = db.Column(db.String(16), unique=False)
    Desc = db.Column(db.String(64), unique=False)
    Object = db.Column(db.String(64), unique=False)
    Comment = db.Column(db.String(64), unique=False)


    def __init__(self,Line):
        self.Name = Line[0:5]
        self.Type = Line[6:9]
        self.RAh = Line[10:12]
        self.RAm = Line[13:17]
        try:
          self.RAB2000 = float(self.RAh) + float(self.RAm)/60.0
        except:
          self.RAB2000 = 0

        self.DE_ = Line[19:20]
        self.DEd = Line[20:22]
        self.DEm = Line[23:25]
        try:
            DEB2000 = float(self.DEd) + float(self.DEm)/60.0
            if self.DE_ == "-":
                self.DEB2000 = DEB2000*-1
            else:
                self.DEB2000 = DEB2000
        except:
            self.DEB2000 = 0
        self.Source = Line[26:27]
        self.Const = Line[29:32]
        self.l_size = Line[32:33]
        self.size =Line[35:38]
        self.mag = Line[40:44]
        self.n_mag = Line[44:45]
        self.Desc = Line[46:96]
        self.Object = ""
        self.Comment = ""


    def NGCCStarDict(self):
        dict = {}
        dict["Name"] = self.Name
        dict["Type"]  =self.Type
        dict["RAh"] = self.RAh
        dict["RAm"] = self.RAm
        dict["DE_"] = self.DE_
        dict["DEd"] = self.DEd
        dict["DEm"] = self.DEm
        dict["RAB2000"] = self.RAB2000
        dict["DEB2000"] = self.DEB2000
        dict["Source"] = self.Source
        dict["Const"] = self.Const
        dict["l_size"] = self.l_size
        dict["size"] = self.size
        dict["mag"]  = self.mag
        dict["n_mag"] = self.n_mag
        dict["Desc"]  =self.Desc
        dict["Object"] = self.Object
        dict["Comment"] = self.Comment

        return dict