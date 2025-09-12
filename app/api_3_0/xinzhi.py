#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,hefengfishingapikey,hefengusername
import json
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
import requests
from .hgt import  get_elavation
from app.utils.constvalue import acuuappkey,xinzhi_prinvate_key,xinzhi_public_key


@api3.route('/xinzhi/location/search')
def xinzhilocationsearch():

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}
    # code = weatherchecklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)


    try:
        # port = request.args.get('port','WTWFRHBJHX9W')
        url  ="https://api.seniverse.com/v3/location/search.json?key="+ xinzhi_prinvate_key+"&q="+lat+':'+lng
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)
        result[x_code] = 200
        result[x_data] = contentdict['results'][0]
    except Exception as  e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)


@api3.route('/xinzhi/aqi')
def ximzhiaqi():

    lat = request.args.get('lat', '30.283')
    lng = request.args.get('lng', '120.05')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}
    # code = weatherchecklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)


    try:
        port = request.args.get('port','WTWFRHBJHX9W')
        url  ="https://api.seniverse.com/v3/air/now.json?key="+ xinzhi_prinvate_key+"&location="+lat+':'+lng +"&language=zh-Hans&scope=city"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)
        result[x_code] = 200
        result[x_data] = contentdict['results'][0]
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)

@api3.route('/xinzhi/aqi/day')
def ximzhiaqiday():

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    port = request.args.get('port', 'WTWFRHBJHX9W')
    result = {}
    # code = weatherchecklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)


    try:

        url  ="https://api.seniverse.com/v3/air/daily.json?key="+ xinzhi_prinvate_key+"&location="+lat+':'+lng +"&language=zh-Hans&scope=city"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)
        result[x_code] = 200
        result[x_data] = contentdict['results'][0]
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


@api3.route('/xinzhi/aqi/hour')
def ximzhiaqihour():

    lat = request.args.get('lat', '30.313')
    lng = request.args.get('lng', '120.05')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    port = request.args.get('port', 'WTWFRHBJHX9W')
    result = {}
    # code = weatherchecklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)


    try:

        url  ="https://api.seniverse.com/v3/air/hourly.json?key="+ xinzhi_prinvate_key+"&location="+lat+':'+lng +"&language=zh-Hans&scope=city"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)
        result[x_code] = 200
        result[x_data] = contentdict['results'][0]
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


@api3.route('/xinzhi/weather')
def ximzhiweather():

    lat = request.args.get('lat', '38.48')
    lng = request.args.get('lng', '95.51')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    result = {}
    # code = weatherchecklatandlon(lat=lat,lng=lng,timestamp=timestamp,total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)


    try:
        # port = request.args.get('port','WTWFRHBJHX9W')

        url  ="https://api.seniverse.com/v3/weather/hourly_history.json?key="+ xinzhi_prinvate_key+"&location="+lat+':'+lng +"&language=zh-Hans&scope=city"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)
        result[x_code] = 200
        result[x_data] = contentdict['results'][0]
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
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