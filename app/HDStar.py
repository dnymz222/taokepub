from app import create_app
import os
from app import db
import sys
import logging

class HDStar(db.Model):
    __tablename__ = 'HDStar'
    HD = db.Column(db.String(16), primary_key=True)
    DM = db.Column(db.String(16),unique=False)
    RAh = db.Column(db.String(32), unique=False)
    RAdm = db.Column(db.String(32), unique=False)
    RAB1900 = db.Column(db.FLOAT, unique=False)
    DE_ = db.Column(db.String(32), unique=False)
    DEd = db.Column(db.String(32), unique=False)
    DEm = db.Column(db.String(32), unique=False)
    DEB1900 = db.Column(db.FLOAT, unique=False)
    q_Ptm = db.Column(db.String(16),unique=False)
    Ptm = db.Column(db.String(16),unique=False)
    n_Ptm = db.Column(db.String(16),unique=False)
    q_Ptg = db.Column(db.String(16),unique=False)
    Ptg = db.Column(db.String(16),unique=False)
    n_Ptg = db.Column(db.String(16),unique=False)
    SpT = db.Column(db.String(16),unique=False)
    Int = db.Column(db.String(16),unique=False)
    Rem = db.Column(db.String(16),unique=False)


    def __init__(self,Line):
        self.HD = Line[0:6]
        self.DM = Line[6:18]
        self.RAh = Line[18:20]
        self.RAdm  = Line[20:23]
        try:
            self.RAB1900 = float(self.RAh) +float(self.RAdm)/600.0
        except:
            self.RAB1900 = 0
        self.DE_ = Line[23:24]
        self.DEd = Line[24:26]
        self.DEm = Line[26:28]
        try:
            DEDegree = float(self.DEd) + float(self.DEm)/60.0
            if self.DE_ == "-":
                self.DEB1900 = DEDegree *-1
            else:
                self.DEB1900 = DEDegree
        except:
            self.DEB1900 = 0
        self.q_Ptm = Line[28:29]
        self.Ptm = Line[29:34]
        self.n_Ptm = Line[34:35]
        self.q_Ptg = Line[35:36]
        self.Ptg = Line[36:41]
        self.n_Ptg = Line[41:42]
        self.SpT = Line[42:45]
        self.Int = Line[45:47]
        self.Rem = Line[47:48]

    def HDStarDict(self):
        dict ={}
        dict["HD"] = self.HD
        dict["DM"] = self.DM
        dict["RAh"] = self.RAh
        dict["RAdm"] = self.RAdm

        dict["RAB1900"] = self.RAB1900
        dict["DE_"] = self.DE_
        dict["DEd"] = self.DEd
        dict["DEm"] = self.DEm
        dict["DEB1900"] = self.DEB1900
        dict["q_Ptm"] = self.q_Ptm
        dict["Ptm"] = self.Ptm
        dict["n_Ptm"] = self.n_Ptm
        dict["q_Ptg"] = self.q_Ptg
        dict["Ptg"] = self.Ptg
        dict["n_Ptg"] = self.n_Ptg
        dict["SpT"] = self.SpT
        dict["Int"] = self.Int
        dict["Rem"] = self.Rem
        dict["RAh"] = self.RAh
        dict["RAdm"] = self.RAdm
        dict["DE_"] = self.DE_
        dict["DEd"] = self.DEd
        dict["DEm"] = self.DEm
        return dict



