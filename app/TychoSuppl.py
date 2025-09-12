from app import create_app
import os
from app import db
import sys
import logging

class TychoSuppl(db.Model):
    __tablename__ = 'TychoSuppl'
    TYCId = db.Column(db.String(64), primary_key=True)
    TYC1 = db.Column(db.String(16), unique=False)
    TYC2 = db.Column(db.String(16), unique=False)
    TYC3 = db.Column(db.String(16), unique=False)
    Catalog = db.Column(db.String(16), unique=False)

    flag = db.Column(db.String(16), unique=False)
    RAdeg = db.Column(db.String(16), unique=False)
    DEdeg = db.Column(db.String(16), unique=False)

    pmRA = db.Column(db.String(16), unique=False)
    pmDE = db.Column(db.String(16), unique=False)
    e_RA = db.Column(db.String(16), unique=False)
    e_DE = db.Column(db.String(16), unique=False)
    e_pmRA = db.Column(db.String(16), unique=False)
    e_pmDE = db.Column(db.String(16), unique=False)

    mflag = db.Column(db.String(16), unique=False)


    BT = db.Column(db.String(16), unique=False)
    e_BT = db.Column(db.String(16), unique=False)
    VT = db.Column(db.String(16), unique=False)
    e_VT = db.Column(db.String(16), unique=False)
    prox = db.Column(db.String(16), unique=False)
    TYC = db.Column(db.String(16), unique=False)
    HIP = db.Column(db.String(16), unique=False)
    CCDM = db.Column(db.String(16), unique=False)


    def __init__(self,Line,Catalog):
        self.Catalog  = Catalog
        self.TYC1 = Line[0:4]
        self.TYC2 = Line[5:10]
        self.TYC3 = Line[11:12]
        self.TYCId = self.TYC1 + "-" + self.TYC2 + "-" + self.TYC3
        self.flag = Line[13:14]
        self.RAdeg = Line[15:27]
        self.DEdeg = Line[28:40]
        self.pmRA = Line[41:48]
        self.pmDE = Line[49:56]
        self.e_RA = Line[57:62]
        self.e_DE = Line[63:68]
        self.e_pmRA = Line[69:74]
        self.e_pmDE = Line[75:80]
        self.mflag = Line[81:82]
        self.BT = Line[83:89]
        self.e_BT = Line[90:95]
        self.VT = Line[96:102]
        self.e_VT = Line[103:108]
        self.prox = Line[109:111]
        self.TYC = Line[113:114]
        self.HIP = Line[115:121]
        self.CCDM = Line[121:122]

    def tychosupplDict(self):
        dict ={}
        dict["Catalog"] = self.Catalog
        dict["TYC1"] = self.TYC1
        dict["TYC2"] = self.TYC2
        dict["TYC3"] = self.TYC3
        dict["TYCId"]  =self.TYCId
        dict["flag"]  =self.flag
        dict["RAdeg"] = self.RAdeg
        dict["pmRA"] = self.pmRA
        dict["pmDE"] = self.pmDE
        dict["e_RA"]  = self.e_RA
        dict["e_DE"]  = self.e_DE
        dict["e_pmRA"]  =self.e_pmRA
        dict["e_pmDE"]  =self.e_pmDE
        dict["mflag"]  =self.mflag
        dict["BT"]  =self.BT
        dict["e_BT"] = self.e_BT
        dict["VT"]  =self.VT
        dict["e_VT"]  =self.e_VT
        dict["prox"] = self.prox
        dict["TYC"] = self.TYC
        dict["HIP"] = self.HIP
        dict["CCDM"] = self.CCDM
        return dict




