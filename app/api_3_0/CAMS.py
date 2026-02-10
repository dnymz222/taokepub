import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage

from flask import request
import json
from config import basedir
import requests
import shutil
import datetime
import pytz
from PIL.ImageFile import ImageFile as ImageReadFile
from PIL import Image
import math


@api3.route("/cams/riseset/map")
def camsrisesetmap():

    result = {}

    timezone = request.args.get("timezone","Asia/Shanghai")

    shanghai_tz = pytz.timezone(timezone)
    huoshaoyunpath = os.path.join(basedir,"static/CAMS","riseset")

    localdaynow = datetime.datetime.now(tz=shanghai_tz)
    timestamp = localdaynow.timestamp()

    hour = int(timestamp / 600)

    try:

        file = "riseset_map_" + str(hour) + ".json"

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

                risepath = os.path.join(huoshaoyunpath, daystr + "_worldrise.webp")

                setpath = os.path.join(huoshaoyunpath, daystr + "_worldset.webp")

                if os.path.exists(risepath):
                    dict = {}

                    dict["url"] = "https://www.oulagongshi.com/api/v3.0/cams/riseset/worldrise/"+ daystr
                    dict["month"] = utcmonth
                    dict["day"] = utcday
                    dict["hour"] = 6
                    dict["type"] = 0 #日出
                    dict["group"] = 0
                    dict["lonmin"] = 72
                    dict["lonmax"] = 136
                    dict["latmin"] = 15
                    dict["latmax"] = 55
                    dict["width"] = 769
                    dict["height"] = 481
                    datalist.append(dict)
                if os.path.exists(setpath):
                    dict = {}

                    dict["url"] = "https://www.oulagongshi.com/api/v3.0/cams/riseset/worldset/"+ daystr
                    dict["month"] = utcmonth
                    dict["day"] = utcday
                    dict["hour"] = 18
                    dict["type"] = 1 # 日落
                    dict["group"] = 0
                    dict["lonmin"] = 72
                    dict["lonmax"] = 136
                    dict["latmin"] = 15
                    dict["latmax"] = 55
                    dict["width"] = 769
                    dict["height"] = 481
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


@api3.route("/cams/glow/map")
def camsglowmap():

    result = {}

    timezone = request.args.get("timezone","Asia/Shanghai")

    shanghai_tz = pytz.timezone(timezone)
    huoshaoyunpath = os.path.join(basedir,"static/CAMS","glow")

    localdaynow = datetime.datetime.now(tz=shanghai_tz)
    timestamp = localdaynow.timestamp()

    hour = int(timestamp / 600)

    try:

        file = "glow_map_" + str(hour) + ".json"

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

                risepath = os.path.join(huoshaoyunpath, daystr + "_worldrise.webp")

                setpath = os.path.join(huoshaoyunpath, daystr + "_worldset.webp")

                if os.path.exists(risepath):
                    dict = {}

                    dict["url"] = "https://www.oulagongshi.com/api/v3.0/cams/glow/worldrise/"+ daystr
                    dict["month"] = utcmonth
                    dict["day"] = utcday
                    dict["hour"] =  6
                    dict["type"] = 0 #日出
                    dict["group"] = 1
                    dict["lonmin"] = 72
                    dict["lonmax"] = 136
                    dict["latmin"] = 15
                    dict["latmax"] = 55
                    dict["width"] = 769
                    dict["height"] = 481
                    datalist.append(dict)
                if os.path.exists(setpath):
                    dict = {}

                    dict["url"] = "https://www.oulagongshi.com/api/v3.0/cams/glow/worldset/"+ daystr
                    dict["month"] = utcmonth
                    dict["day"] =  utcday
                    dict["hour"] = 18
                    dict["type"] = 1 # 日落
                    dict["group"] = 1
                    dict["lonmin"] = 72
                    dict["lonmax"] = 136
                    dict["latmin"] = 15
                    dict["latmax"] = 55
                    dict["width"] = 769
                    dict["height"] = 481
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



