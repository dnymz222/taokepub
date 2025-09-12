#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,mapdict,pid,x_meesage,appkey,secret,qianggoumap,qianggouList,pinpa_adzone_id,adzone_id,milk_cateList,bottle_catelist,laundry_cateList,pregnancy_catelist,diaper_cateList,supplement_cateList,bath_catelist,wet_catelist,pinpaiIdList,pinpaiNameList,muyinIdlist,clothes_catelist,shoes_cateList,muyinNameList,lamaids,lamanames,lamaurls,daeIdList,daeNameList
import json
from flask import request,session,url_for,redirect,make_response,jsonify
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
from app.utils.constvalue import acuuappkey,xinzhi_prinvate_key,xinzhi_public_key,openweather_key
import metpy.calc as mpcalc
from metpy.units import units
import gzip
import jwt
import datetime
from datetime import tzinfo
import requests
from app.JWTConfig import JWTConfig
import time
import pytz
from io import StringIO


config = JWTConfig()
dateForm = "%Y-%m-%dT%H:%M:%SZ"
tz = pytz.timezone("GMT")

@api3.route("/weather")
def adaptdarkweather():
    lat = request.args.get('lat', '40.2422')
    lng = request.args.get('lng', '116.2278')
    timestamp = request.args.get('time','1550069439')
    total = request.args.get('total','1599918717')

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

    url = "https://weatherkit.apple.com/api/v1/weather/en/"+lat+"/"+lng
    param = {}
    now = datetime.datetime.now(tz)
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)

    timezone = request.args.get("timezone", "Asia/Shanghai")
    osname = request.args.get("os","iOS")

    start = zero_today
    end = zero_today + datetime.timedelta(days=9)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)
    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone

    return __requestAndLoadJson(url, param)

@api3.route("/weather/histroy")
def adaptdarkweatherhistroy():
    lat = request.args.get('lat', '40.2422')
    lng = request.args.get('lng', '116.2278')
    timestamp = request.args.get('time','1550069439')
    total = request.args.get('total','1599918717')
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

    url = "https://weatherkit.apple.com/api/v1/weather/en/"+lat+"/"+lng
    param = {}
    now = datetime.datetime.now(tz)

    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)

    timezone = request.args.get("timezone", "Asia/Shanghai")
    osname = request.args.get("os","iOS")

    start = zero_today -  datetime.timedelta(days=1)
    end = zero_today + datetime.timedelta(days=1)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)
    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone

    return __requestAndLoadJson(url, param)


@api3.route('/weather/<latitude>/<longitude>', methods=['GET'])
def weatherLoc(latitude, longitude):

    lat = latitude
    lng = longitude
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

    url = "https://weatherkit.apple.com/api/v1/weather/en/"+latitude+"/"+longitude
    param = {}
    now = datetime.datetime.now(tz)

    zero_today = now - datetime.timedelta(hours=now.hour , minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)

    timezone = request.args.get("timezone", "Asia/Shanghai")
    timezoe = request.args.get("timezoe")
    if timezoe is not  None:
        timezone = timezoe
    osname = request.args.get("os","iOS")

    start = zero_today - datetime.timedelta(days=2)
    end = zero_today + datetime.timedelta(days=8)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)

    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone
    # try:
    return __requestAndLoadJson(url, param)


@api3.route('/weather/json/<latitude>/<longitude>', methods=['GET'])
def weatherjsonLoc(latitude, longitude):

    lat = latitude
    lng = longitude
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

    url = "https://weatherkit.apple.com/api/v1/weather/en/"+latitude+"/"+longitude
    param = {}
    tz = pytz.timezone("Asia/Shanghai")

    now = datetime.datetime.now(tz)





    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)



    timezone = request.args.get("timezone", "Asia/Shanghai")
    osname = request.args.get("os","iOS")

    start = zero_today - datetime.timedelta(days=1)
    end = zero_today + datetime.timedelta(days=9)
    hourstart = start - datetime.timedelta(hours=8)
    hourend = end - datetime.timedelta(hours=8)
    param["hourlyStart"] = appleDateToString(hourstart)
    param["hourlyEnd"] = appleDateToString(hourend)

    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone

    result =  __requestAndLoadNoGzipJson(url, param)
    return json.dumps(result)


