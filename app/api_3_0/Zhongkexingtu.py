#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage,zhongkexingtu_token,xingtuyun_token
from flask import request
import datetime
import urllib
import json

import requests
from config import basedir
import shutil
from PIL import Image
import math
import pytz
from PIL.ImageFile import ImageFile as ImageReadFile

shanghai_tz = pytz.timezone("Asia/Shanghai")



@api3.route("/zhongkexingtu/huoshaoyun/point")
def huoshaoyunpoint():
    result = {}

    lat = request.args.get('lat', '31.00')
    lng = request.args.get('lng', '120')
    start = request.args.get("start","2025050500")
    end = request.args.get("end","2025050800")
    location = lat + "," + lng

    url = "https://tiles.geovisearth.com/meteorology/v1/weather/grid/glow/day/data?location="+location + "&start="+start+"&end="+end+"&meteCodes=glow&level=true&token=" + zhongkexingtu_token

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        datadict = json.loads(content)

        result[x_code] = 200
        result[x_data] = datadict["result"]

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route("/zhongkexingtu/huoshaoyun")
def huoshaoyunold():
    result = {}


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    start = request.args.get("start","2025050400")
    end = request.args.get("end","2025050700")
    location = lat + "," + lng

    latf = float(lat)
    lngf = float(lng)

    if latf > 55 or latf < 15:
        result[x_code] = 201
        result[x_meesage] = "out boundry"
        return json.dumps(result)
    if lngf > 136 or lngf < 72:
        result[x_code] = 201
        result[x_meesage] = "out boundry"
        return json.dumps(result)




    huoshaoyunpath = os.path.join(basedir,"static/CAMS","glow")

    localdaynow = datetime.datetime.now(tz=shanghai_tz)


    datalist = []

    vlongitude = (lngf - 72) * 12
    vlatitude = (55 - latf) * 12

    for i in range(0,3):
        daytome = localdaynow + datetime.timedelta(days=i)
        utcyear = daytome.year
        utcmonth = daytome.month
        utcday = daytome.day

        daystr = "%d%02d%02d" % (utcyear, utcmonth, utcday)


        risepath = os.path.join(huoshaoyunpath, daystr + "_rise.webp")

        setpath = os.path.join(huoshaoyunpath, daystr + "_set.webp")


        if os.path.exists(risepath):
            dict = {}
            riseimage = Image.open(risepath)
            Tsunrise = getGlowValue(riseimage, vlongitude, vlatitude)
            dict["month"] = "%02d"%utcmonth
            dict["day"] = "%02d"%utcday
            dict["hour"] = "06"
            dict["value"] = Tsunrise
            dict["level"] = getGlowType(Tsunrise)
            dict["type"] = 0

            datalist.append(dict)
            riseimage.close()


        else:
            pass


        if os.path.exists(setpath):
            dict = {}
            setimage = Image.open(setpath)
            Tsunset = getGlowValue(setimage, vlongitude, vlatitude)
            dict["month"] = "%02d" % utcmonth
            dict["day"] = "%02d" % utcday
            dict["hour"] = "18"
            dict["value"] = Tsunset
            dict["level"] = getGlowType(Tsunset)
            dict["type"] = 1

            datalist.append(dict)
            setimage.close()
        else:
            pass

    if len(datalist) > 0:
        result[x_code] = 200
        result[x_data] = datalist
    else:
        result[x_code] = 201
        result[x_meesage] = "nodata"
    return json.dumps(result)

def getGlowType(value):
    if value < 0.1:
        return 0
    elif value < 0.2:
        return 1
    elif value < 0.3:
        return 2
    elif value < 0.4:
        return 3
    elif value < 0.5:
        return 4
    else:
        return 5

def getGlowValue(image:ImageReadFile,vlongitude:float,vlatitude:float):
    lng_floor = int(math.floor(vlongitude))
    lat_floor = int(math.floor(vlatitude))
    lat_ceil = int(math.ceil(vlatitude))
    lng_ceil = int(math.ceil(vlongitude))
    if lat_ceil > 480:
        lat_ceil = 480
    if lng_ceil > 768:
        lng_ceil = 768


    r1,g1,b1,a1 = image.getpixel((lng_floor,lat_floor))
    r2,g2,b2,a2 = image.getpixel((lng_ceil, lat_floor))
    r3,g3,b3,a3 = image.getpixel((lng_ceil, lat_ceil))
    r4,g4,b4,a4 = image.getpixel((lng_floor, lat_ceil))

    vx = vlongitude - lng_floor
    vy = vlatitude - lat_floor

    T_D_weight = (1 - vx) * (1 - vy) * a1 / 255.0
    T_C_weight = vx * (1 - vy) * a2 / 255.0
    T_B_weight = vx * vy * a3 / 255.0
    T_A_weight = (1 - vx) * vy  * a4 / 255.0
    total_weight =  T_D_weight + T_C_weight + T_A_weight + T_B_weight
    if total_weight < 0.7:
        return 0
    else:

        T_D = r1 / 255.0

        T_C = r2 / 255.0

        T_B = r3 / 255.0

        T_A = r4 / 255.0

        T = (T_D_weight * T_D + T_C_weight * T_C + T_A_weight * T_A + T_B_weight * T_B) / total_weight

        return T

