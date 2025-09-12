#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,hefengfishingapikey,hefengusername,acuuappkey
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
from config import basedir
from app.Hefengtide import Hefengtide
import xlrd
from app.TyphoonModel import TyphoonModel
import pytz

@api3.route("/hefeng/tid/search")
def hefengtid_seach():
    location = request.args.get("location","汕头")
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    lang = request.args.get("lang", "zh")
    try:
        response = requests.get(
            'https://geoapi.qweather.com/v2/poi/lookup',
            params={
                "location":location,
                "key":hefengfishingapikey,
                "lang":lang,
                "type":"TSTA"
            },

        )


        # print  response

        # Do something with response data.
        json_data = response.json()
        return json.dumps(json_data)
    except Exception as e:

        return "hello word"



@api3.route("/weather/hefeng/tide/group")
def hefengtidegroup():
    datestring = request.args.get('date', '20231224,20231225,20231226')
    fixday = request.args.get("fixday","20230226")
    location = request.args.get("location","P2671")
    code = request.args.get("code","T131")
    result = {}

    dates = datestring.split(",")

    list = []

    try:
        response = requests.get(
            'http://www.xunquan.shop/api/v3.0/weather/hefeng/tide/group',
            params={
                "location":location,
                "date":datestring,
                "code":code,
                "fixday":fixday
            },

        )

        json_data = response.json()
        return json.dumps(json_data)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)





@api3.route("/weather/hefeng/tide")
def hefengtide():
    date = request.args.get('date', '20231222')
    location = request.args.get("location","P2102")
    code = request.args.get("code","T132")
    fixday = request.args.get("fixday", "20230326")
    result = {}

    try:
        response = requests.get(
            'http://www.xunquan.shop/api/v3.0/weather/hefeng/tide',
            params={
                "location":location,
                "date":date,
                "code":code,
                "fixday":fixday
            },

        )

        json_data = response.json()
        return json.dumps(json_data)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route("/hefeng/tide/locations")
def hefengtidelocations():
    list = ["P2102", "P2109", "P2113", "P2115", "P2117", "P2121", "P2122", "P2126", "P2131", "P2134", "P2137", "P2143", "P2146", "P2149", "P2159", "P2168", "P2169", "P2172", "P2177", "P2180", "P2197", "P2205", "P2225", "P2232", "P2236", "P2240", "P2243", "P2244", "P2246", "P2257", "P2259", "P2260", "P2275", "P2284", "P2285", "P2286", "P2288", "P2289", "P2299", "P2304", "P2305", "P2306", "P2313", "P2314", "P2327", "P2334", "P2337", "P2340", "P2350", "P2351", "P2352", "P2357", "P2362", "P2364", "P2372", "P2398", "P2409", "P2410", "P2411", "P2414", "P2418", "P2419", "P2423", "P2426", "P2428", "P2429", "P2432", "P2436", "P2440", "P2442", "P2447", "P2450", "P2454", "P2461", "P2462", "P2474", "P2483", "P2488", "P2490", "P2494", "P2499", "P2510", "P2512", "P2513", "P2519", "P2523", "P2528", "P2532", "P2533", "P2536", "P2537", "P2539", "P2543", "P2554", "P2558", "P2559", "P2560", "P2563", "P2566", "P2570", "P2575", "P2578", "P2582", "P2584", "P2585", "P2587", "P2590", "P2591", "P2598", "P2602", "P2609", "P2612", "P2619", "P2620", "P2621", "P2627", "P2633", "P2643", "P2646", "P2647", "P2651", "P2652", "P2653", "P2659", "P2664", "P2669", "P2671", "P2672", "P2680", "P2683", "P2689", "P2692", "P2699", "P2709", "P2712", "P2717", "P2727", "P2728", "P2735", "P2737", "P2738", "P2739", "P2743", "P2750", "P2751", "P2761", "P2764", "P2769", "P2774", "P2780", "P2781", "P2785", "P2792", "P2793", "P2794", "P2799", "P2801", "P2806", "P2816", "P2822", "P2825", "P2827", "P2830", "P2835", "P2848", "P2849", "P2862", "P2864", "P2872", "P2880", "P2885", "P2886", "P2890", "P2891", "P2892", "P2894", "P2895", "P2903", "P2908", "P2912", "P2916", "P2919", "P2926", "P2929", "P2931", "P2932", "P2938", "P2939", "P2943", "P2944", "P2945", "P2951", "P2953", "P2962", "P2966", "P2967", "P2980", "P2982", "P2992", "P2998"]

    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.datetime.now(tz)
    date = "%d%02d%02d"%(now.year,now.month,now.day)

    for location in list:

        filename = date+"_"+location
        tidepath = os.path.join(basedir,"static/hefengtide",filename)

        try:
            if os.path.exists(tidepath):
                pass
            else:

                    response = requests.get(
                        'https://api.qweather.com/v7/ocean/tide',
                        params={
                            "location": location,
                            "key": hefengfishingapikey,
                            "date":date

                        },

                    )

                    json_data = response.json()

                    code = json_data["code"]
                    tidefixtime = ""
                    if "tideTable" in json_data:
                        tideLabel= json_data["tideTable"]
                        tidelabe0 = tideLabel[0]
                        tidefixtime = tidelabe0["fxTime"]

                    if code == "200" and len(tidefixtime) > 2:

                        result = {}
                        result[x_code] = 200
                        result[x_data] = json_data

                        try:

                            jdata = json.dumps(result).encode("utf8")
                            fw = open(tidepath,"w")
                            fw.write(jdata)
                            fw.close()
                        except Exception as e:
                            print (e)
        except  Exception as e:
            print(e)



