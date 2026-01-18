#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage

from flask import request

import urllib


import json

from app.utils.constvalue import meteoblue_allapi_key

import requests
import  datetime
import pytz
from PIL import Image,ImageDraw, ImageFont
import os
import shutil
from  config import  basedir
from astral import LocationInfo

from astral.location import Location
from flask import send_file

shanghai_tz = pytz.timezone("Asia/Shanghai")


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

    url = "https://my.meteoblue.com/packages/air-1h_air-day?apikey="+meteoblue_allapi_key+"&lat="+lat+"&lon="+lng+"&asl="+asl+"&format=json&tz="+tz

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

    url = "https://my.meteoblue.com/packages/clouds-1h_clouds-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/clouds-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/sea-1h_sea-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz


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

    url = "https://my.meteoblue.com/packages/airquality-1h_airquality-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/solar-1h_solar-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/wind-1h_wind-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/clouds-1h_airquality-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/agro-1h_agro-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/agromodelleafwetness-1h_agromodelspray-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "https://my.meteoblue.com/packages/sea-1h_sea-day?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "http://my.meteoblue.com/packages/profiletemp-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "http://my.meteoblue.com/packages/profilewind-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "http://my.meteoblue.com/packages/profilecloud-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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

    url = "http://my.meteoblue.com/packages/profilerh-1h?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

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
                "apikey":meteoblue_allapi_key,
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

