#coding=utf8
from . import solunar
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,make_response
from app import db

import urllib
import hashlib

import time


from app.HIPStar import HIPStar
from app.HDStar import HDStar
from app.HRStar import HRStar
from app.SAOStar import SAOStar
from app.CCDMStar import CCDMStar
from app.NGCCStar import NGCCStar
from app.GCVSStar import GCVSStar
from app.Tycho import Tycho
from app.TychoSuppl import TychoSuppl
from app.Tycho2 import Tycho2



@solunar.route("/tycho2/nearby")
def tycho2nearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        tycho2s = db.session.query(Tycho2).filter(Tycho2.RAdeg < ra_f+1/6.0,Tycho2.RAdeg>ra_f-1/6.0,Tycho2.DEdeg>de_f-1,Tycho2.DEdeg<de_f+1).all()
        for tycho2object in tycho2s:
            dict = tycho2object.Tycho2Dict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)

@solunar.route("/tychosp/nearby")
def tychospnearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        tychosps = db.session.query(TychoSuppl).filter(TychoSuppl.RAdeg < ra_f+1/6.0,TychoSuppl.RAdeg>ra_f-1/6.0,TychoSuppl.DEdeg>de_f-1,TychoSuppl.DEdeg<de_f+1).all()
        for tychospobject in tychosps:
            dict = tychospobject.tychosupplDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"

    return json.dumps(result)



@solunar.route("/tycho/nearby")
def tychonearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        tychos = db.session.query(Tycho).filter(Tycho.RA199125 < ra_f+1/6.0,Tycho.RA199125>ra_f-1/6.0,Tycho.DE199125>de_f-1,Tycho.DE199125<de_f+1).all()
        for tychoobject in tychos:
            dict = tychoobject.tychodict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)

@solunar.route("/hip/nearby")
def hipnearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        hips = db.session.query(HIPStar).filter(HIPStar.RA199125 < ra_f+1/6.0,HIPStar.RA199125>ra_f-1/6.0,HIPStar.DE199125>de_f-1,HIPStar.DE199125<de_f+1).all()
        for hipobject in hips:
            dict = hipobject.HIPStarDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)


@solunar.route("/hd/nearby")
def hdnearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        hds = db.session.query(HDStar).filter(HDStar.RAB1900 < ra_f+1/6.0,HDStar.RAB1900>ra_f-1/6.0,HDStar.DEB1900>de_f-1,HDStar.DEB1900<de_f+1).all()
        for hdobject in hds:
            dict = hdobject.HDStarDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)

@solunar.route("/hr/nearby")
def hrnearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        hrs = db.session.query(HDStar).filter(HRStar.RA2000 < ra_f+1/6.0,HRStar.RA2000>ra_f-1/6.0,HRStar.Dec2000>de_f-1,HRStar.Dec2000<de_f+1).all()
        for hrobject in hrs:
            dict = hrobject.HRStarDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)


@solunar.route("/sao/nearby")
def saonearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        saos = db.session.query(SAOStar).filter(SAOStar.RA1950 < ra_f+1/6.0,SAOStar.RA1950>ra_f-1/6.0,SAOStar.DE1950>de_f-1,SAOStar.DE1950<de_f+1).all()
        for saoobject in saos:
            dict = saoobject.SAOStarDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)


@solunar.route("/gcvs/nearby")
def gcvsnearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        gcvss = db.session.query(GCVSStar).filter(GCVSStar.RA1950 < ra_f+1/6.0,GCVSStar.RA1950>ra_f-1/6.0,GCVSStar.DE1950>de_f-1,GCVSStar.DE1950<de_f+1).all()
        for gcvsobject in gcvss:
            dict = gcvsobject.GVVStrarDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)


@solunar.route("/ngc/nearby")
def ngcnearby():
    ra = request.args.get("ra","0")
    de = request.args.get("de","0")
    ra_f = float(ra)
    de_f = float(de)
    result = {}
    list = []

    try:
        ngcs = db.session.query(NGCCStar).filter(NGCCStar.RAB2000 < ra_f+1/6.0,NGCCStar.RAB2000>ra_f-1/6.0,NGCCStar.DEB2000>de_f-1,NGCCStar.DEB2000<de_f+1).all()
        for ngcobject in ngcs:
            dict = ngcobject.NGCCStarDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)