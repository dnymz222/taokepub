from app import Comet
from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage
from flask import request
from app import db


import time
import datetime

import json

import math


@api3.route("/comet/upload")
def commetpload():

    commet = Comet(number = "C/2025 A6 (Lemmon)")

    commet.OrbitalPeriod = str(1347.713943707547) #period 年
    commet.SemeMajorAxis = str(122.0093217668168) #a
    commet.Inclination = str(143.6632748988036)  #i
    commet.Ecc = str(0.9956568328248037)   #e
    commet.PerihelionDistance = str(0.5299068813656069)  #q
    commet.LongitudeAscendingNode = str(108.0976178317535) #node
    commet.PerihelionArgument = str(132.9672366055109) #peri
    commet.MeanAnomaly = str(359.9337871412166) #M
    commet.PerihelionPassageTime = str(2460988.037351266917) #tp
    commet.MeanMotion = str(0.0007313319625202579) #n
    commet.AphelionDistance = str(243.488736652268) #Q

    commet.Epoch = str(2460897.5) #
    commet.MotionType = 3 #1.椭圆 2.抛物线 3.准抛物线
    commet.TotalMagnitude = str(9.8) #M1
    commet.TotalMagnitudeSlope = str(13.5)  # K1

    try:
        db.session.add(commet)
        db.session.commit()
    except Exception as e:
        db.session.rollback()




