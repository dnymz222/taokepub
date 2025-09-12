from app import create_app
import os
from app import db
import sys
import logging

class SAOStar(db.Model):
    __tablename__ = 'SAOStar'
    SAO  = db.Column(db.String(16),primary_key=True)
    delFlag = db.Column(db.String(16),unique=False)
    RAh = db.Column(db.String(16), unique=False)
    RAm = db.Column(db.String(16), unique=False)
    RAs = db.Column(db.String(16), unique=False)
    RA1950 = db.Column(db.FLOAT,unique=False)
    pmRA = db.Column(db.String(16),unique=False)
    e_pmRA = db.Column(db.String(16),unique=False)
    RA2mf  = db.Column(db.String(16),unique=False)
    RA2s = db.Column(db.String(16),unique=False)
    e_RA2s = db.Column(db.String(16),unique=False)
    EpRA2 = db.Column(db.String(16),unique=False)
    DE_ = db.Column(db.String(16), unique=False)
    DEd = db.Column(db.String(16), unique=False)
    DEm = db.Column(db.String(16), unique=False)
    DEs = db.Column(db.String(16), unique=False)
    DE1950 = db.Column(db.FLOAT,unique=False)
    pmDE = db.Column(db.String(16),unique=False)
    e_pmDE = db.Column(db.String(16),unique=False)
    DE2mf = db.Column(db.String(16),unique=False)
    DE2s = db.Column(db.String(16),unique=False)
    e_DE2s = db.Column(db.String(16),unique=False)
    EpDE2 = db.Column(db.String(16),unique=False)
    e_Pos = db.Column(db.String(16),unique=False)
    Pmag = db.Column(db.String(16),unique=False)
    Vmag = db.Column(db.String(16),unique=False)
    SpType = db.Column(db.String(16),unique=False)
    r_Vmag = db.Column(db.String(16),unique=False)
    r_Num = db.Column(db.String(16),unique=False)
    r_Pmag = db.Column(db.String(16),unique=False)
    r_pmRA = db.Column(db.String(16),unique=False)
    r_SpType = db.Column(db.String(16),unique=False)
    Rem = db.Column(db.String(16),unique=False)
    a_Vmag = db.Column(db.String(16),unique=False)
    a_Pmag  = db.Column(db.String(16),unique=False)
    r_Cat = db.Column(db.String(16),unique=False)
    CatNum = db.Column(db.String(16),unique=False)
    DM = db.Column(db.String(16),unique=False)
    HD = db.Column(db.String(16),unique=False)
    m_HD = db.Column(db.String(16),unique=False)
    GC = db.Column(db.String(16),unique=False)
    RArad = db.Column(db.String(16),unique=False)
    DErad = db.Column(db.String(16),unique=False)
    RA2000 = db.Column(db.String(32),unique=False)
    pmRA2000 =  db.Column(db.String(16),unique=False)
    DE2000 = db.Column(db.String(32),unique=False)
    pmDE2000 = db.Column(db.String(16),unique=False)
    RA2000rad = db.Column(db.String(16),unique=False)
    DE2000rad = db.Column(db.String(16),unique=False)

    def __init__(self,Line):
        self.SAO = Line[0:6]
        self.delFlag  = Line[6:7]
        self.RAh = Line[7:9]
        self.RAm = Line[9:11]
        self.RAs = Line[11:17]
        try:
            self.RA1950 = float(self.RAh) + float(self.RAm)/60.0 + float(self.RAs)/3600.0
        except:
            self.RA1950 = 0
        self.pmRA = Line[17:24]
        self.e_pmRA = Line[24:26]
        self.RA2mf = Line[26:27]
        self.RA2s = Line[27:33]
        self.e_RA2s = Line[33:35]
        self.EpRA2 = Line[35:41]
        self.DE_ = Line[41:42]
        self.DEd = Line[42:44]
        self.DEm = Line[44:46]
        self.DEs = Line[46:51]
        try:
            DE1950 = float(self.DEd) + float(self.DEm)/60 + float(self.DEs)/3600.0
            if  self.DE_ == "-":
                self.DE1950 = DE1950*-1
            else:
                self.DE1950 = DE1950
        except:
            self.DE1950 = 0
        self.pmDE = Line[51:57]
        self.e_pmDE = Line[57:59]
        self.DE2mf = Line[59:60]
        self.DE2s = Line[60:65]
        self.e_DE2s = Line[65:67]
        self.EpDE2 = Line[67:73]
        self.e_Pos = Line[73:76]
        self.Pmag = Line[76:80]
        self.Vmag = Line[80:84]
        self.SpType = Line[84:87]
        self.r_Vmag = Line[87:89]
        self.r_Num = Line[89:91]
        self.r_Pmag = Line[91:92]
        self.r_pmRA = Line[92:93]
        self.r_SpType = Line[93:94]
        self.Rem = Line[94:95]
        self.a_Vmag = Line[95:96]
        self.a_Pmag = Line[96:97]
        self.r_Cat = Line[97:99]
        self.CatNum = Line[99:104]
        self.DM = Line[104:117]
        self.HD = Line[117:123]
        self.m_HD = Line[123:124]
        self.GC = Line[124:129]
        self.RArad  =Line[129:139]
        self.DErad = Line[139:150]
        self.RA2000 = Line[150:152]+"h"+ Line[152:154]+"m" +Line[154:160] +"s"
        self.pmRA2000 = Line[160:167]
        self.DE2000 = Line[167:168]+Line[168:170]+"d"+Line[170:172]+"m" +Line[172:177]+"s"
        self.pmDE2000 = Line[177:183]
        self.RA2000rad = Line[183:193]
        self.DE2000rad = Line[193:204]

    def SAOStarDict(self):
        dict ={}
        dict["SAO"] = self.SAO
        dict["delFlag"]  = self.delFlag
        dict["RAh"] = self.RAh
        dict["RAm"] = self.RAm
        dict["RAs"] = self.RAs
        dict["RA1950"]  = self.RA1950
        dict["pmRA"]  = self.pmRA
        dict["e_pmRA"] = self.e_pmRA
        dict["RA2mf"] = self.RA2mf
        dict["RA2s"]  =self.RA2s
        dict["e_RA2s"] = self.e_RA2s
        dict["EpRA2"] = self.EpRA2

        dict["DE_"] = self.DE_
        dict["DEd"] = self.DEd
        dict["DEm"] = self.DEm
        dict["DEs"] = self.DEs
        dict["DE1950"]  =self.DE1950
        dict["pmDE"]  =self.pmDE
        dict["e_pmDE"]  =self.e_pmDE
        dict["DE2mf"]  = self.DE2mf
        dict["DE2s"] = self.DE2s
        dict["e_DE2s"]  =self.e_DE2s
        dict["e_Pos"]  =self.e_Pos
        dict["Pmag"]  = self.Pmag
        dict["Vmag"]  = self.Vmag
        dict["SpType"] = self.SpType
        dict["r_Vmag"] =  self.r_Vmag
        dict["r_Num"]  =self.r_Num
        dict["r_Pmag"]  =self.r_Pmag
        dict["r_pmRA"] = self.r_pmRA
        dict["r_SpType"] = self.r_SpType
        dict["Rem"]  = self.Rem
        dict["a_Vmag"]  =self.a_Vmag
        dict["a_Pmag"] = self.a_Pmag
        dict["r_Cat"]  =self.r_Cat
        dict["CatNum"]  =self.CatNum
        dict["DM"] = self.DM
        dict["HD"]  =self.HD
        dict["GC"]  =self.GC
        dict["RArad"] = self.RArad
        dict["DErad"]  =self.DErad
        dict["RA2000"] = self.RA2000
        dict["pmRA2000"]  = self.pmRA2000
        dict["DE2000"] =self.DE2000
        dict["pmDE2000"]  =self.pmDE2000
        dict["RA2000rad"] = self.RA2000rad
        dict["DE2000rad"] = self.DE2000rad


        return dict

















