from app import create_app
import os
from app import db
import sys
import logging

class Tycho(db.Model):
    __tablename__ = 'Tycho'
    TYC = db.Column(db.String(32),primary_key=True)
    Catalog = db.Column(db.String(16),unique=False)
    Proxy = db.Column(db.String(16),unique=False)
    RAhms = db.Column(db.String(16),unique=False)
    DEdms = db.Column(db.String(16),unique=False)
    RA199125 = db.Column(db.Float, unique=False)
    DE199125 = db.Column(db.Float, unique=False)
    Vmag = db.Column(db.String(16),unique=False)
    r_Vmag = db.Column(db.String(16),unique=False)
    RAdeg  = db.Column(db.String(16),unique=False)
    DEdeg = db.Column(db.String(16),unique=False)
    AstroRef =  db.Column(db.String(16),unique=False)
    Plx = db.Column(db.String(16),unique=False)
    pmRA  = db.Column(db.String(16),unique=False)
    pmDE  = db.Column(db.String(16),unique=False)
    e_RAdeg = db.Column(db.String(16),unique=False)
    e_DEdeg  = db.Column(db.String(16),unique=False)
    e_Plx  = db.Column(db.String(16),unique=False)
    e_pmRA = db.Column(db.String(16),unique=False)
    e_pmDE = db.Column(db.String(16),unique=False)
    DE_RA = db.Column(db.String(16),unique=False)
    Plx_RA  = db.Column(db.String(16),unique=False)
    Plx_DE = db.Column(db.String(16),unique=False)
    pmRA_RA = db.Column(db.String(16),unique=False)
    pmRA_DE = db.Column(db.String(16),unique=False)
    pmRA_Plx = db.Column(db.String(16),unique=False)
    pmDE_RA = db.Column(db.String(16),unique=False)
    pmDE_DE = db.Column(db.String(16),unique=False)
    pmDE_Plx = db.Column(db.String(16),unique=False)
    pmDE_pmRA  =  db.Column(db.String(16),unique=False)
    Nastro = db.Column(db.String(16),unique=False)
    F2 = db.Column(db.String(16),unique=False)
    HIP = db.Column(db.String(16),unique=False)
    BTmag = db.Column(db.String(16),unique=False)
    e_BTmag = db.Column(db.String(16),unique=False)
    VTmag = db.Column(db.String(16),unique=False)
    e_VTmag = db.Column(db.String(16),unique=False)
    r_BTmag = db.Column(db.String(16),unique=False)
    B_V = db.Column(db.String(16),unique=False)
    e_B_V  = db.Column(db.String(16),unique=False)
    Q = db.Column(db.String(16),unique=False)
    Fs = db.Column(db.String(16),unique=False)
    Source = db.Column(db.String(16),unique=False)
    Nphoto = db.Column(db.String(16),unique=False)
    VTscat = db.Column(db.String(16),unique=False)
    VTmax = db.Column(db.String(16),unique=False)
    VTmin  = db.Column(db.String(16),unique=False)
    Var = db.Column(db.String(16),unique=False)
    VarFlag = db.Column(db.String(16),unique=False)
    MultFlag = db.Column(db.String(16),unique=False)
    morePhoto = db.Column(db.String(16),unique=False)
    m_HIP = db.Column(db.String(16),unique=False)
    PPM = db.Column(db.String(16),unique=False)
    HD  = db.Column(db.String(16),unique=False)
    BD = db.Column(db.String(16),unique=False)
    CoD = db.Column(db.String(16),unique=False)
    CPD = db.Column(db.String(16),unique=False)
    Remark = db.Column(db.String(16),unique=False)


    def __init__(self,Line):
        self.Catalog = Line[0:1]
        self.TYC = Line[2:14]
        self.Proxy = Line[15:16]
        self.RAhms  = Line[17:28]
        self.DEdms = Line[29:40]
        try:
            rlist = self.RAhms.split(" ")
            self.RA199125 = float(rlist[0]) + float(rlist[1]) / 60.0 + float(rlist[2]) / 3600
        except:
            self.RA199125 = 0

        try:
            dlist = self.DEdms.split(" ")
            a = dlist[0]
            symbol = a[:1]
            degree = a[1:]
            value = float(degree) + float(dlist[1]) / 60.0 + float(dlist[2]) / 3600.0
            if symbol == "-":
                self.DE199125 = value * -1
            else:
                self.DE199125 = value

        except:
            self.DE199125 = 0

        self.Vmag = Line[41:46]
        self.r_Vmag = Line[49:50]
        self.RAdeg = Line[51:63]
        self.DEdeg = Line[64:76]
        self.AstroRef = Line[77:78]
        self.Plx = Line[79:86]
        self.pmRA = Line[87:95]
        self.pmDE = Line[96:104]
        self.e_RAdeg  = Line[105:111]
        self.e_DEdeg = Line[112:118]
        self.e_Plx = Line[119:125]
        self.pmRA = Line[126:132]
        self.pmDE = Line[133:139]
        self.DE_RA = Line[140:145]
        self.Plx_RA = Line[146:151]
        self.Plx_DE =Line [152:157]
        self.pmRA_RA = Line[158:163]
        self.pmRA_DE = Line[164:169]
        self.pmRA_Plx = Line[170:175]
        self.pmDE_RA = Line[176:181]
        self.pmDE_DE = Line[182:187]
        self.pmDE_Plx = Line[188:193]
        self.pmDE_pmRA = Line[194:199]
        self.Nastro = Line[200:203]
        self.F2 = Line[204:209]
        self.HIP = Line[210:216]
        self.BTmag = Line[217:223]
        self.e_BTmag = Line[224:229]
        self.VTmag = Line[230:236]
        self.e_VTmag = Line[237:242]
        self.r_BTmag = Line[243:244]
        self.B_V = Line[245:251]
        self.e_B_V = Line[252:257]
        self.Q = Line[250:261]
        self.Fs =Line[262:266]
        self.Source = Line[267:268]
        self.Nphoto = Line[269:272]
        self.VTscat = Line[273:278]
        self.VTmax = Line[279:284]
        self.VTmin = Line[285:290]
        self.Var = Line[291:292]
        self.VarFlag = Line[293:294]
        self.MultFlag = Line[295:296]
        self.morePhoto = Line[297:298]
        self.m_HIP = Line[299:301]
        self.PPM = Line[302:308]
        self.HD = Line[309:315]
        self.BD = Line[316:326]
        self.CoD = Line[327:337]
        self.CPD = Line[338:348]
        self.Remark = Line[349:350]


    def tychodict(self):
        dict = {}
        dict["TYC"] = self.TYC
        dict["Proxy"]  = self.Proxy
        dict["RAhms"]   = self.RAhms
        dict["DEdms"]  =self.DEdms
        dict["RA199125"] = self.RA199125
        dict["DE199125"] = self.DE199125
        dict["Vmag"] = self.Vmag
        dict["r_Vmag"]  =self.r_Vmag
        dict["RAdeg"] = self.RAdeg
        dict["AstroRef"] = self.AstroRef
        dict["Plx"] = self.Plx
        dict["pmRA"]  = self.pmRA
        dict["e_RAdeg"]  = self.e_RAdeg
        dict["e_DEdeg"]  =self.e_DEdeg
        dict["e_Plx"]  =self.e_Plx
        dict["pmRA"]  = self.pmRA
        dict["pmDE"]  =self.pmDE
        dict["DE_RA"]  =self.DE_RA
        dict["Plx_RA"] = self.Plx_RA
        dict["Plx_DE"]  = self.Plx_DE
        dict["pmRA_RA"]  =self.pmRA_RA
        dict["pmDE_DE"]  =self.pmDE_DE
        dict["pmDE_Plx"]  =self.pmDE_Plx
        dict["pmDE_pmRA"]  =self.pmDE_pmRA
        dict["Nastro"]  =self.Nastro
        dict["F2"] = self.F2
        dict["HIP"]  =self.HIP
        dict["BTmag"]  =self.BTmag
        dict["e_BTmag"]  =self.e_BTmag
        dict["VTmag"]  =self.VTmag
        dict["e_VTmag"]  = self.e_VTmag
        dict["r_BTmag"]  =self.r_BTmag
        dict["B_V"] = self.B_V
        dict["e_B_V"]  =self.e_B_V
        dict["Q"] = self.Q
        dict["Fs"]  =self.Fs
        dict["Source"] = self.Source
        dict["Nphoto"] = self.Nphoto
        dict["VTscat"] = self.VTscat
        dict["VTmax"]  =self.VTmax
        dict["VTmin"] = self.VTmin
        dict["Var"] = self.Var
        dict["VarFlag"] = self.VarFlag
        dict["MultFlag"] = self.MultFlag
        dict["morePhoto"] = self.morePhoto
        dict["m_HIP"]  =self.m_HIP
        dict["PPM"] = self.PPM
        dict["HD"] = self.HD
        dict["BD"]  =self.BD
        dict["CoD"]  =self.CoD
        dict["CPD"]  =self.CPD
        dict["Remark"]  =self.Remark
        return dict




























