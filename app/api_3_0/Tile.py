#coding=utf8
import os.path

from . import api3
from flask import request
import datetime
from config import basedir
from flask import send_file
import shutil



@api3.route("/lpm/<z>/<x>/<y>")
def lpmwepbimage(z, x, y):
   path =  os.path.join(basedir,"static/lpmwepb")
   filename = z +"_" + x + "_"  + y + ".wepb"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e



@api3.route("/cams/cloudmap/<type>/<time>")
def cloudmapcams(type,time):
   path =  os.path.join(basedir,"static/CAMS/cloud_china")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/cams/cloudrgbmap/<type>/<time>")
def cloudrgbmapcams(type,time):
   path =  os.path.join(basedir,"static/CAMS/cloud_world")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/cams/glow/<type>/<time>")
def glowrgbmapcams(type,time):
   path =  os.path.join(basedir,"static/CAMS/glow")
   filename =  time + "_" + type + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/cams/riseset/<type>/<time>")
def riseserrgbmapcams(type,time):
   path =  os.path.join(basedir,"static/CAMS/riseset")
   filename =  time + "_" + type + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/clear/cams/oval")
def clearcamsovalredimage():

    camsPath = os.path.join(basedir, 'static/CAMS/riseset')

    for parent, _, fileNames in os.walk(camsPath):
        for filename in fileNames:
            if filename.find(".webp") > 0 :
                jpath = os.path.join(camsPath,filename)
                os.remove(jpath)

    tpxoPath = os.path.join(basedir, 'static/CAMS/glow')

    for parent, _, fileNames in os.walk(tpxoPath):
        for filename in fileNames:
            if filename.find(".webp") > 0 :
                jpath = os.path.join(tpxoPath,filename)
                os.remove(jpath)

    ovalpath = os.path.join(basedir, 'static/Aurora/oval')
    for parent, _, fileNames in os.walk(ovalpath):
        for filename in fileNames:
            if filename.find(".webp") > 0 :
                jpath = os.path.join(ovalpath,filename)
                os.remove(jpath)

    return "done"


@api3.route("/cams/cloudrgbmap/clear")
def cloudrgbclear():
    now = datetime.datetime.utcnow()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zertimestmap = int(zero_today.timestamp()) - 48 * 3600
    path = os.path.join(basedir, "static/CAMS/cloud_world")
    list = ["hcc", "lcc", "mcc", "tcc", "aod550", "vis", "cbh","blh"]
    for i in range(0,1000):
        time = zertimestmap - i * 3600
        for type in list:
            filename = type + "_" + str(time) + ".webp"
            filepath = os.path.join(path,filename)
            if os.path.exists(filepath):
                os.remove(filepath)

    return "done"


@api3.route("/copernicus/china/clear")
def copernicuschinaclear():
    now = datetime.datetime.utcnow()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zertimestmap = int(zero_today.timestamp()) - 24 * 3600
    path = os.path.join(basedir, "static/copernicus")

    tpxoPath = os.path.join(path, 'china')

    for parent, _, fileNames in os.walk(tpxoPath):
        for filename in fileNames:
            if filename.find(".webp") > 0 :
                timestamp = int(filename[-15:-5])
                if timestamp < zertimestmap:
                    jpath = os.path.join(tpxoPath,filename)
                    os.remove(jpath)


    return "done"





@api3.route("/ecmwf/rgbmap/<type>/<time>")
def ecmwfrgbmap(type,time):
   path =  os.path.join(basedir,"static/ECMWF/red")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e


@api3.route("/gfs/rgbmap/<type>/<time>")
def gfsrgbmap(type,time):
   path =  os.path.join(basedir,"static/GFS/red")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/copernicus/rgbmap/<type>/<time>")
def copernicusrgbmap(type,time):
   path =  os.path.join(basedir,"static/copernicus/red")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/copernicus/china/<type>/<time>")
def copernicuschinamap(type,time):
   path =  os.path.join(basedir,"static/copernicus/china")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/tide/china/<type>/<time>")
def tidechinamap(type,time):
   path =  os.path.join(basedir,"static/TIDE/china")
   filename = type + "_"  + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e

@api3.route("/tide/rgbmap/<time>")
def tidergbmap(time):
   path =  os.path.join(basedir,"static/TIDE/red")
   filename =  "tide_" + time + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e


@api3.route("/ecmwf/rgbmap/clear")
def ecmwfrgbclear():
    now = datetime.datetime.utcnow()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zertimestmap = int(zero_today.timestamp()) - 48 * 3600
    path = os.path.join(basedir, "static/ECMWF/red")
    list = ["precipitation", "temperature", "temperaturechange", "wave", "wind","tide","wind2"]
    for i in range(0, 1000):
        time = zertimestmap - i * 3600
        for type in list:
            filename = type + "_" + str(time) + ".webp"
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)

    return "done"

@api3.route("/gfs/rgbmap/clear")
def gfsrgbclear():
    now = datetime.datetime.utcnow()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zertimestmap = int(zero_today.timestamp()) - 48 * 3600
    path = os.path.join(basedir, "static/GFS/red")
    list = ["significant", "swell1", "swell2", "swell3", "wind","windwave"]
    for i in range(0, 1000):
        time = zertimestmap - i * 3600
        for type in list:
            filename = type + "_" + str(time) + ".webp"
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)

    return "done"

@api3.route("/copernicus/rgbmap/clear")
def copernicusrgbclear():
    now = datetime.datetime.utcnow()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zertimestmap = int(zero_today.timestamp()) - 48 * 3600
    path = os.path.join(basedir, "static/copernicus/red")
    list = [ "swell1p", "swell2p", "sealevel", "wavep","windwavep","swell1h", "swell2h", "waveh","windwaveh"]
    depthmeteolist = ["chlorophylla","ph","oxyge","watercurrent","watersalinity","watertemperature"]
    depthlist = ["0","22","56","110"]
    for i in range(0, 1000):
        time = zertimestmap - i * 3600
        for type in list:
            filename = type + "_" + str(time) + ".webp"
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        for depthmeteo in depthmeteolist:
            for depth in depthlist:
                filename = depthmeteo + "_"  + depth + "_" + str(time) + ".webp"
                filepath = os.path.join(path, filename)
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

   path =  os.path.join(basedir,"static/elevationwepb")
   filename = z +"_" + x + "_"  + y + ".wepb"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

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


@api3.route("/mountain/<mountain_id>/<z>/<x>/<y>")
def  mountainwepbimage(mountain_id,z, x, y):
   path =  os.path.join(basedir,"static/mountain")
   mountainpath = os.path.join(path,mountain_id)
   filename = z +"_" + x + "_"  + y + ".webp"
   try:
       fpath = os.path.join(mountainpath, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return ""



def secrect(t,z,x,y):

    e = 2.71828
    pi = 3.14159
    c = 0.68619
    i = tileIndexCount(z,x,y);
    v = pow(i,1 / e) / pi + pow(t,c)
    return  int(v) + i % 1366


@api3.route("/solareclipse/video/<date>")
def solareclipsevideo(date):
   path =  os.path.join(basedir,"static/Solareclipse/Video")
   filename = date + ".mp4"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e



@api3.route("/astronomy/<id>")
def astronomywepbimage(id):
   path =  os.path.join(basedir,"static/astronomy","webp")
   filename = id + ".webp"
   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return "%s"%e


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