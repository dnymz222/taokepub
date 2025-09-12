from app import  create_app
import os
from app import db
import sys
import json



class SolarEclipse(db.Model):
    __tablename__ = "solareclipsemodel"
    eclipse_id = db.Column(db.Integer, unique=True, primary_key=True)
    year = db.Column(db.Integer, unique=False)
    month = db.Column(db.Integer, unique=False)
    day = db.Column(db.Integer, unique=False)
    td_ge = db.Column(db.String(16),unique=False)
    dt =  db.Column(db.Float, unique=False)
    luna_num = db.Column(db.Integer, unique=False)
    saros = db.Column(db.Integer, unique=False)
    eclipse_type = db.Column(db.String(16),unique=False)
    gamma = db.Column(db.Float, unique=False)
    magnitude = db.Column(db.Float, unique=False)
    # lat_ge = db.Column(db.String(16),unique=False)
    # lng_ge = db.Column(db.String(16),unique=False)
    lat_dd_ge = db.Column(db.Float, unique=False)
    lng_dd_ge = db.Column(db.Float, unique=False)
    sun_alt = db.Column(db.Float, unique=False)
    sun_azm = db.Column(db.Float, unique=False)
    path_width = db.Column(db.Float, unique=False)
    # central_duration =
    duration_secs = db.Column(db.Float, unique=False)
    cat_no = db.Column(db.Float, unique=False)
    canon_plate = db.Column(db.Float, unique=False)
    julian_date = db.Column(db.Float, unique=False)
    t0 = db.Column(db.Float, unique=False)
    x0 = db.Column(db.Float, unique=False)
    x1 = db.Column(db.Float, unique=False)
    x2 = db.Column(db.Float, unique=False)
    x3 = db.Column(db.Float, unique=False)
    y0 = db.Column(db.Float, unique=False)
    y1 = db.Column(db.Float, unique=False)
    y2 = db.Column(db.Float, unique=False)
    y3 = db.Column(db.Float, unique=False)
    d0 = db.Column(db.Float, unique=False)
    d1 = db.Column(db.Float, unique=False)
    d2 = db.Column(db.Float, unique=False)
    mu0 = db.Column(db.Float, unique=False)
    mu1 = db.Column(db.Float, unique=False)
    mu2 = db.Column(db.Float, unique=False)
    l10 = db.Column(db.Float, unique=False)
    l11 = db.Column(db.Float, unique=False)
    l12 = db.Column(db.Float, unique=False)
    l20 = db.Column(db.Float, unique=False)
    l21 = db.Column(db.Float, unique=False)
    l22 = db.Column(db.Float, unique=False)
    tan_f1 = db.Column(db.Float, unique=False)
    tan_f2 = db.Column(db.Float, unique=False)
    tmin = db.Column(db.Float, unique=False)
    tmax = db.Column(db.Float, unique=False)
    etype = db.Column(db.Integer, unique=False)
    PNS = db.Column(db.Integer, unique=False)
    UNS = db.Column(db.Integer, unique=False)
    NCN = db.Column(db.Integer, unique=False)
    nSer = db.Column(db.Integer, unique=False)
    nSeq = db.Column(db.Integer, unique=False)
    nJLE = db.Column(db.Integer, unique=False)
    start_t = db.Column(db.Float, unique=False)
    end_t = db.Column(db.Float, unique=False)

    def __init__(self, row,index):
        self.eclipse_id = index
        self.year = int(row[0])
        self.month = int(row[1])
        self.day = int(row[2])
        self.td_ge = row[3]
        self.dt = float(row[4])
        self.luna_num = int(row[5])
        self.saros = int(row[6])
        self.eclipse_type = row[7]
        self.gamma = float(row[8])
        self.magnitude = float(row[9])
        # lat_ge = db.Column(db.String(16),unique=False)
        # lng_ge = db.Column(db.String(16),unique=False)
        self.lat_dd_ge = float(row[12])
        self.lng_dd_ge = float(row[13])
        self.sun_alt = float(row[14])
        self.sun_azm = float(row[15])
        self.path_width = float(row[16])
        # central_duration =
        self.duration_secs = float(row[18])
        self.cat_no = float(row[19])
        self.canon_plate = float(row[20])
        self.julian_date = float(row[21])
        self.t0 = float(row[22])  #1
        self.x0 = float(row[23])  #6
        self.x1 = float(row[24])  #7
        self.x2 = float(row[25])  #8
        self.x3 = float(row[26])  #9
        self.y0 = float(row[27])  #10
        self.y1 = float(row[28])  #11
        self.y2 = float(row[29])  #12
        self.y3 = float(row[30])  #13
        self.d0 = float(row[31])  #14
        self.d1 = float(row[32])  #15
        self.d2 = float(row[33])  #16
        self.mu0 = float(row[34]) #17
        self.mu1 = float(row[35]) #18
        self.mu2 = float(row[36]) #19
        self.l10 = float(row[37]) #20
        self.l11 = float(row[38]) #21
        self.l12 = float(row[39]) #22
        self.l20 = float(row[40]) #23
        self.l21 = float(row[41]) #24
        self.l22 = float(row[42]) #25
        self.tan_f1 = float(row[43]) #25
        self.tan_f2 = float(row[44]) #26
        self.tmin = float(row[45])  #2
        self.tmax = float(row[46])  #3
        self.etype = int(row[47])
        self.PNS = int(row[48])
        self.UNS = int(row[49])
        self.NCN = int(row[50])
        self.nSer = int(row[51])
        self.nSeq = int(row[52])
        self.nJLE = int(row[53])

    def  eclipsectypename(self):
        if self.eclipse_type.find("T") == 0:
            return "Total"
        elif self.eclipse_type.find("H") == 0:
            return "Hybrid"
        elif self.eclipse_type .find("P") == 0:
            return  "Partial"
        elif self.eclipse_type .find("A") == 0:
            return "Annular"
        else:
            return "None"

    def elemenetsList(self):
        return [self.julian_date,self.t0,self.tmin,self.tmax,self.dt,self.dt,self.x0,self.x1,self.x2,self.x3,self.y0,self.y1,self.y2,self.y3,self.d0,self.d1,self.d2,self.mu0,self.mu1,self.mu2,self.l10,self.l11,self.l12,self.l20,self.l21,self.l22,self.tan_f1,self.tan_f2]









