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


@api3.route("/zhongkexingtu/huoshaoyun/old")
def huoshaoyunold():
    result = {}


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    start = request.args.get("start","2025050400")
    end = request.args.get("end","2025050700")
    location = lat + "," + lng



    huoshaoyunpath = os.path.join(basedir,"static/huoshaoyun")

    utc_now = datetime.datetime.utcnow()
    timestamp = utc_now.timestamp()

    hour = int(timestamp / 600)

    url = "https://tiles.geovisearth.com/meteorology/v1/view/glow/sev/Astronomical_ph/fc_idx/range?token=" + zhongkexingtu_token

    try:
        file = "huoshaoyun_red_" + str(hour) + ".json"
        jsonpath = os.path.join(huoshaoyunpath,file)
        if os.path.exists(jsonpath):
            rf = open(jsonpath,"r")
            datadict = json.loads(rf.read())
            rf.close()

        else:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read()
            datadict = json.loads(content)
            wf = open(jsonpath,"w")
            wf.write(json.dumps(datadict))
            wf.close()

        urls = datadict["result"]["urls"]
        datalist = []
        for key in urls.keys():
            dict = {}
            urllist = urls[key]
            dicturl = urllist[0]

            ulrslips = dicturl.split("/")

            pngname = ulrslips[len(ulrslips) -1]
            dictjson = urllist[1]
            jsonslips = dictjson.split("/")
            jsonname = jsonslips[len(jsonslips) - 1]

            pngpath = os.path.join(huoshaoyunpath,pngname)
            jsonpath = os.path.join(huoshaoyunpath,jsonname)
            if os.path.exists(pngpath):
                pass
            else:
                try:
                    r = requests.get(dicturl, stream=True)
                    if r.status_code != 200:
                        print("faile:" + dict["url"])
                    else:
                        f = open(str(pngpath), "wb")
                        shutil.copyfileobj(r.raw, f, length=16 * 1024 * 1024)
                except Exception as e:
                    print(e)

            if os.path.exists(jsonpath):
                pass
            else:
                try:
                    jreq = urllib.request.Request(dictjson)
                    jresponse = urllib.request.urlopen(jreq)
                    jcontent = json.loads(jresponse.read())
                    wf = open(jsonpath,"w")
                    wf.write(json.dumps(jcontent))
                    wf.close()
                except Exception as e:
                    print(e)


            dict["month"] = key[4:6]
            dict["day"] = key[6:8]
            dict["hour"] = key[8:10]
            if dict["hour"] == "08":
                dict["type"] = 0 #朝霞
            else:
                dict["type"] = 1 #晚霞

            if os.path.exists(jsonpath) and os.path.exists(pngpath):
                jf = open(jsonpath,"r")
                configdict = json.loads(jf.read())
                jf.close()
                min_v = configdict["min"]
                max_v = configdict["max"]
                pngwidth = configdict["width"]
                pngheight = configdict["height"]
                lat_min = configdict["latmin"]
                lat_max = configdict["latmax"]
                lon_min = configdict["lonmin"]
                lon_max = configdict["lonmax"]

                lon_width = (float(lng) - lon_min) / (lon_max - lon_min) * (pngwidth - 1)
                lat_height = (lat_max - float(lat)) / (lat_max - lat_min) * (pngheight - 1)

                if lon_width < 0 or lon_width > pngwidth - 1 - 0.0001:
                    continue
                if lat_height < 0 or lat_height > pngheight - 1 - 0.0001:
                    continue

                image = Image.open(pngpath).convert('RGB')

                r1, g1, b1 = image.getpixel((math.floor(lon_width), math.floor(lat_height)))
                r2, g2, b2 = image.getpixel((math.ceil(lon_width), math.floor(lat_height)))
                r3, g3, b3 = image.getpixel((math.ceil(lon_width), math.ceil(lat_height)))
                r4, g4, b4 = image.getpixel((math.floor(lon_width), math.ceil(lat_height)))



                x = lon_width - math.floor(lon_width)
                y = lat_height - math.floor(lat_height)


                T_D = min_v + r1 / 255.0 * (max_v - min_v)
                T_C = min_v + r2 / 255.0 * (max_v - min_v)
                T_B = min_v + r3 / 255.0 * (max_v - min_v)
                T_A = min_v + r4 / 255.0 * (max_v - min_v)

                # print(T_A)
                # print(T_B)
                # print(T_C)
                # print(T_D)

                T = (1 - x) * (1 - y) * T_D + \
                    x * (1 - y) * T_C + \
                    (1 - x) * y * T_A + \
                    x * y * T_B

                # print(T)

                dict["value"] = T

                level  = 0
                fix  = 0.00001
                if T < 0.018  + fix:
                    level = 0
                elif T < 0.075 + fix:
                    level = 1
                elif T < 0.151 + fix:
                    level =  2
                elif T < 0.438 + fix:
                    level =  3
                elif T < 0.711 + fix:
                    level = 4
                else:
                    level = 5
                dict["level"] = level





                datalist.append(dict)
                image.close()




        result[x_code] = 200
        result[x_data] = datalist

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route("/zhongkexingtu/huoshaoyun")
def huoshaoyun():
    result = {}


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

    huoshaoyunpath = os.path.join(basedir,"static/huoshaoyun")

    utc_now = datetime.datetime.utcnow()
    timestamp = utc_now.timestamp()

    hour = int(timestamp / 600)


    url = "https://tiles.geovisearth.com/meteorology/v1/view/glow/mfv/Astronomical_ph/fc_idx/range?token=" + zhongkexingtu_token

    try:

        file = "huoshaoyun_map_" + str(hour) + ".json"

        jsonpath = os.path.join(huoshaoyunpath, file)
        if os.path.exists(jsonpath):
            rf = open(jsonpath, "r")
            datadict = json.loads(rf.read())
            rf.close()
            return json.dumps(datadict)
        else:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read()

            datadict = json.loads(content)

            urls = datadict["result"]["urls"]
            datalist = []
            for key in urls.keys():
                dict = {}
                urllist = urls[key]
                dict["url"] = urllist[0]
                dict["month"] = key[4:6]
                dict["day"] = key[6:8]
                dict["hour"] = key[8:10]
                if dict["hour"] == "08":
                    dict["type"] = 0 #朝霞
                else:
                    dict["type"] = 1 #晚霞

                dict["lonmin"] = 71.99999698166064
                dict["lonmax"] = 135.95106206703144
                dict["latmin"] = 15.000006383081164
                dict["latmax"] = 54.97079910511656
                dict["width"] = 2374
                dict["height"] = 1890
                datalist.append(dict)


            result[x_code] = 200
            result[x_data] = datalist
            wf = open(jsonpath, "w")
            wf.write(json.dumps(result))
            wf.close()

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
