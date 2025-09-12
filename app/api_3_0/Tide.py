#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,worlrtide_secret,hefengfishingapikey
from flask import request,session,url_for,redirect
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
from app.worldTidalStation import worldTidalStation
from app.chinaTidalStation import chinaTidalStation
from config import basedir
import os
import  xarray as xr
import  selenium
import requests
from app.utils.constvalue import xinzhi_public_key,xinzhi_prinvate_key




@api3.route('/tide/world/forecast')
def worldtideforecast():
    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}
    code = checklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    if 200 == code:
        pass
    elif 201 == code:
        result[x_code] = 201
        result[x_meesage] = "time out ,no data"
        return json.dumps(result)
    elif 202 == code:
        result[x_code] = 202
        result[x_meesage] = "error,no data!"
        return json.dumps(result)

    try:

        url  ="https://www.worldtides.info/api?heights&extremes&length=604800&lat="+lat+"&lon="+lng+"&key=" + worlrtide_secret
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data]= json.loads(content)
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 203


    return json.dumps(result)



@api3.route('/tide/world/forecast/v2')
def worldtideforecast_v2():
    lat = request.args.get('lat', '21.966700')
    lng = request.args.get('lng', '120.750000')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    timezone = request.args.get("timezone","Asia/Shanghai")
    day = request.args.get("day","2021-08-31")
    result = {}
    code = checklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    if 200 == code:
        pass
    elif 201 == code:
        result[x_code] = 201
        result[x_meesage] = "time out ,no data"
        return json.dumps(result)
    elif 202 == code:
        result[x_code] = 202
        result[x_meesage] = "error,no data!"
        return json.dumps(result)

    try:

        url  ="https://www.worldtides.info/api/v2?heights&extremes&days=7&date="+day+"&lat="+lat+"&lon="+lng+"&timezone="+timezone+"&key=" + worlrtide_secret

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data]= json.loads(content)
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 203


    return json.dumps(result)

@api3.route('/tide/world/stations')
def worldtidestation():
    result ={}
    try:
        array = []
        stations =  db.session.query(worldTidalStation).all()
        for station in stations:
           dict  = station.worldstationdict()
           array.append(dict)
        result[x_code] = 200
        result[x_data] = array

    except Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code]  =201

    finally:
       db.session.close()

    return json.dumps(result)


@api3.route('/tide/china/forecast')
def chiantideforecast():

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}
    code = checklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
    if 200 == code:
        pass
    elif 201 == code:
        result[x_code] = 201
        result[x_meesage] = "time out ,no data"
        return json.dumps(result)
    elif 202 == code:
        result[x_code] = 202
        result[x_meesage] = "error,no data!"
        return json.dumps(result)




    try:
        port = request.args.get('port','WTWFRHBJHX9W')
        url  ="https://api.seniverse.com/v3/tide/daily.json?key="+ xinzhi_prinvate_key+"&port="+port

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)
        result[x_code] = 200
        list = []
        datadict = contentdict['results'][0]
        for dict in datadict["data"]:
            # print dict
            if "range" in dict:
                list.append(dict)
        resultdict = {}
        if len(list) > 0:
            resultdict["data"] = list
            resultdict["port"] = datadict["port"]
            result[x_data] = resultdict
        else:
            result[x_meesage] = "红色图标潮汐暂不可用，请选择蓝色图标"
            result[x_code] = 201

    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


# @api3.route('/tide/china/forecast')
# def chiantideforecast():
#
#     lat = request.args.get('lat', '37.513')
#     lng = request.args.get('lng', '122.12')
#     timestamp = request.args.get('time', '1550069439')
#     total = request.args.get('total', '1599918717')
#     result = {}
#     code = checklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
#     # if 200 == code:
#     #     pass
#     # elif 201 == code:
#     #     result[x_code] = 201
#     #     result[x_meesage] = "time out ,no data"
#     #     return json.dumps(result)
#     # elif 202 == code:
#     #     result[x_code] = 202
#     #     result[x_meesage] = "error,no data!"
#     #     return json.dumps(result)
#
#
#
#
#     try:
#         port = request.args.get('port','P2951')
#         url  ="https://api.qweather.com/v7/ocean/tide?key="+hefengfishingapikey+"&location="+port+"&date=20220110"
#         print url
#         req = urllib2.Request(url)
#         response = urllib2.urlopen(req)
#         content = response.read()
#         contentdict = json.loads(content)
#         result[x_code] = 200
#         list = []
#         datadict = contentdict['results'][0]
#         for dict in datadict["data"]:
#             print dict
#             if dict.has_key("range") and  len(dict["range"]) >0:
#                 list.append(dict)
#         resultdict = {}
#         if len(list) > 0:
#             resultdict["data"] = list
#             result[x_data] = resultdict
#         else:
#             result[x_meesage] = "红色图标潮汐暂不可用，请选择蓝色图标"
#             result[x_code] = 201
#
#     except Exception, e:
#         result[x_meesage] = e.message
#         result[x_code] = 201
#     return json.dumps(result)

