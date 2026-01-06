#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage

from flask import request

import datetime
import urllib, sys
import json
from app.utils.constvalue import meteobule_apikey

import requests
import os
from  config import  basedir
from PIL import Image
import  pytz
from astral import LocationInfo
from astral.location import Location

@api3.route("/meteoblue/icon")
def meteoblueicon():
    tpxoPath = os.path.join(basedir, 'static/meteoblue/png')
    rezippath = os.path.join(basedir, 'static/meteoblue/webp')


    for parent, _, fileNames in os.walk(tpxoPath):
        for filename in fileNames:
            if filename.find(".png") > 0 :
                imagepath = os.path.join(tpxoPath,filename)
                webpimagepath = os.path.join(rezippath,filename[:-4] + "@3x.png")
                jpeg_image = Image.open(imagepath)

                out = jpeg_image.resize((240,210),Image.ANTIALIAS)
                out.save(webpimagepath)
                jpeg_image.close()

    return "done"

@api3.route('/meteoblue/mountain/weather')
def meteobluemountainweather():


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz","Asia/Shanghai")
    asl = request.args.get("asl","12")
    key = request.args.get("key","c1_8848_20231114")


    result = {}

    url = "http://www.astronomyobserver.net/api/v3.0/meteoblue/mountain/weather?lat="+lat+"&lng="+lng+"&asl="+asl+"&format=json&tz="+tz +"&key=" + key

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        return content
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)



@api3.route('/meteoblue/china/sea')
def meteobluechianchonglang():


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz","Asia/Shanghai")
    key = request.args.get("key","c1_8848_20231114")


    result = {}

    url = "http://www.astronomyobserver.net/api/v3.0/meteoblue/china/sea?lat="+lat+"&lng="+lng+"&format=json&tz="+tz +"&key=" + key

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        return content
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)




@api3.route("/mountain/sun")
def mountainsun():

    satrttime = request.args.get("starttime","1702483200")
    timestamp = int(satrttime)

    lat = request.args.get("lat","30.2879")
    lng = request.args.get("lng","119.9873")
    timezone = request.args.get("timezone","Asia/Shanghai")
    elevation = request.args.get("elevation",json.dumps(["0","4339","6000","7500","8848"]))
    elevations = json.loads(elevation)



    city = LocationInfo(name="custom",region="China",timezone= timezone,latitude=float(lat),longitude=float(lng))
    location = Location(city)



    datalist = []

    for elev in elevations:
        dict = {}
        dict["elevation"] = elev
        list = []

        for i in range(0,8):
            try:
                dt_noon = datetime.datetime.fromtimestamp(timestamp + 12 * 3600 + 24 * i * 3600, tz=pytz.timezone(timezone))

                astrodict = {}
                sunrise = location.sunrise(date=dt_noon,observer_elevation= float(elev))
                sunset = location.sunset(date=dt_noon,observer_elevation= float(elev))
                astrodict["sunrise"] = "%02d:%02d:%02d" % (sunrise.hour,sunrise.minute,int(sunrise.second))
                astrodict["sunset"] =  "%02d:%02d:%02d" % (sunset.hour,sunset.minute, int(sunset.second))
                astrodict["day"] = "%d-%02d-%02d" % (dt_noon.year,dt_noon.month, dt_noon.day)
                list.append(astrodict)
            except Exception as e:
                print(e)
        dict["sun"] = list
        datalist.append(dict)

    result = {}
    result[x_code] = 200
    result[x_data]  = datalist


    return json.dumps(result)


@api3.route("/elevation/sun")
def elevationsun():

    satrttime = request.args.get("starttime","1702483200")
    timestamp = int(satrttime)

    lat = request.args.get("lat","30.2879")
    lng = request.args.get("lng","119.9873")
    timezone = request.args.get("timezone","Asia/Shanghai")
    elevations = []
    for j in range(0,10):
        elevations.append(j * 1000)



    city = LocationInfo(name="custom",region="China",timezone= timezone,latitude=float(lat),longitude=float(lng))
    location = Location(city)



    datalist = []

    for elev in elevations:
        dict = {}
        dict["elevation"] = elev

        try:
            dt_noon = datetime.datetime.fromtimestamp(timestamp + 12 * 3600 , tz=pytz.timezone(timezone))

            sunrise = location.sunrise(date=dt_noon, observer_elevation=float(elev))
            sunset = location.sunset(date=dt_noon, observer_elevation=float(elev))
            dict["sunrise"] = "%02d:%02d:%02d" % (sunrise.hour, sunrise.minute, int(sunrise.second))
            dict["sunset"] = "%02d:%02d:%02d" % (sunset.hour, sunset.minute, int(sunset.second))
            dict["day"] = "%d-%02d-%02d" % (dt_noon.year, dt_noon.month, dt_noon.day)
        except Exception as e:
            print(e)
        datalist.append(dict)

    result = {}
    result[x_code] = 200
    result[x_data]  = datalist


    return json.dumps(result)