@api3.route('/weather/forecast/<latitude>/<longitude>', methods=['GET'])
def weatherforecastLoc(latitude, longitude):

    lat = latitude
    lng = longitude
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

    url = "https://weatherkit.apple.com/api/v1/weather/en/"+latitude+"/"+longitude
    param = {}
    tz = pytz.timezone("Asia/Shanghai")

    now = datetime.datetime.now(tz)


    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)

    timezone = request.args.get("timezone", "Asia/Shanghai")

    start = zero_today
    end = zero_today + datetime.timedelta(days=7)
    hourstart = start - datetime.timedelta(hours=8)
    hourend = end - datetime.timedelta(hours=8)
    param["hourlyStart"] = appleDateToString(hourstart)
    param["hourlyEnd"] = appleDateToString(hourend)

    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone

    result =  __requestAndLoadNoGzipJson(url, param)
    return json.dumps(result)


@api3.route('/weather/chonglang', methods=['GET'])
def weatherchonglongLoc():
    latitude = request.args.get("latitude","30")
    longitude = request.args.get("longitude","120")


    url = "https://weatherkit.apple.com/api/v1/weather/en/" + latitude + "/" + longitude
    param = {}
    tz = pytz.timezone("Asia/Shanghai")

    now = datetime.datetime.now(tz)

    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)

    timezone = request.args.get("timezone", "Asia/Shanghai")
    start = zero_today
    end = zero_today + datetime.timedelta(days=7)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)

    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone
    result = {}


    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)


        days = content["forecastDaily"]["days"]
        hours = content["forecastHourly"]["hours"]

        data = {}


        data["daily"] = days
        data["hourly"] = hours

        result[x_code] = 200
        result[x_data] = data

        return json.dumps(result)
    except Exception as e:


        try:
            res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
            content = json.loads(res.content)


            days = content["forecastDaily"]["days"]
            hours = content["forecastHourly"]["hours"]

            data = {}


            data["daily"] = days
            data["hourly"] = hours

            result[x_code] = 200
            result[x_data] = data

            return json.dumps(result)

        except Exception as e:
            result [x_code] = 201
            result[x_meesage] = "%s"%e
            return json.dumps(result)


# # 确定可用于指定位置的数据集 https://developer.apple.com/documentation/weatherkitrestapi/get_api_v1_availability_latitude_longitude
@api3.route("/availability/<latitude>/<longitude>", methods=['GET'])
def availability(latitude, longitude):
    url = "https://weatherkit.apple.com/api/v1/availability/"+latitude+"/"+longitude
    param = request.args
    result = {}
    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)
        result[x_code] = 200
        result[x_data] = content


    except Exception  as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)



def __requestAndLoadJson(url, param):
    out = StringIO()
    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)
        days = content["forecastDaily"]["days"]
        hours = content["forecastHourly"]["hours"]

        result = {}
        hourlyDict = {}
        hourlyList = []
        dayList = []
        daydict = {}
        for day in days:
            darkday = mapDayDictToDarkSky(day)
            dayList.append(darkday)
        for hour in hours:
            darkhour = mapHourDictToDarkSky(hour)
            hourlyList.append(darkhour)
        hourlyDict["data"] = hourlyList
        daydict["data"] = dayList
        result["hourly"] = hourlyDict
        result["daily"] = daydict

        json_data = bytes(json.dumps(result), "utf8")

        buf = gzip.compress(json_data, compresslevel=1)
        return buf
    except Exception as e:

        try:
            res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
            content = json.loads(res.content)
            days = content["forecastDaily"]["days"]
            hours = content["forecastHourly"]["hours"]

            result = {}
            hourlyDict = {}
            hourlyList = []
            dayList = []
            daydict = {}
            for day in days:
                darkday = mapDayDictToDarkSky(day)
                dayList.append(darkday)
            for hour in hours:
                darkhour = mapHourDictToDarkSky(hour)
                hourlyList.append(darkhour)
            hourlyDict["data"] = hourlyList
            daydict["data"] = dayList
            result["hourly"] = hourlyDict
            result["daily"] = daydict

            json_data = bytes(json.dumps(result), "utf8")

            buf = gzip.compress(json_data, compresslevel=1)
            return buf
        except Exception as e:

            out.close()
            result = {}
            result[x_code] = 201
            result[x_meesage] = "%s"%e
            return json.dumps(result)




