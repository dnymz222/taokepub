#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,wwotrialapikey,openweather_key
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






@api3.route('/openweather/weather/current')
def openweatherweathercurrent():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'https://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=metric"
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



@api3.route('/openweather/weather/hour')
def openweatherweatherhour():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=metric"
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

@api3.route('/openweather/weather/daily')
def openweatherweatherdaily():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=metric&cnt=7"
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


@api3.route('/openweather/weather/history')
def openweatherweatherhistory():
    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1637510400')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language","zh_cn")

    result = {}

    url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=' + lat + '&lon=' + lng + '&dt='+timestamp+ '&appid=' + openweather_key+"&lang="+language+"&units=metric"

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



@api3.route('/openweather/weather/onecall')
def openweatherweatheronecall():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")
    fish = request.args.get("fish","0")


    result = {}

    url = 'https://api.openweathermap.org/data/2.5/onecall?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=imperial&exclude=current,minutely"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        if fish == "1":
            result[x_code] = 200
        else:
            result[x_code] = 200
            result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)



@api3.route('/openweather/weather/minutes')
def openweatherweatherminutes():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'https://api.openweathermap.org/data/2.5/onecall?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=metric&exclude=daily,hourly,alerts"
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


@api3.route('/openweather/air/current')
def openweatheraircurrent():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=metric"
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


@api3.route('/openweather/air/forecast')
def openweatherairforecast():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat='+lat+'&lon='+lng+'&appid='+openweather_key+"&lang="+language+"&units=metric"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        dict = json.loads(content)
        result[x_code] = 200
        result[x_data] = dict["list"]
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route('/openweather/air/history')
def openweatherairhistory():


    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.048')
    start= request.args.get('start', '1607268942')
    end = request.args.get("end","1607355342")
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat='+lat+'&lon='+lng+"&start="+start +"&end="+end+'&appid='+openweather_key+"&lang="+language+"&units=metric"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        dict=json.loads(content)
        result[x_code] = 200
        result[x_data] = dict["list"]
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route('/openweather/map')
def openweathermap():


    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')
    layer  =request.args.get("layer","clouds_new")
    total = request.args.get('total', '1599918717')
    language = request.args.get("language", "zh_cn")


    result = {}

    url = "https://tile.openweathermap.org/map/"+layer+"/1/"+lat+"/"+lng+".png?appid="+openweather_key

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()

        return content
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)