@api3.route('/station/china')
def chinastations():
    result = {}
    try:
        array = []
        stations = db.session.query(chinaTidalStation).all()
        for station in stations:
            dict = station.chinastationdict()
            array.append(dict)
        result[x_code] = 200
        result[x_data] = array

    except Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    finally:
        db.session.close()

    return json.dumps(result)


@api3.route('/stations')
def stations():
    array = []
    try:

        stations = db.session.query(chinaTidalStation).all()
        for station in stations:
            dict = station.chinastationdict()
            array.append(dict)

        wstations = db.session.query(worldTidalStation).all()
        for wstation in wstations:
            wdict = wstation.worldstationdict()
            array.append(wdict)


    except Exception as e:
        db.session.rollback()
        print(e)


    finally:
        db.session.close()

    return json.dumps(array)





def checklatandlon(lat,lng,timestamp,total):
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

    if abs(t_i + latng_i + he_in - token_i) < 1000:
        return 200
    else:
        return 202

    
    
@api3.route('/ukho/tides/stations')
def ukhostaions():
    url = "https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/7183"
    req = urllib.request.Request(url)

    req.add_header('Ocp-Apim-Subscription-Key', '3e98068e498b4b4e873b869fd9a72ad0')

    response = urllib.request.urlopen(req)
    content = response.read()
    return content



@api3.route("/all/stations")
def allstations():
    upload_path = os.path.join(basedir, 'static', "worldstation.json")
    list = []


    try:

        stations = db.session.query(chinaTidalStation).all()
        for station in stations:
            dict = station.chinastationdict()
            list.append(dict)



    except Exception as  e:
        db.session.rollback()
        print(e)


    finally:
        db.session.close()

    try:

        url = "https://www.worldtides.info/api/v2?stations&lat=30.768321&lon=120.195617&stationDistance=3300&key=" + worlrtide_secret
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        jsondata = json.loads(content)


        stations = jsondata["stations"]
        for dict in stations:
            ndict = {}
            ndict["stationId"] = dict["id"]
            ndict["station"] = dict["name"]
            ndict["lat"] = float(dict["lat"])
            ndict["lon"] = float(dict["lon"])
            ndict["type"] = 2
            ndict["timezone"] = dict["timezone"]

            ndict['sealevel'] = ""


            if ndict["timezone"] =="Asia/Shanghai":
                list.append(ndict)
    except Exception as e:
        print(e)

    jsonstring = json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'tidestation.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return "done"


@api3.route("/tide/constant/all/<lat>/<lng>")
def tideconstant(lat,lng):
    result = {}
    # lat = request.args.get('lat', '21.57')
    # lng = request.args.get('lng', '109.56')
    language = request.args.get('language', 'en-us')
    chao = request.args.get("chao","0")

    try:
        response = requests.get(
            'https://www.astronomyobserver.net/api/v3.0/tide/constant/all/'+ lat +"/" +lng,
            params={
                "language": language,
                "chao":chao

            },

        )

        # print  response

        # Do something with response data.
        json_data = response.json()
        return json.dumps(json_data)
    except Exception as e:
        print(e)
        return "hello word"


    # lng_int =int((float(lng) + 180)*30)
    # lat_int =int((90 - float(lat))*30)
    # has,new_lat,new_lng = checkdataAvaliable(lat_int,lng_int)
    # if has:
    #     tpxoPath = os.path.join(basedir, 'static/TPXO')
    #     dict = {}
    #     for parent, _, fileNames in os.walk(tpxoPath):
    #         for name in fileNames:
    #             if name.startswith('.'):  # 去除隐藏文件
    #                 continue
    #             elif name.startswith("h_"):
    #                 filepath = os.path.join(tpxoPath,name)
    #                 index = name.find("_tpxo9")
    #                 key = name[2:index]
    #                 ds = xr.open_dataset(filepath)
    #                 him = ds["hIm"][new_lng].values[new_lat]
    #                 hre = ds["hRe"][new_lng].values[new_lat]
    #                 dict[key] = str(hre)+","+ str(him)
    #             elif name.startswith("grid"):
    #                 filepath = os.path.join(tpxoPath, name)
    #                 ds = xr.open_dataset(filepath)
    #                 hu = ds["hu"][new_lng].values[new_lat]
    #                 hv = ds["hv"][new_lng].values[new_lat]
    #                 hz = ds["hz"][new_lng].values[new_lat]
    #                 dict["grid"] = str(hu)+","+str(hv) +"," + str(hz)
    #
    #     resultdict = {}
    #     resultdict[x_data] = dict
    #     resultdict["request_lat"] = lat
    #     resultdict["requset_lon"] = lng
    #     response_lat =90- new_lat/30.0
    #     response_lon = new_lng/30.0-180
    #     resultdict["response_lat"] = str(response_lat)
    #     resultdict["response_lon"] = str(response_lon)
    #     result[x_data] = resultdict
    #     result[x_code] = 200
    # else:
    #     result[x_meesage] = "no data"
    #     result[x_code] = 203
    # return  json.dumps(result)