def __requestAndLoadNoGzipJson(url, param):
    out = StringIO()
    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)


        content = json.loads(res.content)

        # return content



        days = content["forecastDaily"]["days"]
        hours = content["forecastHourly"]["hours"]


        result = {}
        hourlyDict = {}
        hourlyList = []
        dayList = []
        daydict = {}
        for day in days:
            darkday = mapDayDictToDarkSky(day)
            dayList.append(darkday)
        for hour in hours:
            darkhour = mapHourDictToDarkSky(hour)
            hourlyList.append(darkhour)
        hourlyDict["data"] = hourlyList
        daydict["data"] = dayList
        result["hourly"] = hourlyDict
        result["daily"] = daydict
        return result

    except Exception as e:



        try:
            res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
            content = json.loads(res.content)
            days = content["forecastDaily"]["days"]
            hours = content["forecastHourly"]["hours"]

            result = {}
            hourlyDict = {}
            hourlyList = []
            dayList = []
            daydict = {}
            for day in days:
                darkday = mapDayDictToDarkSky(day)
                dayList.append(darkday)
            for hour in hours:
                darkhour = mapHourDictToDarkSky(hour)
                hourlyList.append(darkhour)
            hourlyDict["data"] = hourlyList
            daydict["data"] = dayList
            result["hourly"] = hourlyDict
            result["daily"] = daydict

            return  result
        except Exception as e:

            out.close()
            result = {}
            result[x_code] = 201
            result[x_meesage] = "%s"%e
            return result




def mapDayDictToDarkSky(dict):
    darkDict = {}
    darkDict["time"] = appleTimeStempFromString(dict["forecastStart"])
    darkDict["icon"] = dict["conditionCode"]
    darkDict["precipIntensity"] = inchesfrommmday(dict["precipitationAmount"])
    darkDict["precipProbability"] = dict["precipitationChance"]
    darkDict["temperatureMax"] = huashifromnieshi(dict["temperatureMax"])
    darkDict["temperatureMin"] = huashifromnieshi(dict["temperatureMin"])
    darkDict["humidity"] = dict["daytimeForecast"]["humidity"]
    darkDict["uvIndex"] = dict["maxUvIndex"]
    darkDict["windSpeed"] = milesfrom(dict["daytimeForecast"]["windSpeed"])
    darkDict["windBearing"] = dict["daytimeForecast"]["windDirection"]
    darkDict["pressure"] = 1013.0
    darkDict["visibility"] = 10
    return darkDict

def mapHourDictToDarkSky(dict):
    darkDict = {}
    darkDict["time"] = appleTimeStempFromString(dict["forecastStart"])
    darkDict["icon"] = dict["conditionCode"]
    darkDict["precipIntensity"] = dict["precipitationAmount"]
    darkDict["precipProbability"] = dict["precipitationChance"]
    darkDict["temperature"] = huashifromnieshi(dict["temperature"])
    darkDict["humidity"] = dict["humidity"]
    darkDict["windSpeed"] = milesfrom(dict["windSpeed"])
    darkDict["windBearing"] = dict["windDirection"]
    darkDict["windGust"] = milesfrom(dict["windGust"])
    darkDict["pressure"] = dict["pressure"]
    darkDict["daylight"] = dict["daylight"]
    if "pressureTrend" not in dict:
        darkDict["pressureTrend"] = dict["pressureTrend"]
    darkDict["visibility"] = dict["visibility"]
    darkDict["uvIndex"] = dict["uvIndex"]
    darkDict["cloudCover"] = dict["cloudCover"]
    return darkDict


def milesfrom(k):
    return k / 1.609344;

def appleDateToString(date):
    return date.strftime(dateForm)



def appleTimeStempFromString(str):
    startime = datetime.datetime.strptime(str, dateForm)
    return  int(time.mktime(startime.timetuple())) + 8 * 3600

def huashifromnieshi(C):
    huashi = C * 9.0 / 5.0 + 32.0
    return huashi

def inchesfrommmday(mm):
    inches = mm * 0.03937

    return inches


@api3.route('/weatherkit/weather/<latitude>/<longitude>', methods=['GET'])
def weatherkitweather(latitude, longitude):
    url = "https://weatherkit.apple.com/api/v1/weather/en/" + latitude + "/" + longitude
    param = {}

    timezone = request.args.get("timezone", "Asia/Shanghai")

    atz = pytz.timezone(timezone)

    now = datetime.datetime.now(atz)

    isvip = request.args.get("isvip", "0")

    forecastday = 2
    if isvip == "1":
        forecastday = 10

    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)

    start = zero_today - datetime.timedelta(days=4)
    end = zero_today + datetime.timedelta(days=forecastday)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)
    param["dataSets"] = "forecastHourly"
    param["timezone"] = timezone
    result = {}

    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)
        hours = content["forecastHourly"]["hours"]

        result[x_code] = 200
        result[x_data] = hours



    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)

