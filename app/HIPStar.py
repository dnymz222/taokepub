from app import create_app
import os
from app import db
import sys
import logging

class HIPStar(db.Model):
    __tablename__ = 'HIPStarMain'
    HIP = db.Column(db.String(16), primary_key=True)
    Catalog = db.Column(db.String(16),unique=False)
    Proxy = db.Column(db.String(16),unique=False)
    RAhms = db.Column(db.String(16),unique=False)
    DEdms = db.Column(db.String(16),unique=False)
    RA199125 = db.Column(db.Float,unique=False)
    DE199125 = db.Column(db.Float,unique=False)
    Vmag = db.Column(db.String(16),unique=False)
    VarFlag =db.Column(db.String(16),unique=False)
    r_Vmag = db.Column(db.String(16),unique=False)
    RAdeg = db.Column(db.String(16),unique=False)
    DEdeg = db.Column(db.String(16),unique=False)
    AstroRef = db.Column(db.String(16),unique=False)
    Plx  =db.Column(db.String(16),unique=False)
    pmRA = db.Column(db.String(16),unique=False)
    pmDE = db.Column(db.String(16),unique=False)
    e_RAdeg = db.Column(db.String(16),unique=False)
    e_DEdeg  = db.Column(db.String(16),unique=False)
    e_Plx  = db.Column(db.String(16),unique=False)
    e_pmRA  = db.Column(db.String(16), unique=False)
    e_pmDE = db.Column(db.String(16), unique=False)
    DE_RA  = db.Column(db.String(16), unique=False)
    Plx_RA = db.Column(db.String(16), unique=False)
    Plx_DE = db.Column(db.String(16), unique=False)
    pmRA_RA = db.Column(db.String(16), unique=False)
    pmRA_DE = db.Column(db.String(16), unique=False)
    pmRA_Plx = db.Column(db.String(16), unique=False)
    pmDE_RA  = db.Column(db.String(16), unique=False)
    pmDE_DE = db.Column(db.String(16), unique=False)
    pmDE_Plx = db.Column(db.String(16), unique=False)
    pmDE_pmRA = db.Column(db.String(16), unique=False)
    F1 = db.Column(db.String(16), unique=False)
    F2 = db.Column(db.String(16), unique=False)
    BTmag = db.Column(db.String(16), unique=False)
    e_BTmag = db.Column(db.String(16), unique=False)
    VTmag  = db.Column(db.String(16), unique=False)
    e_VTmag  = db.Column(db.String(16), unique=False)
    m_BTmag = db.Column(db.String(16), unique=False)
    B_V = db.Column(db.String(16), unique=False)
    e_B_V  = db.Column(db.String(16), unique=False)
    r_B_V = db.Column(db.String(16), unique=False)
    V_I = db.Column(db.String(16), unique=False)
    e_V_I = db.Column(db.String(16), unique=False)
    r_V_I = db.Column(db.String(16), unique=False)
    CombMag  = db.Column(db.String(16), unique=False)
    Hpmag = db.Column(db.String(16), unique=False)
    e_Hpmag = db.Column(db.String(16), unique=False)
    Hpscat = db.Column(db.String(16), unique=False)
    o_Hpmag = db.Column(db.String(16), unique=False)
    m_Hpmag = db.Column(db.String(16), unique=False)
    Hpmax = db.Column(db.String(16), unique=False)
    HPmin = db.Column(db.String(16), unique=False)
    Period  = db.Column(db.String(16), unique=False)
    HvarType = db.Column(db.String(16), unique=False)
    moreVar = db.Column(db.String(16), unique=False)
    morePhoto = db.Column(db.String(16), unique=False)
    CCDM = db.Column(db.String(16), unique=False)
    n_CCDM = db.Column(db.String(16), unique=False)
    Nsys = db.Column(db.String(16), unique=False)
    Ncomp = db.Column(db.String(16), unique=False)
    MultFlag = db.Column(db.String(16), unique=False)
    Source  = db.Column(db.String(16), unique=False)
    Qual = db.Column(db.String(16), unique=False)
    m_HIP = db.Column(db.String(16), unique=False)
    theta  = db.Column(db.String(16), unique=False)
    rho = db.Column(db.String(16), unique=False)
    e_rho = db.Column(db.String(16), unique=False)
    dHp = db.Column(db.String(16), unique=False)
    e_dHp = db.Column(db.String(16), unique=False)
    Survey = db.Column(db.String(16), unique=False)
    Chart  = db.Column(db.String(16), unique=False)
    Notes = db.Column(db.String(16), unique=False)
    HD = db.Column(db.String(16), unique=False)
    BD = db.Column(db.String(16), unique=False)
    CoD = db.Column(db.String(16), unique=False)
    CPD = db.Column(db.String(16), unique=False)
    V_I_red = db.Column(db.String(16), unique=False)
    SpType = db.Column(db.String(16), unique=False)
    r_SpType = db.Column(db.String(16), unique=False)

    def __init__(self,Line):
        self.HIP = Line[8:14]
        self.Catalog = Line[0:1]
        self.Proxy = Line[15:16]
        self.RAhms= Line[17:28]
        self.DEdms = Line[29:40]
        try:
            rlist = self.RAhms.split(" ")
            self.RA199125 = float(rlist[0]) + float(rlist[1])/60.0 + float(rlist[2])/3600
        except:
            self.RA199125 = 0


        try:
            dlist = self.DEdms.split(" ")
            a = dlist[0]
            symbol  = a[:1]
            degree= a[1:]
            value = float(degree) + float(dlist[1])/60.0 + float(dlist[2])/3600.0
            if  symbol == "-":
                self.DE199125 = value*-1
            else:
                self.DE199125 = value

        except:
            self.DE199125 = 0

        self.Vmag = Line[41:46]
        self.VarFlag = Line[47:48]
        self.r_Vmag = Line[49:50]
        self.RAdeg = Line[51:63]
        self.DEdeg = Line[64:76]
        self.AstroRef = Line[77:78]
        self.Plx = Line[79:86]
        self.pmRA = Line[87:95]
        self.pmDE = Line[96:104]
        self.e_RAdeg = Line[105:111]
        self.e_DEdeg = Line[112:118]
        self.e_Plx = Line[119:125]
        self.e_pmRA = Line[126:132]
        self.e_pmDE = Line[133:139]
        self.DE_RA = Line[140:145]
        self.Plx_RA = Line[146:151]
        self.Plx_DE  =Line[152:157]
        self.pmRA_RA = Line[158:163]
        self.pmRA_DE= Line[164:169]
        self.pmRA_Plx = Line[170:175]
        self.pmDE_RA = Line[176:181]
        self.pmDE_DE = Line[182:187]
        self.pmDE_Plx = Line[188:193]
        self.pmDE_pmRA = Line[194:199]
        self.F1 = Line[200:203]
        self.F2 = Line[204:209]
        self.BTmag  = Line[217:223]
        self.e_BTmag = Line[224:229]
        self.VTmag = Line[230:236]
        self.e_VTmag = Line[237:242]
        self.m_BTmag = Line[243:244]
        self.B_V  =Line[245:251]
        self.e_B_V = Line[252:257]
        self.r_B_V = Line[258:259]
        self.V_I = Line[260:264]
        self.e_V_I = Line[265:269]
        self.r_V_I = Line[270:271]
        self.CombMag  = Line[274:281]
        self.Hpmag = Line[274:281]
        self.e_Hpmag = Line[282:288]
        self.Hpscat = Line[289:294]
        self.o_Hpmag = Line[295:298]
        self.m_Hpmag = Line[299:300]
        self.Hpmax = Line[301:306]
        self.HPmin = Line[307:312]
        self.Period = Line[313:320]
        self.HvarType = Line[321:322]
        self.moreVar = Line[323:324]
        self.morePhoto = Line[325:326]
        self.CCDM = Line[327:337]
        self.n_CCDM = Line[338:339]
        self.Nsys = Line[340:342]
        self.Ncomp = Line[343:345]
        self.MultFlag = Line[346:347]
        self.Source = Line[348:349]
        self.Qual  = Line[350:351]
        self.m_HIP = Line[352:354]
        self.theta = Line[355:358]
        self.rho = Line[359:366]
        self.e_rho = Line[367:372]
        self.dHp = Line[373:378]
        self.e_dHp = Line[379:383]
        self.Survey = Line[384:385]
        self.Chart  = Line[386:387]
        self.Notes = Line[388:389]
        self.HD = Line[390:396]
        self.BD = Line[397:407]
        self.CoD = Line[408:418]
        self.CPD = Line[419:429]
        self.V_I_red = Line[430:434]
        self.SpType = Line[435:447]
        self.r_SpType = Line[448:449]

    def HIPStarDict(self):
        dict = {}
        dict["HIP"]  = self.HIP
        dict["Catalog"]  =self.Catalog
        dict["Proxy"] = self.Proxy
        dict["RAhms"]  = self.RAhms
        dict["DEdms"] = self.DEdms
        dict["RA199125"]  = self.RA199125
        dict["DE199125"]  = self.DE199125
        dict["Vmag"]  =self.Vmag
        dict["VarFlag"]  =self.VarFlag
        dict["r_Vmag"]  = self.r_Vmag
        dict["RAdeg"]  =self.RAdeg
        dict["DEdeg"]  =self.DEdeg
        dict["AstroRef"]  = self.AstroRef
        dict["Plx"] = self.Plx
        dict["pmRA"] = self.pmRA
        dict["pmDE"] = self.pmDE
        dict["e_RAdeg"] = self.e_RAdeg
        dict["e_DEdeg"]  = self.e_DEdeg
        dict["e_Plx"]  =self.e_Plx
        dict["e_pmRA"]  =self.e_pmRA
        dict["e_pmDE"]  =self.e_pmDE
        dict["DE_RA"] = self.DE_RA
        dict["Plx_RA"]   = self.Plx_RA
        dict["pmDE_pmRA"]  = self.pmDE_pmRA
        dict["F1"]  = self.F1
        dict["F2"]  = self.F2
        dict["BTmag"]  = self.BTmag
        dict["e_BTmag"]  =self.e_BTmag
        dict["B_V"] = self.B_V
        dict["e_B_V"]  = self.e_B_V
        dict["r_B_V"] = self.r_B_V
        dict["V_I"] = self.V_I
        dict["e_V_I"]  = self.e_V_I
        dict["r_V_I"] = self.r_V_I
        dict["CombMag"] = self.CombMag
        dict["Hpmag"]  =self.Hpmag
        dict["e_Hpmag"] = self.e_Hpmag
        dict["Hpscat"]  = self.Hpscat
        dict["o_Hpmag"] = self.o_Hpmag
        dict["m_Hpmag"] = self.m_Hpmag
        dict["Hpmax"] = self.Hpmax
        dict["HPmin"]  = self.HPmin
        dict["Period"] = self.Period
        dict["HvarType"]  = self.HvarType
        dict["moreVar"]  =self.moreVar
        dict["morePhoto"] = self.morePhoto
        dict["CCDM"] = self.CCDM
        dict["n_CCDM"] =  self.n_CCDM
        dict["Nsys"] = self.Nsys
        dict["Ncomp"]  =self.Ncomp
        dict["MultFlag"]  =self.MultFlag
        dict["Source"] = self.Source
        dict["Qual"]  = self.Qual
        dict["m_HIP"]  = self.m_HIP
        dict["theta"]  =self.theta
        dict["rho"] = self.rho
        dict["e_rho"] = self.e_rho
        dict["dHp"] = self.dHp
        dict["Survey"]  =self.Survey
        dict["Chart"] = self.Chart
        dict["Notes"] = self.Notes
        dict["HD"] = self.HD
        dict["BD"] = self.BD
        dict["CoD"] = self.CoD
        dict["CPD"] = self.CPD
        dict["V_I_red"] = self.V_I_red
        dict["SpType"] = self.SpType
        dict["r_SpType"]  = self.r_SpType




        return dict





















