@api3.route("/shantou")
def shantou():
    xlspath = os.path.join(basedir, "static/chaoxibiao/shantou", "shantou.xlsx")
    bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

    txtpath1 = os.path.join(basedir,"static/chaoxibiao/shantou","0301.txt")
    txtpath2 = os.path.join(basedir, "static/chaoxibiao/shantou", "0302.txt")

    list = []

    sh = bk.sheets()[0]
    nrows = sh.nrows
    ncols = sh.ncols
    for i in range(1,nrows):
        dict = {}
        row_value = sh.row_values(i)
        year =  str(int(row_value[0]))
        month = "%02d"%(int(row_value[1]))
        day = "%02d"%(int(row_value[2]))
        dict["day"] = year +"-" + month+ "-" + day
        datadict = {}
        tidetable = []
        time1 = row_value[3].replace(" ",":")
        heigh1 = int(row_value[4])
        time2 = row_value[5].replace(" ",":")
        height2 = int(row_value[6])
        time3 = row_value[7].replace(" ",":")
        height3 = int(row_value[8])
        time4 = row_value[9].replace(" ",":")

        dict1 = {}
        dict1["fxTime"] = year +"-" +  month + "-" + day +"T" + time1 + "+08:00"
        dict1["height"] = "%.2f"%(heigh1/100.0)
        if heigh1 > height2:
            dict1["type"] = "H"
        else:
            dict1["type"] = "L"

        tidetable.append(dict1)

        dict2 = {}
        dict2["fxTime"] = year + "-" + month + "-" + day + "T" + time2 + "+08:00"
        dict2["height"] = "%.2f" % (height2 / 100.0)
        if heigh1 > height2:
            dict2["type"] = "L"
        else:
            dict2["type"] = "H"
        tidetable.append(dict2)

        dict3 = {}
        dict3["fxTime"] = year + "-" + month + "-" + day + "T" + time3 + "+08:00"
        dict3["height"] = "%.2f" % (height3 / 100.0)
        if height3 > height2:
            dict3["type"] = "H"
        else:
            dict3["type"] = "L"

        tidetable.append(dict3)


        if len(time4) > 0:
            height4 = int(row_value[10])
            dict4 = {}
            dict4["fxTime"] = year + "-" + month + "-" + day + "T" + time4 + "+08:00"
            dict4["height"] = "%.2f" % (height4 / 100.0)
            if height4 > height3:
                dict4["type"] = "H"
            else:
                dict4["type"] = "L"

            tidetable.append(dict4)
        datadict["code"] ="200"
        datadict["tideTable"] = tidetable
        dict[x_data] = datadict
        list.append(dict)




    file_test1 = open(txtpath1, 'r')
    daycount = 1
    list1 = []
    for lines in file_test1.readlines():
        line = lines.strip().strip('\n')
        line = line.replace("&nbsp;", "")
        values = line.split(" ")
        if len(values) > 1:
            for va in values:
                v = va.strip()
                if len(v) > 0:
                    list1.append("%.2f"%(int(v)/100.0))

    n1 = 16
    if len(list1) == n1 * 24:
        for i in range(0, n1 ):
            dict = list[i]
            day = dict["day"]
            datadict = dict[x_data]
            tidehour = []
            for j in range(0,24):
                hourdict = {}
                hourdict["fxTime"] = day +"T"+ "%02d"%j +":00+08:00"
                hourdict["height"] = list1[j * n1 + i]
                tidehour.append(hourdict)
            datadict["tideHourly"] = tidehour


    else:
        print ("wrong")
        print (len(list1))

    list2 = []
    file_test2 = open(txtpath2, 'r')
    for lines in file_test2.readlines():
        line = lines.strip().strip('\n')
        line = line.replace("&nbsp;", "")
        values = line.split(" ")
        if len(values) > 1:
            for va in values:
                v = va.strip()
                if len(v) > 0:
                    list2.append("%.2f"%(int(v)/100.0))
    n2 = 15
    if len(list2) ==  n2 * 24:
        for i in range(0, n2 ):
            dict = list[n1 + i]
            day = dict["day"]
            datadict = dict[x_data]
            tidehour = []
            for j in range(0,24):
                hourdict = {}
                hourdict["fxTime"] = day +"T"+ "%02d"%j +":00+08:00"
                hourdict["height"] = list2[j * n2 + i]
                tidehour.append(hourdict)
            datadict["tideHourly"] = tidehour

    else:
        print ("wrong")
        print (len(list2))


    for dict in list:
        day = dict["day"]
        filename = day.replace("-","") +"_" + "P0000"
        resultpath = os.path.join(basedir, "static/chaoxibiao/shantou/03",filename )
        datadict = dict[x_data]
        result = {}
        result[x_code] = 200
        result[x_data]  =datadict
        jdata = json.dumps(result).encode("utf8")
        fw = open(resultpath, "w")
        fw.write(jdata)
        fw.close()


    return json.dumps(list)