@api3.route('/weatherkit/current', methods=['GET'])
def currentappleweather():
    latitude = request.args.get("lat", "30")
    longitude = request.args.get("lat", "120")
    url = "https://weatherkit.apple.com/api/v1/weather/en/" + latitude + "/" + longitude
    param = {}

    timezone = request.args.get("timezone", "Asia/Shanghai")

    param["dataSets"] = "currentWeather"
    param["timezone"] = timezone
    result = {}

    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)
        result[x_code] = 200
        result[x_data] = content["currentWeather"]
        return json.dumps(result)

    except Exception  as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


def checklatandlon(lat,lng,timestamp,total):
    latng_i = int(float(lat) * 100 * float(lng) * 100)
    timestamp_i = int(timestamp)
    local_i = int(time.time())
    deta = abs(timestamp_i - local_i)
    if deta > 3600 :
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


@api3.route('/weather/forecast/json/v2/<latitude>/<longitude>', methods=['GET'])
def weatherforecastjsonversontwo(latitude, longitude):
    url = "https://weatherkit.apple.com/api/v2/weather/en/"+latitude+"/"+longitude
    param = {}



    timstamp = request.args.get("starttime","1739980800")
    zerotime = datetime.datetime.fromtimestamp(int(timstamp),tz=tz)

    start = zerotime

    timezone = request.args.get("timezone", "Asia/Shanghai")

    target = request.args.get("target","app")
    days = 10
    if target == "widget":
        days = 3

    end = start + datetime.timedelta(days=days)


    param["dailyStart"] = appleDateToString(start)
    param["dailyEnd"] = appleDateToString(end)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)

    param["dataSets"] = "forecastHourly,forecastDaily"
    param["timezone"] = timezone

    result = {}

    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)


        days = content["forecastDaily"]["days"]
        hours = content["forecastHourly"]["hours"]

        data = {}


        data["daily"] = days
        data["hourly"] = hours

        result[x_code] = 200
        result[x_data] = data

        return json.dumps(result)

    except Exception as e:
        try:
            res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
            content = json.loads(res.content)

            days = content["forecastDaily"]["days"]
            hours = content["forecastHourly"]["hours"]

            data = {}

            data["daily"] = days
            data["hourly"] = hours

            result[x_code] = 200
            result[x_data] = data

            return json.dumps(result)
        except Exception as e:

            result [x_code] = 201
            result[x_meesage] = "%s" % e
            return json.dumps(result)


@api3.route('/cloud/hour', methods=['GET'])
def cloudhourapple():
    latitude = request.args.get("lat","30")
    longitude = request.args.get("lng","120")
    timezone = request.args.get("timezone","Asia/Shanghai")

    starttime = request.args.get("starttime","1743091200")


    url = "https://weatherkit.apple.com/api/v2/weather/en/" + latitude + "/" + longitude
    param = {}


    zerotime = datetime.datetime.fromtimestamp(int(starttime), tz=tz)

    start = zerotime
    end = zerotime + datetime.timedelta(days=10)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)

    param["dataSets"] = "forecastHourly"
    param["timezone"] = timezone
    result = {}




    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)

        hours = content["forecastHourly"]["hours"]

        result[x_code] = 200
        result[x_data] = hours

        return json.dumps(result)



    except Exception as e:


        try:
            res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
            content = json.loads(res.content)


            hours = content["forecastHourly"]["hours"]


            result[x_code] = 200
            result[x_data] = hours

            return json.dumps(result)

        except Exception as e:
            result [x_code] = 201
            result[x_meesage] = "%s"%e
            return json.dumps(result)



