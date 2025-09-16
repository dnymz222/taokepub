#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage
import json
from flask import request
from app import db


import time

import json

import math
from app.water import water

import metpy.calc as mpcalc
from metpy.units import units
import gzip
from io import  StringIO







def gzip_compress(buf):
    out = StringIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(buf)
    return out.getvalue()






@api3.route("/water")
def waterget():
    host = 'https://naswater.market.alicloudapi.com'
    path = '/api/v1/surface_water/stations'

    appcode = '03302ec93478463a9e1579abc4bc8f5b'


    local_i = int(time.time())


    result = {}


    try:

        # json_res = req.addTextPara("status", '0') \
        #     .get()
        waters = db.session.query(water).all()
        list = []
        for waterobject in waters:
            sta_time = waterobject.sta_time
            
            sta_i = int(time.mktime(time.strptime(sta_time, "%Y-%m-%d %H:%M:%S")))
            if local_i - sta_i  < 2592000:
                waterdict  = waterobject.columndict()
                list.append(waterdict)
        result[x_code] = 200
        result[x_data] = list




    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()

    return json.dumps(result)







def weatherchecklatandlon(lat,lng,timestamp,total):
    latng_i = int(float(lat) * 100 * float(lng) * 100)
    timestamp_i = int(timestamp)
    local_i = int(time.time())
    deta = abs(timestamp_i - local_i)
    if deta > 360:
        return 201
    e = 2.71828
    pi = 3.14159
    c = 0.68619
    lat_fs = abs(float(lat))
    lng_fs = abs(float(lng))
    he = math.pow(lat_fs, e) + math.pow(lng_fs, pi)
    he_in = int(he)
    token_i = int(total)
    t_i = int(math.pow(timestamp_i, c))

    if abs(t_i + latng_i + he_in - token_i) < 200:
        return 200
    else:
        return 202



@api3.route("/wetbulb/temperature")
def wetbulbtemperature():

    temp = float(request.args.get("temp","20"))
    dewpoint = float(request.args.get("dewpoint","16"))
    pressure = float(request.args.get("pressure","1013.25"))


    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}

    try:
        wetbulbtemp  = mpcalc.wet_bulb_temperature(pressure =pressure* units.hPa, temperature=temp*units.degC, dewpoint =dewpoint*units.degC)
        lclpressure,lcltemperature = mpcalc.lcl(pressure=pressure * units.hPa, temperature=temp * units.degC, dewpoint=dewpoint * units.degC)

        dict = {}
        dict["wet_bulb"] = wetbulbtemp.magnitude
        dict["lcl_pressure"]  = lclpressure.magnitude
        dict["lcl_temperature"]  = lcltemperature.magnitude


        result[x_code] = 200
        result[x_data] = dict
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code]  =201


    return json.dumps(result)


@api3.route("/metpy/lcl")
def metlcl():

    temp = float(request.args.get("temp","20"))
    humidity = float(request.args.get("humidity","50"))
    dewpoint = float(request.args.get("dewpoint","16"))
    pressure = float(request.args.get("pressure","1013.25"))


    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}

    try:
        lcl  = mpcalc.lcl(pressure =pressure* units.hPa, temperature=temp*units.degC, dewpt =dewpoint*units.degC)
        # parcel_profile  =mpcalc.parcel_profile(pressure=[pressure ]* units.hPa, temperature=temp * units.degC, dewpt=dewpoint * units.degC)
        #
        # el =  mpcalc.el(pressure=pressure * units.hPa, temperature=temp * units.degC, dewpt=dewpoint * units.degC)
        lfc = mpcalc.lfc(pressure=[1031.25] * units.hPa, temperature=[temp] * units.degC, dewpt=[dewpoint] * units.degC)



    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code]  =201


    return json.dumps(result)




@api3.route("/metpy/lfc")
def metlfc():

    temp = float(request.args.get("temp","20"))
    humidity = float(request.args.get("humidity","50"))
    dewpoint = float(request.args.get("dewpoint","16"))
    pressure = float(request.args.get("pressure","1013.25"))


    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}

    try:
        lfcpressure,lfctemperature  = mpcalc.lcl(pressure =pressure* units.hPa, temperature=temp*units.degC, dewpoint =dewpoint*units.degC)


    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code]  =201


    return json.dumps(result)