@api3.route("/mountain/yunhai")
def mountainyunhai():
    mountainlist = [
        {
                "timezone": "Asia/Shanghai", "height": "1864", "latitude": "30.12745", "longitude": "118.16598",
                "elevations": ["176", "1000", "1864"], "name": "莲花峰 / 黄山", "source": 1, "mountainId": "C392"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1820", "latitude": "28.90915", "longitude": "118.05782",
            "elevations": ["84", "1000", "1820"], "name": "玉京峰 / 三清山", "source": 1, "mountainId": "C350"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1557", "latitude": "30.17559", "longitude": "118.89967",
            "elevations": ["24", "1000", "1557"], "name": "太子尖", "source": 1, "mountainId": "C327"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1918", "latitude": "27.45523", "longitude": "114.17324",
            "elevations": ["123", "1000", "1918"], "name": "金顶/武功山", "source": 1, "mountainId": "C329"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2494", "latitude": "27.91937", "longitude": "108.69217",
            "elevations": ["486", "1500", "2494"], "name": "梵净山老金顶", "source": 1, "mountainId": "C896"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1533", "latitude": "36.25703", "longitude": "117.10305",
            "elevations": ["185", "1000", "1533"], "name": "玉皇顶 / 泰山", "source": 1, "mountainId": "C474"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1612", "latitude": "32.401", "longitude": "111.0047",
            "elevations": ["118", "1612"], "name": "武当山", "source": 1, "mountainId": "C2017"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "3099", "latitude": "29.51035", "longitude": "103.33187",
            "elevations": ["437", "1500", "3099"], "name": "峨眉山", "source": 1, "mountainId": "C235"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "3660", "latitude": "29.77518", "longitude": "102.3738",
            "elevations": ["765", "2000", "3660"], "name": "牛背山", "source": 1, "mountainId": "C239"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2303", "latitude": "40.03071", "longitude": "115.45402",
            "elevations": ["124", "1500", "2303"], "name": "东灵山", "source": 1, "mountainId": "C35"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1519", "latitude": "29.04988", "longitude": "110.47889",
            "elevations": ["161", "1000", "1519"], "name": "天门山", "source": 1, "mountainId": "C631"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "3767", "latitude": "33.95512", "longitude": "107.76528",
            "elevations": ["1565", "3000", "3767"], "name": "拔仙台 / 太白山", "source": 1, "mountainId": "C38"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2200", "latitude": "33.7183", "longitude": "111.64",
            "elevations": ["779", "2200"], "name": "老君山", "source": 1, "mountainId": "C2018"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1492", "latitude": "34.51104", "longitude": "113.04073",
            "elevations": ["402", "1492"], "name": "峻极峰 / 嵩山", "source": 1, "mountainId": "C650"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "3061", "latitude": "39.07985", "longitude": "113.56713",
            "elevations": ["1058", "2500", "3061"], "name": "叶斗峰 / 五台山", "source": 1, "mountainId": "C37"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2016", "latitude": "39.67166", "longitude": "113.72596",
            "elevations": ["1088", "2016"], "name": "天峰岭 / 恒山", "source": 1, "mountainId": "C649"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2508", "latitude": "24.93775", "longitude": "102.6372",
            "elevations": ["1910", "2508"], "name": "西山", "source": 1, "mountainId": "C1155"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2161", "latitude": "27.85969", "longitude": "117.78331",
            "elevations": ["42", "1500", "2161"], "name": "黄岗山 / 武夷山", "source": 1, "mountainId": "C386"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1587", "latitude": "30.38351", "longitude": "119.39852",
            "elevations": ["2", "1000", "1587"], "name": "龙王山", "source": 1, "mountainId": "C331"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1474", "latitude": "29.50095", "longitude": "115.9565",
            "elevations": ["41", "1474"], "name": "汉阳峰 / 庐山", "source": 1, "mountainId": "C460"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2604", "latitude": "33.9244", "longitude": "109.0455",
            "elevations": ["1072", "2000", "2604"], "name": "翠华山", "source": 1, "mountainId": "C2034"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2161", "latitude": "34.47776", "longitude": "110.07808",
            "elevations": ["358", "2161"], "name": "华山南峰", "source": 1, "mountainId": "C647"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1867", "latitude": "18.89944", "longitude": "109.7048",
            "elevations": ["244", "1000", "1867"], "name": "五指山主峰", "source": 1, "mountainId": "C520"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1296", "latitude": "23.28308", "longitude": "114.01649",
            "elevations": ["17", "1296"], "name": "飞云顶 / 罗浮山", "source": 1, "mountainId": "C828"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2736", "latitude": "38.7387", "longitude": "111.9277",
            "elevations": ["1458", "2736"], "name": "芦芽山", "source": 1, "mountainId": "C2031"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1300", "latitude": "27.29722", "longitude": "112.6897",
            "elevations": ["96", "1300"], "name": "祝融峰 / 衡山", "source": 1, "mountainId": "C648"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1229", "latitude": "28.9579", "longitude": "120.8381",
            "elevations": ["12", "1229"], "name": "大雷山", "source": 1, "mountainId": "C703"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1382", "latitude": "28.81", "longitude": "120.92207",
            "elevations": ["12", "1382"], "name": "米筛浪 / 括苍山", "source": 1, "mountainId": "C357"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1195", "latitude": "29.4806", "longitude": "120.43859",
            "elevations": ["85", "1195"], "name": "太白峰", "source": 1, "mountainId": "C356"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2691", "latitude": "42.01618", "longitude": "128.03273",
            "elevations": ["420", "1500", "2691"], "name": "白云峰", "source": 1, "mountainId": "C41"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1529", "latitude": "51.29725", "longitude": "123.12802",
            "elevations": ["544", "1529"], "name": "大白山", "source": 1, "mountainId": "C846"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1337", "latitude": "41.2934", "longitude": "126.1144",
            "elevations": ["179", "1337"], "name": "五女峰", "source": 1, "mountainId": "C2053"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "3326", "latitude": "33.8277", "longitude": "104.1078",
            "elevations": ["1652", "2500", "3326"], "name": "拉尕山", "source": 1, "mountainId": "C2065"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "2123", "latitude": "35.5371", "longitude": "106.4716",
            "elevations": ["1369", "2123"], "name": "崆峒山", "source": 1, "mountainId": "C2062"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1320", "latitude": "31.0974", "longitude": "115.2401",
            "elevations": ["42", "1320"], "name": "龟峰山", "source": 1, "mountainId": "C2042"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "3106", "latitude": "31.4401", "longitude": "110.3073",
            "elevations": ["924", "2000", "3106"], "name": "神农顶", "source": 1, "mountainId": "C32"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1364", "latitude": "27.91721", "longitude": "117.02053",
            "elevations": ["88", "1364"], "name": "笔架峰 / 龙虎山", "source": 1, "mountainId": "C854"
        }
        ,
        {
            "timezone": "Asia/Shanghai", "height": "1496", "latitude": "28.57855", "longitude": "117.7914",
            "elevations": ["77", "1496"], "name": "天梯峰 / 灵山", "source": 1, "mountainId": "C857"
        }
        ,
        {
            "source": 1, "mountainId": "C360", "elevations": ["176", "1000", "1501"], "latitude": "28.47009",
            "timezone": "Asia/Shanghai", "height": "1501", "name": "大洋山", "longitude": "120.29553"
        }
        ,
        {
            "source": 1, "mountainId": "C450", "elevations": ["24", "1479"], "latitude": "30.36301",
            "timezone": "Asia/Shanghai", "height": "1479", "name": "东天目山", "longitude": "119.5131"
        }
        ,
        {
            "source": 1, "mountainId": "C394", "elevations": ["20", "1490"], "latitude": "30.74483",
            "timezone": "Asia/Shanghai", "height": "1490", "name": "天柱峰 / 安徽天柱山", "longitude": "116.45058"
        }
        ,
        {
            "source": 1, "mountainId": "C890", "elevations": ["24", "1133"], "latitude": "36.17529",
            "timezone": "Asia/Shanghai", "height": "1133", "name": "崂山", "longitude": "120.62617"
        }
        ,
        {
            "source": 1, "mountainId": "C1233", "elevations": ["160", "1156"], "latitude": "35.5588",
            "timezone": "Asia/Shanghai", "height": "1156", "name": "龟蒙顶 / 蒙山", "longitude": "117.8929"
        }
        ,
        {
            "source": 1, "mountainId": "C1235", "elevations": ["94", "1032"], "latitude": "36.1993",
            "timezone": "Asia/Shanghai", "height": "1032", "name": "玉皇顶  / 沂山", "longitude": "118.6211"
        }
        ,
        {
            "latitude": "39.21019", "name": "白石山", "mountainId": "C1221", "height": "2096", "longitude": "114.69574",
            "elevations": ["840", "2096"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "37.4401", "name": "黄庵垴", "mountainId": "C2020", "height": "1774", "longitude": "114.0228",
            "elevations": ["115", "1000", "1774"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "33.6396", "name": "洛阳白云山", "mountainId": "C2021", "height": "2216", "longitude": "111.8271",
            "elevations": ["361", "1500", "2216"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "35.1993", "name": "王屋山", "mountainId": "C2024", "height": "1715", "longitude": "112.2712",
            "elevations": ["162", "1000", "1715"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "35.6757", "name": "王莽岭", "mountainId": "C2026", "height": "1665", "longitude": "113.613",
            "elevations": ["1312", "1665"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "33.99", "name": "南五台", "mountainId": "C2033", "height": "1688", "longitude": "108.9747",
            "elevations": ["441", "1688"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "34.7988", "name": "五老峰", "mountainId": "C2028", "height": "1809", "longitude": "110.5901",
            "elevations": ["355", "1809"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "24.8539", "name": "那色峰", "mountainId": "C2080", "height": "1702", "longitude": "104.5923",
            "elevations": ["1294", "1702"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "25.649", "name": "马龙峰 / 苍山", "mountainId": "C2081", "height": "4122", "longitude": "100.098",
            "elevations": ["1533", "3000", "4122"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "29.0344", "name": "金佛山", "mountainId": "C2048", "height": "2238", "longitude": "107.1926",
            "elevations": ["523", "1500", "2238"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "24.92786", "name": "石坑崆", "mountainId": "C395", "height": "1902", "longitude": "112.99098",
            "elevations": ["56", "1000", "1902"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "25.7124", "name": "九仙山", "mountainId": "C2057", "height": "1658", "longitude": "118.1632",
            "elevations": ["518", "1658"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "27.71441", "name": "白云尖", "mountainId": "C664", "height": "1611", "longitude": "119.64293",
            "elevations": ["227", "1000", "1611"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "40.07923", "name": "阳台山", "mountainId": "C341", "height": "1276", "longitude": "116.04681",
            "elevations": ["124", "1276"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "40.575", "name": "海坨山", "mountainId": "C2001", "height": "2241", "longitude": "115.8184",
            "elevations": ["474", "1500", "2241"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "40.59826", "name": "雾灵山", "mountainId": "C382", "height": "2118", "longitude": "117.48115",
            "elevations": ["603", "2118"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "27.60445", "name": "太平山 / 明月山", "mountainId": "C934", "height": "1736", "longitude": "114.29168",
            "elevations": ["63", "1000", "1736"], "timezone": "Asia/Shanghai", "source": 1
        }
        ,
        {
            "latitude": "30.46362", "name": "十王峰 / 九华山", "mountainId": "C766", "height": "1344", "longitude": "117.818",
            "elevations": ["2", "1344"], "timezone": "Asia/Shanghai", "source": 1
        },
        {
            "latitude": "26.3684", "name": "舜皇山", "mountainId": "C2222", "height": "1882", "longitude": "111.0098",
            "elevations": ["315","1000","1882"], "timezone": "Asia/Shanghai", "source": 1
        },
        {
            "mountainId": "C234", "longitude": "103.55896", "timezone": "Asia/Shanghai", "height": "1260", "source": 1,
            "name": "青城山", "latitude": "30.91073", "elevations": ["742", "1260"]
            }
            ,
            {
                "mountainId": "C709", "longitude": "121.05029", "timezone": "Asia/Shanghai", "height": "1107", "source": 1,
                "name": "百岗尖 / 雁荡山", "latitude": "28.36969", "elevations": ["6", "1107"]
            }
            ,
            {
                "mountainId": "C398", "longitude": "114.9505", "timezone": "Asia/Shanghai", "height": "1794", "source": 1,
                "name": "九岭尖", "latitude": "28.88166", "elevations": ["49", "1000", "1794"]
            }
            ,
            {
                "latitude": "28.43977", "name": "七星岭", "elevations": ["84", "1000", "1608"], "source": 1,
                "timezone": "Asia/Shanghai", "height": "1608", "longitude": "114.16517", "mountainId": "C863"
            }
            ,
            {
                "latitude": "29.36002", "name": "老鸦尖 / 九宫山", "elevations": ["116", "1000", "1657"], "source": 1,
                "timezone": "Asia/Shanghai", "height": "1657", "longitude": "114.59498", "mountainId": "C753"
            }
    ]

    result = {}
    result[x_code] = 200
    result[x_data] = mountainlist
    print(len(mountainlist))
    return json.dumps(result)

@api3.route("/mountain/weather/image/clear")
def mountainweatherimageclear():

    now = datetime.datetime.now(tz=shanghai_tz)

    for i  in range(1,30):

        lastday = now - datetime.timedelta(days=i)

        date = "%d%02d%02d" % (lastday.year, lastday.month, lastday.day)

        dirpath = os.path.join(basedir,"static/meteoblue/weather",date)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        else:
            pass
    return "done"

@api3.route("/mountain/weather/image")
def mountainweatherimage():



    now = datetime.datetime.now(tz=shanghai_tz)


    date = "%d%02d%02d" % (now.year, now.month, now.day)

    todaynoon = datetime.datetime(year=now.year,month=now.month,day=now.day,hour=12)


    dirpath = os.path.join(basedir,"static/meteoblue/weather",date)
    if os.path.exists(dirpath):
        pass
    else:
        os.mkdir(dirpath)
    i = 0

    scale = 1

    font_path = os.path.join(basedir, "static/meteoblue/PingFangSC-Medium.ttf")
    font = ImageFont.truetype(font_path, 50 * scale)

    font_path1 = os.path.join(basedir, "static/meteoblue/PingFangSC-Regular.ttf")
    font1 = ImageFont.truetype(font_path1, 30 * scale)

    font2 = ImageFont.truetype(font_path1, 10 * scale)

    font3 = ImageFont.truetype(font_path1, 20 * scale)



    perhour = 1376 / 168.0 * scale
    statrx = 112 * scale

    lat = request.args.get("latitude","30.12745")
    lng = request.args.get("longitude", "118.16598")
    tz = "Asia/Shanghai"
    asl = request.args.get("height","1864")
    mountain_id = request.args.get("mountainId","C392")
    baseheight = request.args.get("base","176")
    name = request.args.get("name","莲花峰 / 黄山")

    meteobluePath = os.path.join(dirpath, "meteo_" + mountain_id + ".png")

    mountainPath = os.path.join(dirpath, "mountain_" + mountain_id + ".png")

    unit = request.args.get("unit", "metric")

    if os.path.exists(mountainPath):

        return send_file(mountainPath, as_attachment=True)

    else:


        elevation = float(asl) - float(baseheight)

        city = LocationInfo(name="custom", region="China", timezone="Asia/Shanghai", latitude=float(lat), longitude=float(lng))
        location = Location(city)

        cloudheight = height_to_weathercloud(float(asl)) *scale



        if unit == "metric":
            unitset = "&temperature_units=C&precipitation_units=mm&windspeed_units=kmh"
        else:
            unitset = "&temperature_units=F&precipitation_units=inch&windspeed_units=knot&"




        url = "https://my.meteoblue.com/images/meteogram_extended?apikey=" + meteoblue_allapi_key + "&lat=" + lat + "&lon=" + lng + "&format=png&dpi=100&asl=" + asl + "&tz=" + tz + unitset



        try:

            r = requests.get(url, stream=True)
            if r.status_code != 200:
                print("faile:" + url)
            else:

                f = open(str(meteobluePath), "wb")
                shutil.copyfileobj(r.raw, f, length=16 * 1024 * 1024)
            if os.path.exists(meteobluePath):
                try:
                    print(meteobluePath)
                    layer = Image.new("RGBA", (1600 * scale, 1456 * scale), (255, 255, 255, 255))
                    img = Image.open(meteobluePath).convert("RGBA")
                    layer.paste(img, (0, 0), img)

                    draw = ImageDraw.Draw(layer)
                    draw.text((640 * scale, 15 * scale), name, font=font, fill=(90, 136, 255, 255))

                    draw.line([(80 * scale, cloudheight), (1520 * scale, cloudheight)], fill=(255, 0, 0, 255),
                              width=1)

                    for k in range(0, 7):

                        try:

                            daynoon = todaynoon + datetime.timedelta(days=k)
                            sunrise = location.sunrise(date=daynoon, observer_elevation=float(elevation))
                            sunset = location.sunset(date=daynoon, observer_elevation=float(elevation))

                            risex = statrx + k * 24 * perhour + (sunrise.hour + sunrise.minute / 60.0) * perhour
                            setx = statrx + k * 24 * perhour + (sunset.hour + sunset.minute / 60.0) * perhour

                            draw.line([(risex, cloudheight - 15), (risex, cloudheight + 15)],
                                      fill=(255, 0, 0, 255), width=1)
                            draw.line([(setx, cloudheight - 15), (setx, cloudheight + 15)],
                                      fill=(255, 0, 0, 255),
                                      width=1)

                            draw.text((risex + 1 * scale, cloudheight - 16 * scale),
                                      "日出: %02d:%02d" % (sunrise.hour, sunrise.minute), font=font2,
                                      fill=(255, 0, 0, 255))
                            draw.text((setx + 1 * scale, cloudheight + 5 * scale),
                                      "日落: %02d:%02d" % (sunset.hour, sunset.minute),
                                      font=font2, fill=(255, 0, 0, 255))


                        except Exception as e:
                            print(e)

                    draw.text((30 * scale, 13 * scale), "温馨提示: 山顶天气变幻莫测，请注意防寒和安全措施",
                              font=font3, fill=(255, 0, 0, 255))
                    draw.text((50 * scale, cloudheight - 20 * scale), "山顶", font=font3, fill=(255, 0, 0, 255))
                    # draw.text((30 * scale, 1370 * scale), "更多山峰和一座山峰不同海拔天气查询可在以下App中查询",
                    #           font=font1, fill=(90, 136, 255, 255))
                    # draw.text((30 * scale, 1410 * scale), "iOS端：登山天气-海拔地图", font=font1,
                    #           fill=(90, 136, 255, 255))
                    # draw.text((530 * scale, 1410 * scale), "安卓端：气象计算", font=font1,
                    #           fill=(90, 136, 255, 255))

                    layer.save(mountainPath, "PNG")

                    layer.close()

                except Exception as e:
                    print(e)


        except Exception as e:
            print(e)

        if os.path.exists(mountainPath):
            return send_file(mountainPath, as_attachment=True)
        else:
            return ""




def height_to_weathercloud(mheight):

    height =  mheight


    min_height = 0
    max_height = 14000
    if height < min_height + 0.0000000000001:
        return  714
    if height > max_height - 0.0000000000001:
        return 1140


    normalized_value = height

    breakpoints = [
        (0, 993),
        (1500, 950),
        (3500, 911),
        (6000, 870),
        (9000, 829),
        (14000, 790)
    ]

    # Find the two neighboring breakpoints for the normalized value
    prev_breakpoint, prev_color = breakpoints[0]
    for next_breakpoint, next_color in breakpoints[1:]:
        if normalized_value < next_breakpoint:
            break
        prev_breakpoint, prev_color = next_breakpoint, next_color

    # Interpolate between the neighboring colors
    prev_normalized, prev_rgb = prev_breakpoint, prev_color
    next_normalized, next_rgb = next_breakpoint, next_color
    try:
        t = (normalized_value - prev_normalized) / (next_normalized - prev_normalized)
    except Exception as e:

        print(height)
        print(e)

    r = prev_rgb + (next_rgb - prev_rgb) * t


    return int(r+ 0.5)