@api3.route('/openmeteo/hour', methods=['GET'])
def openmeteohourapple():
    latitude = request.args.get("lat","30")
    longitude = request.args.get("lng","120")


    url = "https://weatherkit.apple.com/api/v2/weather/en/" + latitude + "/" + longitude
    param = {}
    tz = pytz.timezone("Asia/Shanghai")

    now = datetime.datetime.now(tz)

    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)

    timezone = request.args.get("timezone", "Asia/Shanghai")
    start = zero_today
    end = zero_today + datetime.timedelta(days=7)
    param["hourlyStart"] = appleDateToString(start)
    param["hourlyEnd"] = appleDateToString(end)

    param["dataSets"] = "forecastHourly"
    param["timezone"] = timezone
    result = {}


    try:
        res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
        content = json.loads(res.content)



        hours = content["forecastHourly"]["hours"]

        data = {}

        hourdict = {}

        time_list = []
        temperature_2m_list = []
        relative_humidity_2m_list = []
        dew_point_2m_list = []
        apparent_temperature_list = []
        precipitation_probability_list = []
        precipitation_list = []
        weather_code_list = []
        pressure_msl_list = []
        surface_pressure_list = []
        cloud_cover_list = []
        cloud_cover_low_list = []
        cloud_cover_mid_list = []
        cloud_cover_high_list = []
        visibility_list = []
        wind_speed_10m_list = []
        wind_gusts_10m_list = []
        wind_direction_10m_list = []
        uv_index_list = []
        conditionCode_list = []

        for houritem in hours:
            time_list.append(houritem["forecastStart"])
            temperature_2m_list.append(houritem["temperature"])
            relative_humidity_2m_list.append(houritem["humidity"])
            dew_point_2m_list.append(houritem["temperatureDewPoint"])
            apparent_temperature_list.append(houritem["temperatureApparent"])
            precipitation_probability_list.append(houritem["precipitationChance"])
            precipitation_list.append(houritem["precipitationIntensity"])

            conditionCode = houritem["conditionCode"]
            conditionCode_list.append(conditionCode)
            weather_code_list.append(conditiontoweathercode(conditionCode))

            pressure_msl_list.append(houritem["pressure"])
            surface_pressure_list.append(houritem["pressure"])
            cloud_cover_list.append(houritem["cloudCover"])
            cloud_cover_low_list.append(houritem["cloudCoverLowAltPct"])
            cloud_cover_mid_list.append(houritem["cloudCoverMidAltPct"])
            cloud_cover_high_list.append(houritem["cloudCoverHighAltPct"])
            visibility_list.append(houritem["visibility"])
            wind_speed_10m_list.append(houritem["windSpeed"])
            wind_gusts_10m_list.append(houritem["windGust"])
            wind_direction_10m_list.append(houritem["windDirection"])

            uv_index_list.append(houritem["uvIndex"])





        hourdict["time"] = time_list
        hourdict["temperature_2m"] = temperature_2m_list
        hourdict["relative_humidity_2m"] = relative_humidity_2m_list
        hourdict["dew_point_2m"] = dew_point_2m_list
        hourdict["apparent_temperature"] = apparent_temperature_list
        hourdict["precipitation_probability"] = precipitation_probability_list
        hourdict["precipitation"] = precipitation_list
        hourdict["weather_code"] = weather_code_list
        hourdict["pressure_msl"] = pressure_msl_list
        hourdict["surface_pressure"] =surface_pressure_list
        hourdict["cloud_cover"] = cloud_cover_list
        hourdict["cloud_cover_low"] = cloud_cover_low_list
        hourdict["cloud_cover_mid"] = cloud_cover_mid_list
        hourdict["cloud_cover_high"] = cloud_cover_high_list
        hourdict["visibility"] = visibility_list
        hourdict["wind_speed_10m"] = wind_speed_10m_list
        hourdict["wind_gusts_10m"] = wind_gusts_10m_list
        hourdict["wind_direction_10m"] = wind_direction_10m_list
        hourdict["uv_index"] = uv_index_list
        hourdict["condition_code"] = conditionCode_list
        data["hourly"] = hourdict

        result[x_code] = 200
        result[x_data] = data

        return json.dumps(result)
    except Exception as e:


        try:
            res = requests.get(url, headers={"Authorization": ("Bearer " + config.genToken())}, params=param)
            content = json.loads(res.content)

            hours = content["forecastHourly"]["hours"]

            data = {}

            hourdict = {}

            time_list = []
            temperature_2m_list = []
            relative_humidity_2m_list = []
            dew_point_2m_list = []
            apparent_temperature_list = []
            precipitation_probability_list = []
            precipitation_list = []
            weather_code_list = []
            pressure_msl_list = []
            surface_pressure_list = []
            cloud_cover_list = []
            cloud_cover_low_list = []
            cloud_cover_mid_list = []
            cloud_cover_high_list = []
            visibility_list = []
            wind_speed_10m_list = []
            wind_gusts_10m_list = []
            wind_direction_10m_list = []
            uv_index_list = []
            conditionCode_list = []

            for houritem in hours:
                time_list.append(houritem["forecastStart"])
                temperature_2m_list.append(houritem["temperature"])
                relative_humidity_2m_list.append(houritem["humidity"])
                dew_point_2m_list.append(houritem["temperatureDewPoint"])
                apparent_temperature_list.append(houritem["temperatureApparent"])
                precipitation_probability_list.append(houritem["precipitationChance"])
                precipitation_list.append(houritem["precipitationIntensity"])

                conditionCode = houritem["conditionCode"]
                conditionCode_list.append(conditionCode)
                weather_code_list.append(conditiontoweathercode(conditionCode))

                pressure_msl_list.append(houritem["pressure"])
                surface_pressure_list.append(houritem["pressure"])
                cloud_cover_list.append(houritem["cloudCover"])
                cloud_cover_low_list.append(houritem["cloudCoverLowAltPct"])
                cloud_cover_mid_list.append(houritem["cloudCoverMidAltPct"])
                cloud_cover_high_list.append(houritem["cloudCoverHighAltPct"])
                visibility_list.append(houritem["visibility"])
                wind_speed_10m_list.append(houritem["windSpeed"])
                wind_gusts_10m_list.append(houritem["windGust"])
                wind_direction_10m_list.append(houritem["windDirection"])

                uv_index_list.append(houritem["uvIndex"])

            hourdict["time"] = time_list
            hourdict["temperature_2m"] = temperature_2m_list
            hourdict["relative_humidity_2m"] = relative_humidity_2m_list
            hourdict["dew_point_2m"] = dew_point_2m_list
            hourdict["apparent_temperature"] = apparent_temperature_list
            hourdict["precipitation_probability"] = precipitation_probability_list
            hourdict["precipitation"] = precipitation_list
            hourdict["weather_code"] = weather_code_list
            hourdict["pressure_msl"] = pressure_msl_list
            hourdict["surface_pressure"] = surface_pressure_list
            hourdict["cloud_cover"] = cloud_cover_list
            hourdict["cloud_cover_low"] = cloud_cover_low_list
            hourdict["cloud_cover_mid"] = cloud_cover_mid_list
            hourdict["cloud_cover_high"] = cloud_cover_high_list
            hourdict["visibility"] = visibility_list
            hourdict["wind_speed_10m"] = wind_speed_10m_list
            hourdict["wind_gusts_10m"] = wind_gusts_10m_list
            hourdict["wind_direction_10m"] = wind_direction_10m_list
            hourdict["uv_index"] = uv_index_list
            hourdict["condition_code"] = conditionCode_list
            data["hourly"] = hourdict

            result[x_code] = 200
            result[x_data] = data

            return json.dumps(result)

        except Exception as e:
            result [x_code] = 201
            result[x_meesage] = "%s"%e
            return json.dumps(result)

