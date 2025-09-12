#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,hefengfishingapikey,hefengusername,acuuappkey
import json
from flask import request,session,url_for,redirect
from app import db
import hashlib
import time
import datetime
import ssl

import json
import base64
import math
import requests

from config import basedir
from flask import send_file
import shutil



@api3.route("/lpm/<z>/<x>/<y>")
def lpmwepbimage(z, x, y):
   path =  os.path.join(basedir,"static/lpmwebp")
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/tide/world/<t>/<z>/<x>/<y>")
def tideworldwepbimage(t,z, x, y):
   path =  os.path.join(basedir,"static/tide/world",t)
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(path, filename)
       if os.path.exists(fpath):
            return send_file(fpath,as_attachment=True)
       else:
           return ""


   except Exception as e:
       return "%s"%e


@api3.route("/lpm/altas/year/<year>/<z>/<x>/<y>")
def lpmaltasyearwepbimage(year,z, x, y):

   path = os.path.join(basedir, "static/altas" + year)
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e
@api3.route("/lpm/year/<year>/<z>/<x>/<y>")
def lpmyearwepbimage(year,z, x, y):

   if year == "2015":
       path =  os.path.join(basedir,"static/world2015")
   else:
       path = os.path.join(basedir, "static/vnl" + year)
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/lpm/year/move/<year>")
def lpmyearmovewepbimage(year):


   if year == "2023" or year == "2020":
       return "done"

   if year == "2015":
       path =  os.path.join(basedir,"static/world2015")
   else:
       path = os.path.join(basedir, "static/vnl" + year)

   for z in range(10, 11):
       for x in range(0, int(pow(2, z) + 0.1)):
           for y in range(0, int(pow(2, z) + 0.1)):
               filename = str(z) +"_" + str(x) + "_"  + str(y) + ".webp"
               filepath = os.path.join(path,filename)
               if os.path.exists(filepath):
                   os.remove(filepath)


   return "done"

@api3.route("/lpm/move")
def lpmmove():

    bathyPath = os.path.join(basedir, 'static/lpmwepb')
    bathydownloadPath = os.path.join(basedir, 'static/lpmwepb9')


    for parent, _, fileNames in os.walk(bathydownloadPath):
        for filename in fileNames:
            if filename.find("DS_Store")< 0:
                dpth = os.path.join(bathydownloadPath,filename)
                tpath = os.path.join(bathyPath,filename)
                shutil.move(dpth,tpath)
    return "done"



@api3.route("/bathy/<z>/<x>/<y>")
def bathywepbimage(z, x, y):
   path =  os.path.join(basedir,"static/bathywepb")
   filename = z +"_" + x + "_"  + y + ".wepb"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/bathy/china/<z>/<x>/<y>")
def bathychinawepbimage(z, x, y):
   path =  os.path.join(basedir,"static/bathychinawebp")
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/elevation/<z>/<x>/<y>")
def elevationwepbimage(z, x, y):

   t = request.args.get('t', '1550069439')
   zint = int(z)
   xint = int(x)
   yint = int(y)
   tcheck = (zint + 1) * (xint + 1) * ( yint + 1)
   tuplod = int(t)
   if tcheck != tuplod:
       return ""
   s = request.args.get("s",'1550069439')
   supload= int(s)
   scheck = secrect(tcheck,zint,xint,yint)
   if abs(supload-scheck) > 1366:
       return ""

   path =  os.path.join(basedir,"static/elevationwebp")
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e



@api3.route("/chao/<t>")
def chaoimage(t):
   path =  os.path.join(basedir,"static/downloads/tide/china")
   filename = t + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       print(e)
       return "none picture"

@api3.route("/surge/<index>/<t>")
def surgeimage(index,t):
   surfPath = os.path.join(basedir, 'static/downloads/stofs')

   imagedatepath = os.path.join(surfPath, "northimage/image" + index)
   filename = t + ".webp"
   try:
       fpath = os.path.join(imagedatepath, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       print(e)
       return "none picture"



def secrect(t,z,x,y):

    e = 2.71828
    pi = 3.14159
    c = 0.68619
    i = tileIndexCount(z,x,y);
    v = pow(i,1 / e) / pi + pow(t,c)
    return  int(v) + i % 1366




def tileIndexCount(z,x,y):
    zpow = powz(z)
    return  x * zpow + y + degradecount(z)



def powz(z):

    y = 1
    for i in range(0,z):
        y = y * 2
    return y
def degradecount(z):

    y = 0
    for i in range(0,z):
        y = y + powz(i) * powz(i)

    return y