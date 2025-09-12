from app import create_app
import os
from app import db
import sys
import logging

class HRStar(db.Model):
    __tablename__ = 'HRStar'
    HR = db.Column(db.String(16), primary_key=True)

    Name = db.Column(db.String(16), unique=False)
    DM = db.Column(db.String(16), unique=False)
    HD = db.Column(db.String(16), unique=False)
    SAO = db.Column(db.String(16), unique=False)
    FK5 = db.Column(db.String(16),unique=False)
    IRflag = db.Column(db.String(16),unique=False)
    r_IRflag = db.Column(db.String(16),unique=False)
    Multiple  = db.Column(db.String(16),unique=False)
    ADS = db.Column(db.String(16),unique=False)
    ADScomp =db.Column(db.String(16),unique=False)
    VarID = db.Column(db.String(16),unique=False)
    RAh1900 = db.Column(db.String(16), unique=False)
    RAm1900 = db.Column(db.String(16), unique=False)
    RAs1900 = db.Column(db.String(16), unique=False)
    RA1900 = db.Column(db.FLOAT, unique=False)
    DE_1900 = db.Column(db.String(16), unique=False)
    DEd1900 = db.Column(db.String(16), unique=False)
    DEm1900 = db.Column(db.String(16), unique=False)
    DEs1900 = db.Column(db.String(16), unique=False)
    Dec1900= db.Column(db.FLOAT, unique=False)

    RAh = db.Column(db.String(16), unique=False)
    RAm = db.Column(db.String(16), unique=False)
    RAs = db.Column(db.String(16), unique=False)
    RA2000 = db.Column(db.FLOAT, unique=False)

    DE_ = db.Column(db.String(16), unique=False)
    DEd = db.Column(db.String(16), unique=False)
    DEm = db.Column(db.String(16), unique=False)
    DEs = db.Column(db.String(16), unique=False)
    Dec2000 = db.Column(db.FLOAT, unique=False)


    GLON = db.Column(db.String(16), unique=False)
    GLAT  = db.Column(db.String(16), unique=False)
    Vmag  = db.Column(db.String(16), unique=False)
    n_Vmag = db.Column(db.String(16), unique=False)
    u_Vmag = db.Column(db.String(16), unique=False)
    BV = db.Column(db.String(16), unique=False)
    u_BV = db.Column(db.String(16), unique=False)
    UB = db.Column(db.String(16), unique=False)
    u_UB = db.Column(db.String(16), unique=False)
    RI = db.Column(db.String(16), unique=False)
    n_RI = db.Column(db.String(16), unique=False)

    SpType = db.Column(db.String(16), unique=False)
    n_SpType = db.Column(db.String(16), unique=False)
    pmRA = db.Column(db.String(16), unique=False)
    pmDE = db.Column(db.String(16), unique=False)


    Parallax = db.Column(db.String(16),unique=False)
    n_Parallax = db.Column(db.String(16), unique=False)
    RadVel= db.Column(db.String(16),unique=False)
    n_RadVel = db.Column(db.String(16),unique=False)
    l_RotVel =db.Column(db.String(16),unique=False)
    RotVel = db.Column(db.String(16),unique=False)
    u_RotVel = db.Column(db.String(16),unique=False)
    Dmag = db.Column(db.String(16),unique=False)
    Sep = db.Column(db.String(16),unique=False)
    MultID = db.Column(db.String(16),unique=False)
    MultCnt = db.Column(db.String(16),unique=False)
    NoteFlag = db.Column(db.String(16),unique=False)

    def __init__(self,Line):
        self.HR = Line[0:4]
        self.Name = Line[4:14]
        self.DM = Line[14:25]
        self.HD = Line[25:31]
        self.SAO = Line[31:37]
        self.FK5 = Line[37:41]
        self.IRflag = Line[41:42]
        self.r_IRflag = Line[42:43]
        self.Multiple = Line[43:44]
        self.ADS = Line[44:49]
        self.VarID = Line[49:51]
        self.RAh1900 = Line[60:62]
        self.RAm1900 = Line[62:64]
        self.RAs1900 = Line[64:68]
        try:
            self.RA1900 = float(self.RAh1900) + float(self.RAm1900)/60.0 + float(self.RAs1900)/3600.0
        except:
            self.RAs1900 = 0
        self.DE_1900 = Line[68:69]
        self.DEd1900 = Line[69:71]
        self.DEm1900 = Line[71:73]
        self.DEs1900 = Line[73:75]
        try:
             Dec1900 = float(self.DEd1900) + float(self.DEm1900)/60.0 + float(self.DEs1900)/3600.0
             if self.DE_1900 == "-1":
                 self.Dec1900  = Dec1900 *-1
             else:
                 self.Dec1900 = Dec1900
        except:
            self.Dec1900 = 0
        self.RAh = Line[75:77]
        self.RAm = Line[77:79]
        self.RAs = Line[79:83]
        try:
            self.RA2000 = float(self.RAh) + float(self.RAm)/60.0 + float(self.RAs)/3600.0
        except:
            self.RA2000 = 0
        self.DE_ = Line[83:84]
        self.DEd = Line[84:86]
        self.DEm = Line[86:88]
        self.DEs = Line[88:90]
        try:
             Dec2000 = float(self.DEd) +float(self.DEm)/60.0 + float(self.DEs)/3600.0
             if self.DE_ == "-1":
                 self.Dec2000 = Dec2000 *-1;
             else:
                 self.Dec2000 = Dec2000
        except:
            self.Dec2000 = 0
        self.GLON = Line[90:96]
        self.GLAT = Line[96:102]
        self.Vmag = Line[102:107]
        self.n_Vmag = Line[107:108]
        self.u_Vmag = Line[108:109]
        self.BV = Line[109:114]
        self.u_BV  = Line[114:115]
        self.UB = Line[115:120]
        self.u_UB = Line[120:121]
        self.RI = Line[121:126]
        self.n_RI = Line[126:127]
        self.SpType = Line[127:147]
        self.n_SpType = Line[147:148]
        self.pmRA  = Line[148:154]
        self.pmDE = Line[154:160]
        self.n_Parallax = Line[160:161]
        self.Parallax = Line[161:166]
        self.RadVel = Line[166:170]
        self.n_RadVel = Line[170:174]
        self.l_RotVel = Line[174:176]
        self.RotVel = Line[176:179]
        self.u_RotVel = Line[179:180]
        self.Dmag = Line[180:184]
        self.Sep = Line[184:190]
        self.MultID = Line[190:194]
        self.MultCnt = Line[194:196]
        self.NoteFlag = Line[196:197]

    def HRStarDict(self):
        dict = {}
        dict["HR"]  = self.HR
        dict["DM"]  = self.DM
        dict["Name"]  = self.Name
        dict["HD"] = self.HD
        dict["FK5"]  = self.FK5
        dict["IRflag"] = self.IRflag
        dict["r_IRflag"] = self.r_IRflag
        dict["Multiple"] = self.Multiple
        dict["ADS"] = self.ADS
        dict["VarID"]  =self.VarID

        dict["RAh1900"] = self.RAh1900
        dict["RAm1900"] = self.RAm1900
        dict["RAs1900"] = self.RAs1900
        dict["RA1900"] = self.RA1900
        dict["DEd1900"] = self.DEd1900
        dict["DEm1900"] = self.DEm1900
        dict["DEs1900"] = self.DEs1900
        dict["Dec1900"] = self.Dec1900
        dict["RAh"] = self.RAh
        dict["RAm"] = self.RAm
        dict["RAs"] = self.RAs
        dict["RA2000"]  =self.RA2000
        dict["DE_"] = self.DE_
        dict["DEd"] = self.DEd
        dict["DEm"] = self.DEm
        dict["DEs"] = self.DEs
        dict["Dec2000"] = self.Dec2000
        dict["GLON"]  = self.GLON
        dict["GLAT"] = self.GLAT
        dict["Vmag"] = self.Vmag
        dict["n_Vmag"] = self.n_Vmag
        dict["u_Vmag"] = self.u_Vmag
        dict["BV"] = self.BV
        dict["u_BV"] = self.u_BV
        dict["UB"] = self.UB
        dict["u_UB"] = self.u_UB
        dict["RI"] = self.RI
        dict["n_RI"]  = self.n_RI
        dict["SpType"] = self.SpType
        dict["pmRA"] = self.pmRA
        dict["pmDE"] = self.pmDE
        dict["Parallax"] = self.Parallax
        dict["n_Parallax"] = self.n_Parallax
        dict["RadVel"] = self.RadVel
        dict["n_RadVel"] = self.n_RadVel
        dict["l_RotVel"] = self.l_RotVel
        dict["RotVel"] = self.RotVel
        dict["u_RotVel"]  =self.u_RotVel
        dict["Dmag"]  = self.Dmag
        dict["Sep"] = self.Sep
        dict["MultID"] = self.MultID
        dict["MultCnt"] = self.MultCnt
        dict["NoteFlag"] =  self.NoteFlag

        return dict








