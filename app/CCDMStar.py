from app import create_app
import os
from app import db
import sys
import logging

class CCDMStar(db.Model):
    __tablename__ = 'CCDMStar'
    CCDM = db.Column(db.String(16),primary_key=True)
    rComp = db.Column(db.String(16),unique=False)
    Comp = db.Column(db.String(16),unique=False)
    Note1 = db.Column(db.String(16),unique=False)
    Note2  = db.Column(db.String(16),unique=False)
    Disc = db.Column(db.String(16),unique=False)
    dRAs = db.Column(db.String(16),unique=False)
    dDEs = db.Column(db.String(16),unique=False)
    r_dRAs = db.Column(db.String(16),unique=False)
    Year = db.Column(db.String(16),unique=False)
    theta = db.Column(db.String(16),unique=False)
    rho = db.Column(db.String(16),unique=False)
    Obs = db.Column(db.String(16),unique=False)
    Vmag = db.Column(db.String(16),unique=False)
    Sp  = db.Column(db.String(16),unique=False)
    pmNote = db.Column(db.String(16),unique=False)
    pmRA = db.Column(db.String(16),unique=False)
    pmDE = db.Column(db.String(16),unique=False)
    DM = db.Column(db.String(16),unique=False)
    Name2 = db.Column(db.String(16),unique=False)
    HD  = db.Column(db.String(16),unique=False)
    m_HD = db.Column(db.String(16),unique=False)
    ADS_BDS = db.Column(db.String(16),unique=False)
    m_ADS_BDS = db.Column(db.String(16),unique=False)
    n_IDS = db.Column(db.String(16),unique=False)
    IDS = db.Column(db.String(16),unique=False)
    HIP = db.Column(db.String(16),unique=False)
    RA199125 = db.Column(db.Float, unique=False)
    DE199125 = db.Column(db.Float, unique=False)

    def __init__(self,Line):
        self.CCDM = Line[1:11] + "-"+Line[11:12] + "-"+Line[12:13]
        self.rComp = Line[11:12]
        self.Comp = Line[12:13]
        self.Note1 = Line[13:14]
        self.Note2 = Line[14:15]
        self.Disc = Line[15:22]
        self.dRAs = Line[23:30]
        self.dDEs = Line[30:37]
        self.r_dRAs = Line[38:40]
        self.Year = Line[41:45]
        self.theta = Line[46:49]
        self.rho = Line[49:55]
        self.Obs = Line[56:58]
        self.Vmag = Line[59:63]
        self.Sp = Line[64:66]
        self.pmNote = Line[66:67]
        self.pmRA  = Line[67:72]
        self.pmDE = Line[72:77]
        self.DM = Line[77:87]
        self.Name2 = Line[87:97]
        self.HD = Line[98:104]
        self.m_HD = Line[104:106]
        self.ADS_BDS = Line[106:112]
        self.m_ADS_BDS = Line[112:113]
        self.n_IDS = Line[113:114]
        self.IDS = Line[114:125]
        self.HIP = Line[126:132]

    def ccdmDict(self):
        dict = {}
        dict["CCDM"] = self.CCDM
        dict["rComp"] = self.rComp
        dict["Comp"] = self.Comp
        dict["Note1"]  =self.Note1
        dict["Note2"] = self.Note2
        dict["Disc"] = self.Disc
        dict["dDEs"] = self.dDEs
        dict["r_dRAs"] = self.r_dRAs
        dict["Year"] = self.Year
        dict["theta"] = self.theta
        dict["rho"]  = self.rho
        dict["Obs"] = self.Obs
        dict["Vmag"]  =self.Vmag
        dict["Sp"]  =self.Sp
        dict["pmNote"] = self.pmNote
        dict["pmRA"] = self.pmRA
        dict["pmDE"]  =self.pmDE
        dict["DM"] = self.DM
        dict["Name2"] = self.Name2
        dict["HD"]  =self.HD
        dict["m_HD"] = self.m_HD
        dict["ADS_BDS"] = self.ADS_BDS
        dict["n_IDS"]  =self.n_IDS
        dict["IDS"] = self.IDS
        dict["HIP"] = self.HIP
        dict["RA199125"] = self.RA199125
        dict["DE199125"] = self.DE199125

        return dict



