def checkdataAvaliable(lat_int,long_int):
    tpxopath = os.path.join(basedir,"static/TPXO","h_m2_tpxo9_atlas_30_v5.nc")
    ds = xr.open_dataset(tpxopath)
    has  = False

    new_lat = lat_int
    new_lng = long_int

    try:
        him = ds["hIm"][new_lng].values[new_lat]
        if abs(him) > 0:
            has = True
            return (has, new_lat, new_lng)

    except Exception as e:
        print(e)

    try:
        for i in range(1,4):
            for j in range(0,4):
                if  0 == j:
                    new_lat = lat_int + i
                    new_lng = long_int + i
                    him = ds["hIm"][new_lng].values[new_lat]
                    if  abs(him) > 0:
                        has = True
                        return  (has,new_lat,new_lng)
                elif 1 == j:
                    new_lat = lat_int - i
                    new_lng = long_int + i
                    him = ds["hIm"][new_lng].values[new_lat]
                    if abs(him) > 0:
                        has = True
                        return (has, new_lat, new_lng)
                elif 2== j:
                    new_lat = lat_int + i
                    new_lng = long_int - i
                    him = ds["hIm"][new_lng].values[new_lat]
                    if abs(him) > 0:
                        has = True
                        return (has, new_lat, new_lng)
                else:
                    new_lat = lat_int - i
                    new_lng = long_int - i
                    him = ds["hIm"][new_lng].values[new_lat]
                    if abs(him) > 0:
                        has = True
                        return (has, new_lat, new_lng)

    except:
        pass


    return  (has,new_lat,new_lng)




def tidetpxoconstantsingleLocation(lat,lng):
    tpxoPath = os.path.join(basedir, 'static/TPXO')

    dict = {}
    dict["lng"] = lng
    dict["lat"] = lat
    hlist = []
    ulist =[]
    gridlist = []


    constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4","S1"]

    #h
    for cons in constants:
        c = cons.lower()
        try:
            filename =  "h_"+ c +"_tpxo9_atlas_30_v5.nc"
            filepath = os.path.join(tpxoPath, filename)
            ds = xr.open_dataset(filepath)
            # print(ds)
            him = ds["hIm"][lng].values
            hre = ds["hRe"][lng].values

            himvalue = him[lat]
            hrevalue = hre[lat]


            if c == "m2":
                if abs(float(himvalue)) < 0.0001 and abs(float(hrevalue)) < 0.0001:
                    dict["value"] = False
                else:
                    dict["value"] = True
            hlist.append(int(himvalue))
            hlist.append(int(hrevalue))
            ds.close()
        except Exception as e:
            print(e)


    for con in constants:
        c = con.lower()
        try:
            filename =  "u_"+ c +"_tpxo9_atlas_30_v5.nc"
            filepath = os.path.join(tpxoPath, filename)
            ds = xr.open_dataset(filepath)
            uim = ds["uIm"][lng].values
            ure = ds["uRe"][lng].values

            vim = ds["vIm"][lng].values
            vre = ds["vRe"][lng].values

            uimvalue = uim[lat]
            urevalue = ure[lat]
            vimvalue = vim[lat]
            vrevalue = vre[lat]
            ulist.append(int(uimvalue))
            ulist.append(int(urevalue))
            ulist.append(int(vimvalue))
            ulist.append(int(vrevalue))
            ds.close()
        except Exception as  e:
            print(e)

    if 1:
        filename = "grid_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)
        # print(ds)
        hu = ds["hu"][lng].values
        hv = ds["hv"][lng].values
        hz = ds["hz"][lng].values

        lat = dict["lat"]
        huvalue = hu[lat]
        hvvalue = hv[lat]
        hzvalue = hz[lat]


        gridlist.append(float(huvalue))
        gridlist.append(float(hvvalue))
        gridlist.append(float(hzvalue))
        ds.close()

    dict["h"] = hlist
    dict["u"] = ulist
    dict["grid"] = gridlist


    return dict


def latIndex(lat):
    latvalue = lat + 90
    return int(round(latvalue * 30))

def lngIndex(lng):
    lngvalue = 0
    if lng < 1 / 60 :
        lngvalue = lng  + 360
    else:
        lngvalue = lng
    return int(round(lngvalue * 30 - 1))

@api3.route("/tide/constant/check/<lat>/<lng>")
def tideconstantcheck(lat,lng):
    latindex = latIndex(float(lat))
    lngindex = lngIndex(float(lng))
    result = {}
    try:
        tpxoPath = os.path.join(basedir, 'static/TPXO')
        filename = "h_m2_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)
        him = ds["hIm"][lngindex].values
        hre = ds["hRe"][lngindex].values
        himvalue = him[latindex]
        hrevalue = hre[latindex]
        datadict = {}
        if abs(float(himvalue)) < 0.0001 and abs(float(hrevalue)) < 0.0001:
            datadict["value"] = False
        else:
            datadict["value"] = True
        result[x_code] = 200
        result[x_data] = datadict


    except Exception as e:
        print(e)
        result[x_code] = 201
        result[x_meesage] = "%s"%e
    return json.dumps(result)