@api3.route("/hefeng/storm/list")
def hefengstormlist():
    basin = request.args.get("basin","NP")

    lang = request.args.get("lang", "zh")
    year = request.args.get("year","2023")
    result = {}
    try:
        response = requests.get(
            'https://api.qweather.com/v7/tropical/storm-list',
            params={

                "key":hefengfishingapikey,
                "lang":lang,
                "basin":basin,
                "year": year
            },

        )



        json_data = response.json()

        list = json_data["storm"]

        result[x_data]  = list
        result[x_code] = 200

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
    return json.dumps(result)


@api3.route("/hefeng/storm/forecast")
def hefengstormforecast():
    stormid = request.args.get("stormid","NP_2305")

    lang = request.args.get("lang", "zh")

    result = {}

    try:
        response = requests.get(
            'https://api.qweather.com/v7/tropical/storm-forecast',
            params={

                "key":hefengfishingapikey,
                "lang":lang,
                "stormid": stormid,

            },

        )
        json_data = response.json()

        result[x_code]  = 200
        result[x_data] = json_data["forecast"]

    except Exception as e:
        result[x_code] = 200
        result[x_meesage] = "%s"%e
    return  json.dumps(result)

@api3.route("/hefeng/storm/track")
def hefengstormtrack():
    stormid = request.args.get("stormid","NP_2305")

    lang = request.args.get("lang", "zh")
    result = {}

    try:
        response = requests.get(
            'https://api.qweather.com/v7/tropical/storm-track',
            params={

                "key":hefengfishingapikey,
                "lang":lang,
                "stormid": stormid,

            },

        )



        json_data = response.json()

        result[x_code] = 200
        datadict = {}
        datadict["track"] = json_data["track"]
        if "now" in json_data:
            datadict["now"] = json_data["now"]
        result[x_data] = datadict
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return  json.dumps(result)


@api3.route("/hefeng/minute")
def hefeingminute():
    lat = request.args.get("lat","30.2872")
    lng = request.args.get("lng","119.9870")
    location = lng + "," + lat

    lang = request.args.get("lang", "zh")

    result = {}

    try:
        response = requests.get(
            'https://api.qweather.com/v7/minutely/5m',
            params={

                "key":hefengfishingapikey,
                "lang":lang,
                "location":location,

            },

        )



        json_data = response.json()

        result[x_code] = 200
        result[x_data] = json_data



        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


