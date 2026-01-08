#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage,hefengtyphoonkey,xinzhi_prinvate_key,hefeng_apihost
from flask import request,session,url_for,redirect
import time
import datetime


import json

import math
import requests
from .Hgt import  get_elavation
from config import basedir
from app.Hefengtide import Hefengtide
import xlrd
from app.TyphoonModel import TyphoonModel
import pytz

from app.HefengJWTConfig import HefengJWTConfig


hefengjwtconfig = HefengJWTConfig()


@api3.route("/hefeng/cid/location")
def hefengcid_location():
    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.0')
    lang = request.args.get("lang","zh")

    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    # starttime = request.args.get('starttime', '1585929600')
    result = {}

    try:
        response = requests.get(
            "https://"+hefeng_apihost+"/v2/city/lookup",
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={
                "location":lng+","+lat,
                "lang":lang
            },

        )


        json_data = response.json()



        heweatherarry = json_data["location"]

        # dataarray = dict["basic"]
        #
        for dict in heweatherarry:
            dict["elevation"] = get_elavation(float(dict["lon"]),float(dict["lat"]))


        result[x_code] = 200
        result[x_data] = heweatherarry
    except Exception as e:
        print(e)
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)

@api3.route("/hefeng/tid/search")
def hefengtid_seach():
    location = request.args.get("location","海门")
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    lang = request.args.get("lang", "zh")
    try:
        response = requests.get(
            'https://'+hefeng_apihost+'/v2/poi/lookup',
            params={
                "location":location,
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



@api3.route("/hefeng/cid/search")
def hefengcid_seach():
    key = request.args.get("key","beijing")
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    lang = request.args.get("lang", "zh")
    # starttime = request.args.get('starttime', '1585929600')
    result = {}

    try:
        response = requests.get(
            'https://'+hefeng_apihost+'/v2/city/lookup',
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={
                "location":key,

                "lang":lang
            },

        )

        json_data = response.json()

        heweatherarry = json_data["location"]


        for dict in heweatherarry:
            dict["elevation"] = get_elavation(float(dict["lon"]),float(dict["lat"]))



        result[x_code] = 200
        result[x_data] = heweatherarry
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)




@api3.route("/weather/hefeng/rain")
def hefengrain():
    lat = request.args.get('lat', '30.28')
    lng = request.args.get('lng', '120.05')
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    elavation = request.args.get("elavation", "6")
    cid = request.args.get("cid", "8238D")
    date = request.args.get('date', '20201102')
    result = {}


    try:
        response = requests.get(
            'https://'+hefeng_apihost+'/v7/minutely/5m',
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={
                "location": lng+","+lat,
                "key": hefengtyphoonkey,

            },

        )

        # print  response

        # Do something with response data.
        json_data = response.json()

        # print json_data

        result[x_code] = 200
        result[x_data] = json_data
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


@api3.route("/weather/hefeng/tide/group")
def hefengtidegroup():
    lat = request.args.get('lat', '30.28')
    lng = request.args.get('lng', '120.05')
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    datestring = request.args.get('date', '20230224,20230225,20230226')
    fixday = request.args.get("fixday","20230226")
    location = request.args.get("location","P2671")
    code = request.args.get("code","T131")

    result = {}



    dates = datestring.split(",")

    list = []

    try:
        for dateitem in dates:
            filename = dateitem + "_" + location
            tidepath = os.path.join(basedir, "static/hefengtide", filename)
            if os.path.exists(tidepath):
                try:
                    f = open(tidepath,"r")
                    jdata = f.read()
                    f.close()
                    jdict = json.loads(jdata)
                    list.append(jdict[x_data])

                except Exception as e:

                    print(e)
            else:
                if location == "P0000":
                    shantouencrypt
                    try:
                        f = open(tidepath, "r")
                        jdata = f.read()
                        f.close()
                        jdict = json.loads(jdata)
                        list.append(jdict[x_data])

                    except Exception as  e:

                        print(e)

                else:
                    subresult = {}
                    response = requests.get(
                        'https://'+hefeng_apihost+'/v7/ocean/tide',
                        headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
                        params={
                            "location": location,

                            "date":dateitem
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


                        subresult[x_code] = 200
                        subresult[x_data] = json_data
                        list.append(json_data)

                        try:

                            jdata = json.dumps(subresult)
                            fw = open(tidepath,"w")
                            fw.write(jdata)
                            fw.close()
                        except Exception as e:

                            print(e)
                    else:
                        result[x_code] = 201
                        result[x_meesage] = "没有数据2"
                        return json.dumps(result)

            result[x_code] = 200
            result[x_data] = list


    except Exception as  e:

            result[x_meesage] = "%s" %e
            result[x_code] = 201
    return json.dumps(result)



@api3.route("/weather/hefeng/tide")
def hefengtide():
    lat = request.args.get('lat', '30.28')
    lng = request.args.get('lng', '120.05')
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    date = request.args.get('date', '20250401')
    location = request.args.get("location","P2352")
    code = request.args.get("code","T132")
    fixday = request.args.get("fixday", "20230326")
    result = {}
    filename = date+"_"+location
    tidepath = os.path.join(basedir,"static/hefengtide",filename)
    tiledirecoty = os.path.join(basedir,"static/hefengtide")
    if os.path.exists(tiledirecoty):
        pass
    else:
        os.mkdir(tiledirecoty)

    try:
        if os.path.exists(tidepath):
            try:
                f = open(tidepath,"r")
                jdata = f.read()
                f.close()
                return jdata
            except Exception as e:
                result[x_meesage] = "%s"%e
                result[x_code] = 201
        else:

            if location == "P0000":
                shantouencrypt()
                if os.path.exists(tidepath):
                    try:
                        f = open(tidepath, "r")
                        jdata = f.read()
                        f.close()
                        return jdata
                    except Exception as  e:
                        result[x_meesage] = "%s" %e
                        result[x_code] = 201

            else:

                response = requests.get(
                    'https://'+hefeng_apihost+'/v7/ocean/tide',
                    headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
                    params={
                        "location": location,

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


                    result[x_code] = 200
                    result[x_data] = json_data

                    try:

                        jdata = json.dumps(result)
                        fw = open(tidepath,"w")
                        fw.write(jdata)
                        fw.close()
                    except Exception as e:
                        print(e)
                else:
                    result[x_code] = 201
                    result[x_meesage] = "没有数据"


    except Exception as  e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


@api3.route("/shantou/encypt")
def shantouencrypt():
    try:
        xinzhiport = "WS5HB68PW5KX"

        response = requests.get(
            'https://api.seniverse.com/v3/tide/daily.json',
            params={
                "port": xinzhiport,
                "key": xinzhi_prinvate_key

            },

        )

        contentdict = response.json()





        list = []
        datadict = contentdict['results'][0]
        for dict in datadict["data"]:
            # print dict
            if "range" in dict and len(dict["range"]) > 0:
                list.append(dict)
        for xdict in list:

            hefengresult = {}
            hefengresult[x_code] = 200
            hefengdict = {}
            hefengdict["code"] = "200"
            tides = xdict["tide"]
            hour = len(tides)
            xdate = xdict["date"]
            tideHourly = []
            for i in range(0, hour):
                hourdict = {}
                hourdict["fxTime"] = "%sT%02d:00+08:00" % (xdate, i)
                tide = tides[i]

                hourdict["height"] = "%.2f" % (float(tide) / 100.0)
                tideHourly.append(hourdict)
            hefengdict["tideHourly"] = tideHourly
            xrange = xdict["range"]
            tideTable = []
            for xrdict in xrange:
                exdict = {}
                exdict["type"] = xrdict["type"][0:1].upper()
                height = xrdict["height"]
                exdict["height"] = "%.2f" % (float(height) / 100.0)
                time = xrdict["time"][:-9] + "+08:00"
                exdict["fxTime"] = time
                tideTable.append(exdict)
            hefengdict["tideTable"] = tideTable
            hefengresult[x_data] = hefengdict

            try:
                filename = xdate.replace("-","")  +"_" + "P0000"
                tidepath = os.path.join(basedir, "static/hefengtide", filename)

                jdata = json.dumps(hefengresult)
                fw = open(tidepath, "w")
                fw.write(jdata)
                fw.close()
            except Exception as  e:

                print (e)

    except Exception as e:

        print(e)


@api3.route("/hefeng/tide/locations")
def hefengtidelocations():
    list = ["P0000","P2102", "P2109", "P2113", "P2115", "P2117", "P2121", "P2122", "P2126", "P2131", "P2134", "P2137", "P2143", "P2146", "P2149", "P2159", "P2168", "P2169", "P2172", "P2177", "P2180", "P2197", "P2205", "P2225", "P2232", "P2236", "P2240", "P2243", "P2244", "P2246", "P2257", "P2259", "P2260", "P2275", "P2284", "P2285", "P2286", "P2288", "P2289", "P2299", "P2304", "P2305", "P2306", "P2313", "P2314", "P2327", "P2334", "P2337", "P2340", "P2350", "P2351", "P2352", "P2357", "P2362", "P2364", "P2372", "P2398", "P2409", "P2410", "P2411", "P2414", "P2418", "P2419", "P2423", "P2426", "P2428", "P2429", "P2432", "P2436", "P2440", "P2442", "P2447", "P2450", "P2454", "P2461", "P2462", "P2474", "P2483", "P2488", "P2490", "P2494", "P2499", "P2510", "P2512", "P2513", "P2519", "P2523", "P2528", "P2532", "P2533", "P2536", "P2537", "P2539", "P2543", "P2554", "P2558", "P2559", "P2560", "P2563", "P2566", "P2570", "P2575", "P2578", "P2582", "P2584", "P2585", "P2587", "P2590", "P2591", "P2598", "P2602", "P2609", "P2612", "P2619", "P2620", "P2621", "P2627", "P2633", "P2643", "P2646", "P2647", "P2651", "P2652", "P2653", "P2659", "P2664", "P2669", "P2671", "P2672", "P2680", "P2683", "P2689", "P2692", "P2699", "P2709", "P2712", "P2717", "P2727", "P2728", "P2735", "P2737", "P2738", "P2739", "P2743", "P2750", "P2751", "P2761", "P2764", "P2769", "P2774", "P2780", "P2781", "P2785", "P2792", "P2793", "P2794", "P2799", "P2801", "P2806", "P2816", "P2822", "P2825", "P2827", "P2830", "P2835", "P2848", "P2849", "P2862", "P2864", "P2872", "P2880", "P2885", "P2886", "P2890", "P2891", "P2892", "P2894", "P2895", "P2903", "P2908", "P2912", "P2916", "P2919", "P2926", "P2929", "P2931", "P2932", "P2938", "P2939", "P2943", "P2944", "P2945", "P2951", "P2953", "P2962", "P2966", "P2967", "P2980", "P2982", "P2992", "P2998"]

    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.datetime.now(tz)
    date = "%d%02d%02d"%(now.year,now.month,now.day)

    for location in list:
        time.sleep(1)
        filename = date+"_"+location
        tidepath = os.path.join(basedir,"static/hefengtide",filename)

        try:
            if os.path.exists(tidepath):
                pass
            else:
                if location == "P0000":
                    shantouencrypt
                else:
                    response = requests.get(
                        'https://'+hefeng_apihost+'/v7/ocean/tide',
                        headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
                        params={
                            "location": location,

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

                            jdata = json.dumps(result)
                            fw = open(tidepath,"w")
                            fw.write(jdata)
                            fw.close()
                        except Exception as e:
                            print(e)
        except  Exception  as e:
            print(e)


def hefengchecklatandlon(lat,lng,timestamp,total):
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



@api3.route("/hefeng/storm/list")
def hefengstormlist():
    basin = request.args.get("basin","NP")

    lang = request.args.get("lang", "zh")
    year = request.args.get("year","2025")
    time = request.args.get("time","0")

    listpath = os.path.join(basedir, "static/typhoon/list", time)

    direcorypath = os.path.join(basedir, "static/typhoon/list")
    if os.path.exists(direcorypath):
        pass
    else:
        os.mkdir(direcorypath)

    result = {}

    if os.path.exists(listpath):
        try:
            f = open(listpath, "r")
            jdata = f.read()
            f.close()
            return jdata
        except Exception as  e:
            result[x_meesage] = "%s"%e
            result[x_code] = 201
    else:
        pass

    try:
        response = requests.get(
            'https://'+hefeng_apihost+'/v7/tropical/storm-list',
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={

                "lang":lang,
                "basin":basin,
                "year": year
            },

        )



        json_data = response.json()

        list = json_data["storm"]

        resultList = []
        for dict in list:
            isactivate = dict["isActive"]
            if "1" == isactivate:
                resultList.append(dict)
        for dict in list:
            isactivate = dict["isActive"]
            if "0" == isactivate:
                resultList.append(dict)


        result[x_data]  = resultList
        result[x_code] = 200

        try:
            jdata = json.dumps(result)
            fw = open(listpath, "w")
            fw.write(jdata)
            fw.close()
        except Exception as  e:

            print(e)

    except Exception as e:
        listpath = os.path.join(basedir, "static/typhoon/list", "0")
        if os.path.exists(listpath):
            try:
                f = open(listpath, "r")
                jdata = f.read()
                f.close()
                return jdata
            except Exception as e:
                result[x_meesage] = "%s" % e
                result[x_code] = 201
        else:
            result[x_meesage] = "%s" % e
            result[x_code] = 201
    return json.dumps(result)


@api3.route("/hefeng/storm/forecast")
def hefengstormforecast():
    stormid = request.args.get("stormid","NP_2305")

    lang = request.args.get("lang", "zh")
    # time = request.args.get("time","0")

    timestamp = int(datetime.datetime.now().timestamp())
    hourtime = timestamp - timestamp % 3600

    time = str(hourtime)


    filename = stormid + "_" + time

    listpath = os.path.join(basedir, "static/typhoon/forecast", filename)

    direcorypath = os.path.join(basedir, "static/typhoon/forecast")
    if os.path.exists(direcorypath):
        pass
    else:
        os.mkdir(direcorypath)

    result = {}

    if os.path.exists(listpath):
        try:
            f = open(listpath, "r")
            jdata = f.read()
            f.close()
            return jdata
        except Exception as e:
            result[x_meesage] = "%s" %e
            result[x_code] = 201
    else:
        pass

    try:
        response = requests.get(
            'https://'+hefeng_apihost+'/v7/tropical/storm-forecast',
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={

                "lang":lang,
                "stormid": stormid,

            },

        )

        json_data = response.json()

        result[x_code]  = 200
        result[x_data] = json_data["forecast"]

        try:
            jdata = json.dumps(result)
            fw = open(listpath, "w")
            fw.write(jdata)
            fw.close()
        except Exception as  e:

            print(e)



    except Exception as e:
        result[x_code] = 200
        result[x_meesage] = "%s"%e
    return  json.dumps(result)

@api3.route("/hefeng/storm/track")
def hefengstormtrack():
    stormid = request.args.get("stormid","NP_2305")

    lang = request.args.get("lang", "zh")
    result = {}

    deactivatepath = os.path.join(basedir,"static/typhoon/deactivate",stormid)
    isactive = request.args.get("isactive","0")


    time = request.args.get("time", "0")

    filename = stormid + "_" + time

    listpath = os.path.join(basedir, "static/typhoon/activate", filename)

    direcorypath = os.path.join(basedir, "static/typhoon/deactivate")
    if os.path.exists(direcorypath):
        pass
    else:
        os.mkdir(direcorypath)

    direcorypath1 = os.path.join(basedir, "static/typhoon/activate")
    if os.path.exists(direcorypath1):
        pass
    else:
        os.mkdir(direcorypath1)



    if "1" == isactive :
        if os.path.exists(listpath):
            try:
                f = open(listpath, "r")
                jdata = f.read()
                f.close()
                return jdata
            except Exception as  e:
                result[x_meesage] = "%s" %e
                result[x_code] = 201
        else:
            pass
    else:
        if os.path.exists(deactivatepath):
            try:
                f = open(deactivatepath, "r")
                jdata = f.read()
                f.close()
                return jdata
            except Exception as  e:
                result[x_meesage] = "%s" %e
                result[x_code] = 201
        else:
            pass




    try:
        response = requests.get(
            'https://'+hefeng_apihost+'/v7/tropical/storm-track',
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={

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

        try:
            if "1" == isactive:
                jdata = json.dumps(result)
                fw = open(listpath, "w")
                fw.write(jdata)
                fw.close()
            else:
                jdata = json.dumps(result)
                fw = open(deactivatepath, "w")
                fw.write(jdata)
                fw.close()
        except Exception as  e:

            print(e)

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
             "https://"+hefeng_apihost +'/v7/minutely/5m',
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={

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


@api3.route("/hefeng/now")
def hefeingnow():
    lat = request.args.get("lat","30.2872")
    lng = request.args.get("lng","119.9870")
    location = lng + "," + lat

    lang = request.args.get("lang", "zh")

    result = {}

    try:
        response = requests.get(
            "https://" + hefeng_apihost +"/v7/weather/now",
            headers={"Authorization": ("Bearer " + hefengjwtconfig.genToken())},
            params={

                "lang":lang,
                "location":location,
                "unit":"i"

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

