from app import create_app
import os
from app import db
import sys
import logging

class GCVSStar(db.Model):
    __tablename__ = 'GCVSStar'
    GCVS  = db.Column(db.String(16),primary_key=True)
    Constell = db.Column(db.String(16),unique=False)
    Number  = db.Column(db.String(16),unique=False)
    Component = db.Column(db.String(16),unique=False)
    NoteFlag = db.Column(db.String(16),unique=False)
    RA1950 = db.Column(db.FLOAT,unique=False)
    RAh = db.Column(db.String(32),unique=False)
    RAm = db.Column(db.String(32),unique=False)
    RAs = db.Column(db.String(32),unique=False)
    DE1950 = db.Column(db.FLOAT,unique=False)
    DE_ = db.Column(db.String(32),unique=False)
    DEd = db.Column(db.String(32),unique=False)
    DEm = db.Column(db.String(32),unique=False)
    precRA = db.Column(db.String(16),unique=False)
    precDE = db.Column(db.String(16),unique=False)
    GLON = db.Column(db.String(16),unique=False)
    GLAT = db.Column(db.String(16),unique=False)
    Ref1 = db.Column(db.String(16),unique=False)
    Ref2 = db.Column(db.String(16),unique=False)
    VarType = db.Column(db.String(16),unique=False)
    l_magMax = db.Column(db.String(16),unique=False)
    magMax = db.Column(db.String(16),unique=False)
    u_magMax = db.Column(db.String(16),unique=False)
    l_magMin = db.Column(db.String(16),unique=False)
    magMin = db.Column(db.String(16),unique=False)
    n_magMin = db.Column(db.String(16),unique=False)
    u_magMin = db.Column(db.String(16),unique=False)
    f_magMin = db.Column(db.String(16),unique=False)
    magCode = db.Column(db.String(16),unique=False)
    Epoch = db.Column(db.String(16),unique=False)
    q_Epoch = db.Column(db.String(16),unique=False)
    YearNova = db.Column(db.String(16),unique=False)
    u_YearNova = db.Column(db.String(16),unique=False)
    l_Period = db.Column(db.String(16),unique=False)
    Period = db.Column(db.String(20),unique=False)
    u_Period = db.Column(db.String(16),unique=False)
    n_Period = db.Column(db.String(16),unique=False)
    M_m_D = db.Column(db.String(16),unique=False)
    u_M_m_D = db.Column(db.String(16),unique=False)
    n_M_m_D = db.Column(db.String(16),unique=False)
    SpType = db.Column(db.String(20),unique=False)
    Exists = db.Column(db.String(16),unique=False)


    def __init__(self,Line):
        self.Constell = Line[0:2]
        self.Number = Line[2:6]
        self.Component = Line[6:7]
        self.GCVS = Line[7:15]
        self.NoteFlag = Line[15:16]
        self.RAh = Line[16:18]
        self.RAm = Line[18:20]
        self.RAs = Line[20:22]
        try:
            self.RA1950 = float(self.RAh) + float(self.RAm)/60.0 + float(self.RAs)/3600.0
        except:
            self.RA1950 = 0
        self.DE_ = Line[22:23]
        self.DEd = Line[23:25]
        self.DEm = Line[25:29]
        try:
            degree = float(self.DEd)+float(self.DEm)/600.0
            if self.DE_ == "-":
                self.DE1950 = degree*-1
            else:
                self.DE1950  = degree
        except:
            self.DE1950 = 0
        self.precRA =  Line[29:36]
        self.precDE = Line[36:42]
        self.GLON = Line[42:48]
        self.GLAT = Line[48:54]
        self.Ref1 = Line[54:59]
        self.Ref2 = Line[59:64]
        self.VarType = Line[64:73]
        self.l_magMax = Line[73:74]
        self.magMax = Line[74:81]
        self.u_magMax = Line[81:82]
        self.l_magMin = Line[82:83]
        self.magMin = Line[83:89]
        self.n_magMin = Line[89:90]
        self.u_magMin = Line[90:91]
        self.f_magMin = Line[91:92]
        self.magCode = Line[92:93]
        self.Epoch = Line[93:107]
        self.q_Epoch = Line[107:108]
        self.YearNova = Line[108:114]
        self.u_YearNova = Line[114:115]
        self.l_Period = Line[115:116]
        self.Period = Line[116:132]
        self.u_Period = Line[132:133]
        self.n_Period = Line[133:134]
        self.M_m_D = Line[134:138]
        self.u_M_m_D = Line[138:139]
        self.n_M_m_D = Line[139:140]
        self.SpType = Line[140:157]
        self.Exists = Line[157:158]

    def GVVStrarDict(self):
        dict = {}
        dict["Constell"]  =self.Constell
        dict["Number"] = self.Number
        dict["Component"] = self.Component
        dict["GCVS"] = self.GCVS
        dict["NoteFlag"] = self.NoteFlag
        dict["RA1950"]  =self.RA1950
        dict["RAh"] = self.RAh
        dict["RAm"] = self.RAm
        dict["RAs"] = self.RAs
        dict["DE1950"] = self.DE1950
        dict["DE_"] = self.DE_
        dict["DEd"] = self.DEd
        dict["DEm"] = self.DEm

        dict["precRA"] = self.precRA
        dict["precDE"]  =self.precDE
        dict["GLON"] = self.GLON
        dict["GLAT"] = self.GLAT
        dict["Ref1"] = self.Ref1
        dict["Ref2"] = self.Ref2
        dict["VarType"] = self.VarType
        dict["l_magMax"] = self.l_magMax
        dict["magMax"]  =self.magMax

        dict["u_magMax"]  = self.u_magMax

        dict["l_magMin"] = self.l_magMin
        dict["magMin"] = self.magMin
        dict["n_magMin"] = self.n_magMin

        dict["u_magMin"]  = self.u_magMin
        dict["f_magMin"] = self.f_magMin

        dict["magCode"] = self.magCode
        dict["Epoch"]  =self.Epoch
        dict["q_Epoch"] = self.q_Epoch
        dict["YearNova"] = self.YearNova
        dict["u_YearNova"]  =self.u_YearNova
        dict["l_Period"] = self.l_Period
        dict["Period"]  =self.Period
        dict["u_Period"]  =self.u_Period
        dict["n_Period"] = self.n_Period
        dict["M_m_D"]  =self.M_m_D
        dict["u_M_m_D"]  =self.u_M_m_D
        dict["n_M_m_D"] = self.n_M_m_D
        dict["SpType"] = self.SpType
        dict["Exists"] = self.Exists



        return dict















