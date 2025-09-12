#coding=utf8
from . import api3


from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,make_response


import time
from datetime import  datetime
import urllib, sys
import ssl

import json
import base64
import math

import gzip
from app.utils.constvalue import acuuappkey,xinzhi_prinvate_key,xinzhi_public_key,openweather_key,meteobule_apikey

from metpy.units import units
import gzip
from io import StringIO
import requests




@api3.route('/openmeteo/hour/olf')
def openmeteohourold():
    lat = request.args.get('lat', '30')
    lng = request.args.get('lng', '120')


    result = {}

    url = "https://customer-api.open-meteo.com/v1/forecast?latitude="+ lat + "&longitude=" + lng + "&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation_probability,precipitation,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,wind_speed_10m,wind_gusts_10m,wind_direction_10m&timeformat=unixtime&apikey=SUdh1HYBrpXGHv54"

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
#

# @api3.route('/openmeteo/hour')
# def openmeteohour():
#
#
#     lat = request.args.get('lat', '30')
#     lng = request.args.get('lng', '120')
#     # total = request.args.get('total', '1599918717')
#     # language = request.args.get("language", "zh_cn")
#     # tz = request.args.get("tz","Asia/Shanghai")
#     # asl = request.args.get("asl","12")
#     # key = request.args.get("key","c1_8848_20231114")
#
#
#     result = {}
#
#     url = "http://www.astronomyobserver.net/api/v3.0/openmeteo/hour?lat="+lat+"&lng="+lng
#
#     try:
#         req = urllib.request.Request(url)
#         response = urllib.request.urlopen(req)
#         content = response.read()
#
#         return content
#     except Exception as e:
#
#         result[x_code] = 201
#         result[x_meesage] = "%s"%e
#         return json.dumps(result)





@api3.route('/openmeteo/air/old')
def openmeteoairold():
    lat = request.args.get('lat', '30.53')
    lng = request.args.get('lng', '120.05')

    result = {}

    url = "https://customer-air-quality-api.open-meteo.com/v1/air-quality?latitude="+ lat + "&longitude=" + lng + "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,us_aqi&timeformat=unixtime&apikey=SUdh1HYBrpXGHv54"

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


@api3.route('/openmeteo/air')
def openmeteoair():
    lat = request.args.get('lat', '30.53')
    lng = request.args.get('lng', '120.05')

    tz = request.args.get("tz", "Asia,Shanghai")
    asl = request.args.get("asl", "12")

    result = {}

    url = "https://my.meteoblue.com/packages/airquality-1h?apikey=" + meteobule_apikey + "&lat=" + lat + "&lon=" + lng + "&asl="+asl+"&format=json&tz=" + tz

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        contentdict = json.loads(content)

        datadict = {}
        datadict["hourly_units"] = contentdict["units"]
        hourdict = {}
        meteobluehour = contentdict["data_1h"]
        hourdict["pm10"] = meteobluehour["pm10"]
        hourdict["pm2_5"] = meteobluehour["pm25"]
        hourdict["carbon_monoxide"] = meteobluehour["co"]
        hourdict["nitrogen_dioxide"] = meteobluehour["no2"]
        hourdict["sulphur_dioxide"] = meteobluehour["so2"]
        hourdict["ozone"] = meteobluehour["ozone"]
        hourdict["aerosol_optical_depth"] = meteobluehour["aod550"]
        hourdict["dust"] = meteobluehour["dust_concentration"]
        hourdict["us_aqi"] = meteobluehour["airqualityindex"]
        timelist = []
        meteobluetime = meteobluehour["time"]
        tz_offset = timezonfoffset()
        for time_str in meteobluetime:
            fdate = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            timelist.append(int(fdate.timestamp()) + tz_offset)
        hourdict["time"] = timelist
        datadict["hourly"] = hourdict

        result[x_data] = datadict
        result[x_code] = 200

        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)



def timezonfoffset():

    return time.localtime().tm_gmtoff