@api3.route("/cams/sun/forecast")
def camssunforecast():
    result = {}


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    start = request.args.get("start","2025050400")
    end = request.args.get("end","2025050700")

    timezone = request.args.get("timezone","Asia/Shanghai")
    shanghai_tz = pytz.timezone(timezone)

    location = lat + "," + lng

    latf = float(lat)
    lngf = float(lng)

    if lngf < 0:
        lngf  = lngf + 360

    if latf > 55 or latf < 15:
        result[x_code] = 201
        result[x_meesage] = "out boundry"
        return json.dumps(result)

    if lngf > 136 or lngf < 72:
        result[x_code] = 201
        result[x_meesage] = "out boundry"
        return json.dumps(result)





    glowdatalist = []

    vlongitude = (lngf - 72) * 12
    vlatitude = (55 - latf) * 12

    datadict = {}



    huoshaoyunpath = os.path.join(basedir,"static/CAMS","glow")

    localdaynow = datetime.datetime.now(tz=shanghai_tz)

    for i in range(0,3):
        daytome = localdaynow + datetime.timedelta(days=i)
        utcyear = daytome.year
        utcmonth = daytome.month
        utcday = daytome.day

        daystr = "%d%02d%02d" % (utcyear, utcmonth, utcday)


        risepath = os.path.join(huoshaoyunpath, daystr + "_rise.webp")

        setpath = os.path.join(huoshaoyunpath, daystr + "_set.webp")


        if os.path.exists(risepath):
            try:
                dict = {}
                riseimage = Image.open(risepath)
                Tsunrise = getGlowValue(riseimage, vlongitude, vlatitude)
                dict["month"] = utcmonth
                dict["day"] =  utcday
                dict["hour"] = 6
                dict["value"] = Tsunrise
                dict["level"] = getGlowType(Tsunrise)
                dict["type"] = 0
                dict["group"] = 0

                glowdatalist.append(dict)
                riseimage.close()
            except Exception as e:
                print(e)


        else:
            pass



        if os.path.exists(setpath):

            try:

                dict = {}
                setimage = Image.open(setpath)
                Tsunset = getGlowValue(setimage, vlongitude, vlatitude)
                dict["month"] =  utcmonth
                dict["day"] =  utcday
                dict["hour"] = 18
                dict["value"] = Tsunset
                dict["level"] = getGlowType(Tsunset)
                dict["type"] = 1
                dict["group"] = 0

                glowdatalist.append(dict)
                setimage.close()
            except Exception as e:
                print(e)
        else:
            pass


    if len(glowdatalist) > 0:
        datadict["glow"] = glowdatalist

    risesetpath = os.path.join(basedir, "static/CAMS", "riseset")

    risesetlist = []

    for i in range(0, 3):
        daytome = localdaynow + datetime.timedelta(days=i)
        utcyear = daytome.year
        utcmonth = daytome.month
        utcday = daytome.day

        daystr = "%d%02d%02d" % (utcyear, utcmonth, utcday)

        risepath = os.path.join(risesetpath, daystr + "_rise.webp")

        setpath = os.path.join(risesetpath, daystr + "_set.webp")

        if os.path.exists(risepath):
            try:
                dict = {}
                riseimage = Image.open(risepath)
                Tsunrise = getGlowValue(riseimage, vlongitude, vlatitude)
                dict["month"] = utcmonth
                dict["day"] =   utcday
                dict["hour"] = 6
                dict["value"] = Tsunrise
                dict["level"] = getSunrisesetType(Tsunrise)
                dict["type"] = 0
                dict["group"] = 0

                risesetlist.append(dict)
                riseimage.close()
            except Exception as e:
                print(e)


        else:
            pass

        if os.path.exists(setpath):

            try:

                dict = {}
                setimage = Image.open(setpath)
                Tsunset = getGlowValue(setimage, vlongitude, vlatitude)
                dict["month"] = utcmonth
                dict["day"] = utcday
                dict["hour"] = 18
                dict["value"] = Tsunset
                dict["level"] = getSunrisesetType(Tsunset)
                dict["type"] = 1
                dict["group"] = 0

                risesetlist.append(dict)
                setimage.close()
            except Exception as e:
                print(e)
        else:
            pass

    if len(risesetlist) > 0:
        datadict["riseset"] = glowdatalist

    if len(glowdatalist) > 0 and len(risesetlist) > 0:
        result[x_code] = 200
        result[x_data] = datadict
    else:
        result[x_code] = 201
        result[x_meesage] = "no data"

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

def getSunrisesetType(value):
    if value < 0.01:
        return 0
    elif value < 0.2:
        return 1
    elif value < 0.4:
        return 2
    elif value < 0.6:
        return 3
    elif value < 0.8:
        return 4
    else:
        return 5

def getGlowValue(image:ImageReadFile,vlongitude:float,vlatitude:float):
    lng_floor = int(math.floor(vlongitude))
    lat_floor = int(math.floor(vlatitude))
    lat_ceil = int(math.ceil(vlatitude))
    lng_ceil = int(math.ceil(vlongitude))
    if lat_ceil > 732:
        lat_ceil = 732
    if lng_ceil > 2159:
        lng_ceil = 0


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
    total_weight = T_D_weight + T_C_weight + T_A_weight + T_B_weight
    if total_weight < 0.7:
        return 0
    else:

        T_D = r1 / 255.0

        T_C = r2 / 255.0

        T_B = r3 / 255.0

        T_A = r4 / 255.0

        T = (T_D_weight * T_D + T_C_weight * T_C + T_A_weight * T_A + T_B_weight * T_B) / total_weight

        return T
