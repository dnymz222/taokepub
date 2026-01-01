#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,make_response
from app import db
import urllib
import hashlib

import time
import datetime
import urllib, sys
import ssl

import json
import base64
import math

import gzip
from app.utils.constvalue import acuuappkey,meteobule_apikey
import metpy.calc as mpcalc
from metpy.units import units
import gzip
from io import StringIO
import requests
import pytz
from pymeeus.Epoch import Epoch
from pymeeus.Sun import Sun
from pymeeus.Moon import Moon
from pymeeus.Earth import Earth
import pymeeus.Coordinates

from datetime import  datetime,timezone
import time
from app.AstroEvent import AstroEvent
from config import  basedir


# @api3.route("/astroevent/china")
# def astroeventchina():
#     months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
#     year = "2025"
#     path = os.path.join(basedir,"static/astronomy",year)
#     i = 0
#     list = []
#
#     for month in months:
#         monthpath = os.path.join(path,month + ".txt")
#         file_test = open(monthpath, 'r')
#         for lines in file_test.readlines():
#             line = lines.strip('\n')
#             line = line.replace("&nbsp;", "")
#             i = i + 1
#             astro = AstroEvent(line,year,month,"8","zh",i + 1)
#
#             print(astro)
#             try:
#                 db.session.add(astro)
#                 db.session.commit()
#                 list.append(astro.astroeventdict())
#             except Exception as e:
#                 db.session.rollback()
#                 print(e)
#
#
#     return json.dumps(list)

@api3.route("/astroevent/china")
def astroeventchina():
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

    for month in months:
        year_str = "2026"
        yearpath = os.path.join(basedir,"static/astronomy",year_str)

        txtpath = os.path.join(yearpath,month +".txt")
        if os.path.exists(txtpath):
               tf = open(txtpath,"r")
               i = 0
               for lines in tf.readlines():
                   line = lines.strip('\n')
                   if len(line) > 0:
                       pass
                   else:
                       continue
                   i  = i + 1
                   astro = AstroEvent(line,i)
                   try:
                       db.session.add(astro)
                       db.session.commit()
                       print(line)
                   except Exception as e:
                       print(e)
                       db.session.rollback()


    return "done"



@api3.route("/astroevent/english")
def astroeventenglish():
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    emonths = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    n = len(months)
    monthdict = {}
    for i in range(0,n):
        emonth = emonths[i]
        monthdict[emonth] = months[i]


    timzonenames = ["art","ast","est","cst","mst","pst","akst","hst","cvt","gmt","cet","eet","msk","gst","pkt","ist","bst","ict","awst","jst","act","aest","nct","nzst"]
    timzonevalues =["-3","-4","-5","-6","-7","-8","-9","-10","-1","0","1","2","3","4","5","5.5","6","7","8","9","9.5","10","11","12"]

    m = len(timzonenames)
    timezondict = {}
    for j in range(0,m):
        timezondict[timzonenames[j]] = timzonevalues[j]


    list = []

    for year in range(2048,2101):
        year_str = str(year)
        yearpath = os.path.join(basedir,"static/astronomy/en",year_str)
        for timezonename in timzonenames:
            print(year_str)
            print(timezonename)
            timezonev = timezondict[timezonename]
            txtpath = os.path.join(yearpath,timezonename +".txt")
            if os.path.exists(txtpath):
               tf = open(txtpath,"r")
               monthnew = ""
               i = 0
               for lines in tf.readlines():
                   line = lines.strip('\n')
                   if len(line) > 0:
                       pass
                   else:
                       continue
                   month = line[0:3].strip()
                   if len(month) > 0:
                      monthnew = month
                   i  = i + 1
                   astro = AstroEvent(line,year_str,monthnew,timezonev,"en",i)
                   try:
                       db.session.add(astro)
                       db.session.commit()
                       print(line)
                   except Exception as e:
                       print(e)
                       db.session.rollback()










    return json.dumps(list)
