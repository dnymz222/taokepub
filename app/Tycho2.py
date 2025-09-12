from app import create_app
import os
from app import db
import sys
import logging

class Tycho2(db.Model):
    __tablename__ = 'Tycho2'
    TYCId = db.Column(db.String(64), primary_key=True)
    TYC1 = db.Column(db.String(16), unique=False)
    TYC2 = db.Column(db.String(16), unique=False)
    TYC3 = db.Column(db.String(16), unique=False)
    recordId = db.Column(db.BigInteger, unique=True)

    pflag = db.Column(db.String(16), unique=False)
    mRAdeg = db.Column(db.String(16), unique=False)
    mDEdeg = db.Column(db.String(16), unique=False)

    pmRA = db.Column(db.String(16), unique=False)
    pmDE = db.Column(db.String(16), unique=False)
    e_mRA = db.Column(db.String(16), unique=False)
    e_mDE = db.Column(db.String(16), unique=False)
    e_pmRA = db.Column(db.String(16), unique=False)
    e_pmDE = db.Column(db.String(16), unique=False)

    mepRA = db.Column(db.String(16), unique=False)
    mepDE = db.Column(db.String(16), unique=False)
    Num = db.Column(db.String(16), unique=False)
    g_mRA = db.Column(db.String(16), unique=False)
    g_mDE = db.Column(db.String(16), unique=False)
    g_pmRA = db.Column(db.String(16), unique=False)
    g_pmDE = db.Column(db.String(16), unique=False)

    BT = db.Column(db.String(16), unique=False)
    e_BT = db.Column(db.String(16), unique=False)
    VT = db.Column(db.String(16), unique=False)
    e_VT = db.Column(db.String(16), unique=False)
    prox = db.Column(db.String(16), unique=False)
    TYC = db.Column(db.String(16), unique=False)
    HIP = db.Column(db.String(16), unique=False)

    CCDM = db.Column(db.String(16), unique=False)
    RAdeg = db.Column(db.String(16), unique=False)
    DEdeg = db.Column(db.String(16), unique=False)
    epRA = db.Column(db.String(16), unique=False)
    epDE = db.Column(db.String(16), unique=False)
    e_RA = db.Column(db.String(16), unique=False)
    e_DE = db.Column(db.String(16), unique=False)
    posflg = db.Column(db.String(16), unique=False)
    corr = db.Column(db.String(16), unique=False)


    def __init__(self,Line,RecordeId):
        self.recordId = RecordeId
        self.TYC1 = Line[0:4]
        self.TYC2 = Line[5:10]
        self.TYC3 = Line[11:12]
        self.TYCId = self.TYC1 + "-" + self.TYC2 +"-" + self.TYC3
        self.pflag = Line[13:14]
        self.mRAdeg = Line[15:27]
        self.mDEdeg = Line[28:40]
        self.pmRA  = Line[41:48]
        self.pmDE = Line[49:56]
        self.e_mRA  =Line[57:60]
        self.e_mDE = Line[61:64]
        self.e_pmRA  =Line[65:69]
        self.e_pmDE  =Line[70:74]
        self.mepRA = Line[75:82]
        self.mepDE = Line[83:90]
        self.Num = Line[91:93]
        self.g_mRA = Line[94:97]
        self.g_mDE = Line[98:101]
        self.g_pmRA = Line[102:105]
        self.g_pmDE = Line[106:109]
        self.BT = Line[110:116]
        self.e_BT = Line[117:122]
        self.VT = Line[123:129]
        self.e_VT = Line[130:135]
        self.prox = Line[136:139]
        self.TYC = Line[140:141]
        self.HIP = Line[142:147]
        self.CCDM = Line[148:151]
        self.RAdeg = Line[152:164]
        self.DEdeg = Line[165:177]
        self.epRA = Line[178:182]
        self.epDE = Line[183:187]
        self.e_RA = Line[188:193]
        self.e_DE = Line[194:199]
        self.posflg = Line[200:201]
        self.corr = Line[202:206]


    def Tycho2Dict(self):
        dict = {}
        dict["TYC1"] = self.TYC1
        dict["TYC2"] = self.TYC2
        dict["TYC3"] = self.TYC3
        dict["TYCId"] = self.TYCId
        dict["pflag"] = self.pflag
        dict["mRAdeg"] = self.mRAdeg
        dict["mDEdeg"] = self.mDEdeg
        dict["pmRA"]  =self.pmRA
        dict["pmDE"] = self.pmDE
        dict["e_mRA"] = self.e_mRA
        dict["mepDE"] = self.mepDE
        dict["Num"] =self.Num
        dict["g_mRA"] = self.g_mRA
        dict["g_pmDE"]  =self.g_pmDE
        dict["BT"] = self.BT
        dict["e_BT"]  =self.e_BT
        dict["VT"] = self.VT
        dict["e_VT"]  =self.e_VT
        dict["prox"] = self.prox
        dict["TYC"] = self.TYC
        dict["HIP"] = self.HIP
        dict["CCDM"] = self.CCDM
        dict["RAdeg"]  =self.RAdeg
        dict["DEdeg"]  =self.DEdeg
        dict["epRA"] = self.epRA
        dict["epDE"] = self.epDE
        dict["e_RA"] = self.e_RA
        dict["e_DE"] = self.e_DE
        dict["posflg"]  =self.posflg
        dict["corr"] = self.corr



        return dict