def conditiontoweathercode(theCondition: str) -> int:

    if theCondition == "Clear":
        return 0

    elif theCondition == "MostlyClear":
        return 1

    elif theCondition == "PartlyCloudy":
        return 2
    elif theCondition == "MostlyCloudy":
        return 3
    elif theCondition == "Cloudy":
        return 2

    elif theCondition == "Hazy":
        return 45


    elif theCondition == "ScatteredThunderstorms"  or theCondition == "IsolatedThunderstorms":
        return 95

    elif theCondition == "Drizzle":
        return 51

    elif theCondition == "Rain":
        return 63
    elif theCondition == "HeavyRain":
        return 65

    elif theCondition == "Snow":
        return 73
    elif theCondition == "HeavySnow":
        return 75

    elif theCondition == "Flurries":
        return 71


    elif theCondition == "Haze":
        return 48

    elif theCondition == "BlowingDust":

        return 48

    elif theCondition == "Foggy":
        return 45
    elif theCondition == "Smoky":
        return 48
    elif theCondition == "Breezy" or theCondition == "Windy":
        return 56
    elif theCondition == "StrongStorms" or theCondition == "Thunderstorms":
        return 96
    elif theCondition == "Hail" or theCondition == "FreezingDrizzle" or theCondition == "FreezingRain":
        return 57

    elif theCondition == "Sleet" or theCondition == "WintryMix":
        return 57
    elif theCondition == "SunFlurries":

        return 80

    elif theCondition ==  "Hurricane" or  theCondition == "TropicalStorm":
        return 82
    elif theCondition == "Blizzard" or theCondition == "BlowingSnow":
        return 77

    elif theCondition == "SunShowers":
        return 81
    else:
        return 0