@api3.route("/zhongkexingtu/huoshaoyun/api")
def huoshaoyun():
    result = {}

    osplat = request.args.get("os","iOS")
    if osplat == "android":
        isVip = request.args.get("isVip","0")
        if isVip =="0":
            result[x_code] = 201
            result[x_meesage] = "no result"
            return json.dumps(result)
        else:
            pass
    else:
        pass

    datenow = datetime.datetime.now(tz=shanghai_tz)
    nextday = datenow + datetime.timedelta(days=4)



    start = "%d%02d%02d00" % (datenow.year, datenow.month, datenow.day)
    end = "%d%02d%02d00" % (nextday.year, nextday.month, nextday.day)
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')

    location = lng + "," + lat

    utc_now = datetime.datetime.utcnow()
    timestamp = utc_now.timestamp()

    timespan = "&start=" + start + "&end=" + end


    url = "https://api.open.geovisearth.com/v2/grid/glow/day?meteCodes=aod,glow&level=true&token=" + xingtuyun_token + "&location=" + location + timespan

    print(url)
    try:

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        datadict = json.loads(content)

        datalist = datadict["result"]["datas"]
        resultlist = []
        for datadict1 in datalist:
            dict = {}
            startViewTime = datadict1["startViewTime"]
            dict["month"] = startViewTime[5:7]
            dict["day"] = startViewTime[8:10]
            dict["hour"] = startViewTime[11:13]
            hour = int(dict["hour"])
            if hour < 12:
                dict["type"] = 0  # 朝霞
            else:
                dict["type"] = 1  # 晚霞
            dict["value"] = datadict1["values"][0]
            dict["aod_value"] = datadict1["values"][1]
            dict["level"] = datadict1["levels"][0]
            dict["aod_level"] = datadict1["levels"][1]
            resultlist.append(dict)


        result[x_code] = 200
        result[x_data] = resultlist

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

def tile_to_latitude(y, pz):
        n = float(math.pi - 2 * math.pi * y / pz)
        latitude = float(180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
        return latitude


def tile_to_longitude(x, pz):
    longitude = float(x / pz * 360 - 180)
    return longitude



@api3.route("/zhongkexingtu/huoshaoyun/map")
def huoshaoyunmap():

    result = {}

    huoshaoyunpath = os.path.join(basedir,"static/CAMS","glow")

    localdaynow = datetime.datetime.now(tz=shanghai_tz)
    timestamp = localdaynow.timestamp()

    hour = int(timestamp / 600)


    # url = "https://tiles.geovisearth.com/meteorology/v1/view/glow/mfv/Astronomical_ph/fc_idx/range?token=" + zhongkexingtu_token

    try:

        file = "huoshaoyun_map_" + str(hour) + ".json"

        jsonpath = os.path.join(huoshaoyunpath, file)
        if os.path.exists(jsonpath):
            rf = open(jsonpath, "r")
            datadict = json.loads(rf.read())
            rf.close()
            return json.dumps(datadict)
        else:
            datalist = []
            for i in range(0,3):

                daytome = localdaynow + datetime.timedelta(days=i)
                utcyear = daytome.year
                utcmonth = daytome.month
                utcday = daytome.day
                daystr = "%d%02d%02d" % (utcyear, utcmonth, utcday)

                risepath = os.path.join(huoshaoyunpath, daystr + "_riseme.webp")

                setpath = os.path.join(huoshaoyunpath, daystr + "_setme.webp")

                if os.path.exists(risepath):
                    dict = {}

                    dict["url"] = "https://www.oulagongshi.com/api/v3.0/cams/glow/riseme/"+ daystr
                    dict["month"] = "%02d"%utcmonth
                    dict["day"] = "%02d" %utcday
                    dict["hour"] = "06"
                    dict["type"] = 0 #朝霞
                    dict["lonmin"] = 72
                    dict["lonmax"] = 136
                    dict["latmin"] = 15
                    dict["latmax"] = 55
                    dict["width"] = 1921
                    dict["height"] = 1530
                    datalist.append(dict)
                if os.path.exists(setpath):
                    dict = {}

                    dict["url"] = "https://www.oulagongshi.com/api/v3.0/cams/glow/setme/"+ daystr
                    dict["month"] = "%02d"%utcmonth
                    dict["day"] = "%02d" %utcday
                    dict["hour"] = "18"
                    dict["type"] = 1 #朝霞
                    dict["lonmin"] = 72
                    dict["lonmax"] = 136
                    dict["latmin"] = 15
                    dict["latmax"] = 55
                    dict["width"] = 1921
                    dict["height"] = 1530
                    datalist.append(dict)
            if len(datalist) > 3:
                result[x_code] = 200
                result[x_data] = datalist
                wf = open(jsonpath, "w")
                wf.write(json.dumps(result))
                wf.close()
            else:
                result[x_code] = 200
                result[x_data] = "no data"

            return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route("/zhongkexingtu/weather/map")
def zhengkexingtuweathermap():
    meteCode = request.args.get("meteCode","tcdc")


    start = request.args.get("start","2025050700")
    end = request.args.get("end","2025051200")


    result = {}


    url = "https://tiles.geovisearth.com/meteorology/v1/view/module/sevg/gfs/"+meteCode+"/range?start="+start+"&end=" + end +"&token=" + zhongkexingtu_token

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        datadict = json.loads(content)


        result[x_code] = 200
        result[x_data] = datadict["result"]["urls"]

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)



@api3.route("/zhongkexingtu/bluesky")
def bluesky():
    result = {}

    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    start = request.args.get("start","2025050300")
    end = request.args.get("end","2025050600")
    location = lat + "," + lng



    url = "https://tiles.geovisearth.com/meteorology/v1/weather/grid/glow/hour/data?location="+location+"&start="+start+"&end="+ end+"&meteCodes=aod550&level=true&token=" + zhongkexingtu_token

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        result[x_code] = 200
        result[x_data] = json.loads(content)

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route("/huoshaoyun/clear")
def huoshaoyunclear():

    bathyPath = os.path.join(basedir, 'static/huoshaoyun')


    for parent, _, fileNames in os.walk(bathyPath):
        for filename in fileNames:
            path = os.path.join(parent,filename)
            os.remove(path)

    return "done"
