#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,mapdict,x_meesage,appkey,secret
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
from app.water import water
from app.worldTidalStation import worldTidalStation
from app.chinaTidalStation import chinaTidalStation
import gzip
from app.utils.constvalue import acuuappkey,xinzhi_prinvate_key,xinzhi_public_key,openweather_key,meteobule_apikey
import metpy.calc as mpcalc
from metpy.units import units
import gzip
from io import StringIO
import requests


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


@api3.route("/china/chonglang/sea")
def chinachonglangsea():
    lat = request.args.get("lat", "22.4146")
    lng = request.args.get("lng", "114.381")

    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")

    key = request.args.get("key", "20240102_c1")

    try:

        response = requests.get(
            'http://www.astronomyobserver.net/api/v3.0/meteoblue/china/sea',
            params={
                "lat": lat,
                "lng": lng,
                "tz": tz,
                "key": key,
                "language": language

            }

        )

        json_data = response.json()
        return json.dumps(json_data)

    except Exception as e:

        result = {}
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        return json.dumps(result)


@api3.route("/mountain/sun")
def mountainsun():

    starttime = request.args.get("starttime", "1702483200")

    lat = request.args.get("lat", "30.2879")
    lng = request.args.get("lng", "119.9873")
    timezone = request.args.get("timezone", "Asia/Shanghai")
    elevation = request.args.get("elevation", json.dumps(["0", "4339", "6000", "7500", "8848"]))


    try:

        response = requests.get(
            'http://www.astronomyobserver.net/api/v3.0/mountain/sun',
            params={
                "lat":lat,
                "lng": lng,
                "timezone": timezone,
                "starttime": starttime,
                "elevation": elevation

            }

        )

        json_data = response.json()
        return json.dumps(json_data)

    except Exception as e:

        result = {}
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        return json.dumps(result)


@api3.route("/elevation/sun")
def elevationsun():
    starttime = request.args.get("starttime", "1702483200")

    lat = request.args.get("lat", "30.2879")
    lng = request.args.get("lng", "119.9873")
    timezone = request.args.get("timezone", "Asia/Shanghai")
    try:

        response = requests.get(
            'http://www.astronomyobserver.net/api/v3.0/elevation/sun',
            params={
                "lat": lat,
                "lng": lng,
                "timezone": timezone,
                "starttime": starttime,

            }

        )

        json_data = response.json()
        return json.dumps(json_data)

    except Exception as e:

        result = {}
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        return json.dumps(result)


@api3.route('/meteoblue/air')
def meteoblueair():


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz","Asia/Shanghai")
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/meteoblue/clound')
def meteoblueclound():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/meteoblue/cloud/hour')
def meteobluecloudhour():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/clouds-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        result[x_code] = 200
        result[x_data] = json.loads(content)

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route('/meteoblue/airquality')
def meteoblueairquality():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/meteoblue/solar')
def meteobluesolar():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route('/meteoblue/wind')
def meteobluewind():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route('/meteoblue/sunquality/hour')
def meteobluesunqualityhour():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    tz = request.args.get("tz", "Asia/Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/clouds-1h_airquality-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        result[x_code] = 200
        result[x_data] = json.loads(content)

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
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
        result[x_meesage] = "%s"%e
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
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/meteoblue/seamodel')
def meteobseamodel():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
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
        result[x_meesage] = "%s"%e
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
        result[x_meesage] = "%s"%e
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
        result[x_meesage] = "%s"%e
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
    except Exception as  e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
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
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
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
        print (e)
        return "hello word"