#
# @api3.route('/meteoblue/china/sea')
# def meteobluechianchonglang():
#
#     lat = request.args.get('lat', '30')
#     lng = request.args.get('lng', '120')
#     total = request.args.get('total', '1599918717')
#     language = request.args.get("language", "zh_cn")
#     tz = request.args.get("tz","Asia/Shanghai")
#
#
#     key = request.args.get("key")
#
#
#     result = {}
#
#     meteobluePath = os.path.join(basedir, 'static/meteoblue/seachina',key)
#
#     url = "http://my.meteoblue.com/packages/sea-1h_sea-day?apikey="+meteobule_apikey+"&lat="+lat+"&lon="+lng+"&format=json&tz="+tz
#
#     try:
#
#         if os.path.exists(meteobluePath):
#             try:
#                 f = open(meteobluePath,"r")
#                 jdata = f.read()
#                 f.close()
#                 return jdata
#             except Exception as e:
#
#                 result[x_code] = 201
#                 result[x_meesage] = "file error"
#                 return json.dumps(result)
#         else:
#             req = urllib.request.Request(url)
#             response = urllib.request.urlopen(req)
#             content = response.read()
#
#             result[x_code] = 200
#             result[x_data] = json.loads(content)
#
#             try:
#
#                 jdata = json.dumps(result)
#                 fw = open(meteobluePath, "w")
#                 fw.write(jdata)
#                 fw.close()
#             except Exception as e:
#                 print(e)
#
#
#             return json.dumps(result)
#     except Exception as e:
#         result[x_code] = 201
#         result[x_meesage] = "%s" % e
#         return json.dumps(result)


@api3.route('/meteoblue/air')
def meteoblueair():

    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz","Asia,Shanghai")
    asl = request.args.get("asl","12")


    result = {}

    url = "https://my.meteoblue.com/packages/air-1h_air-day?apikey="+meteobule_apikey+"&lat="+lat+"&lon="+lng+"&asl="+asl+"&format=json&tz="+tz

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


@api3.route('/meteoblue/clound')
def meteoblueclound():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia,Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/clouds-1h_clouds-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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



@api3.route('/meteoblue/sea')
def meteobluesea():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '123')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/sea-1h_sea-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz


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

@api3.route('/meteoblue/airquality')
def meteoblueairquality():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia,Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/airquality-1h_airquality-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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


@api3.route('/meteoblue/solar')
def meteobluesolar():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia,Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/solar-1h_solar-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

@api3.route('/meteoblue/wind')
def meteobluewind():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia,Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/wind-1h_wind-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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


@api3.route('/meteoblue/windpower')
def meteobluewindpower():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia,Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/wind-1h_wind-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

@api3.route('/meteoblue/argo')
def meteoblueargo():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/agro-1h_agro-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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


@api3.route('/meteoblue/argomodel')
def meteoblueargomodel():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")

    result = {}

    url = "https://my.meteoblue.com/packages/agromodelleafwetness-1h_agromodelspray-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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


@api3.route('/meteoblue/seamodel')
def meteobseamodel():
    lat = request.args.get('lat', '18.6321')
    lng = request.args.get('lng', '110.2189')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")

    result = {}

    url = "https://my.meteoblue.com/packages/sea-1h_sea-day?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

@api3.route('/meteoblue/profile/temprature')
def meteoblueprotemprature():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")

    result = {}

    url = "http://my.meteoblue.com/packages/profiletemp-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

@api3.route('/meteoblue/profile/wind')
def meteoblueprowind():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")

    result = {}

    url = "http://my.meteoblue.com/packages/profilewind-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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


@api3.route('/meteoblue/profile/cloud')
def meteoblueprocloud():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")

    result = {}

    url = "http://my.meteoblue.com/packages/profilecloud-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

@api3.route('/meteoblue/profile/rh')
def meteoblueprorh():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")

    result = {}

    url = "http://my.meteoblue.com/packages/profilerh-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        result[x_code] = 200
        result[x_data] = json.loads(content)

        return json.dumps(result)
    except Exception as  e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)



@api3.route("/meteoblue/profile/height")
def meteoblueproheight():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "0")
    try:
        response = requests.get(
            'http://my.meteoblue.com/packages/profileheight-1h',
            params={
                "lat":lat,
                "lon":lng,
                "apikey":meteobule_apikey,
                "asl":asl,
                "tz":tz,
                "format":"json"
            },

        )


        # print  response

        # Do something with response data.
        json_data = response.json()
        return json.dumps(json_data)
    except Exception as e:
        return "hello word"

