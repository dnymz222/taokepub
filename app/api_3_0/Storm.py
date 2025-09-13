#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,stormmglassapikey

from flask import request
from app import db


import time
import datetime

import json

import math
import requests
from app.StormStation import StormStation

@api3.route("/storm/weather")
def  stormweather():
    lat = request.args.get('lat', '29.361')
    lng = request.args.get('lng', '91.06')
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    starttime = request.args.get('starttime', '1637596800')
    isvip = request.args.get("isvip","0")
    days = 5
    if isvip == "1":
        days = 10
    result = {}

    code = stormchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
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

    try:

        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat':lat,
                'lng': lng,
                'params': ','.join(["airTemperature","humidity","windDirection","windSpeed","pressure","precipitation","cloudCover","visibility"]),
                'start': starttime , # Convert to UTC timestamp
                'end':int(starttime)+days*86400,  # Convert to UTC timestamp
                'source':"noaa"
            },
            headers={
                'Authorization': stormmglassapikey
            }
        )

        json_data = response.json()
        result[x_code] = 200
        list = json_data["hours"]
        for dict1 in  list:
            for key in dict1.keys():
                dict0 = dict1[key]
                if type(dict0) is dict:
                    value = valuefromdict(dict=dict0)
                    dict1[key] = value

        result[x_data] = list

    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)

@api3.route("/storm/wave")
def stormwave():
        lat = request.args.get('lat', '16.8')
        lng = request.args.get('lng', '112.34')
        timestamp = request.args.get('time', '1585843200')
        starttime = request.args.get('starttime', '1585929600')
        total = request.args.get('total', '1599918717')
        result = {}

        # code = stormchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
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

            response = requests.get(
                'https://api.stormglass.io/v2/weather/point',
                params={
                    'lat': lat,
                    'lng': lng,
                    'params': ','.join(
                        ["seaLevel",
                         "waterTemperature", 'waveHeight', "waveDirection", "wavePeriod", 'swellDirection', "swellHeight",
                         "swellPeriod", "windWaveHeight", "windWavePeriod", "windWaveDirection","iceCover","pressure","airTemperature","gust","humidity","precipitation","secondarySwellPeriod","secondarySwellDirection","secondarySwellHeight","windSpeed","currentDirection","currentSpeed","windDirection","visibility","cloudCover"]),
                    'start': starttime,  # Convert to UTC timestamp
                    'end': int(starttime) + 7 * 86400  # Convert to UTC timestamp
                },
                headers={
                    'Authorization': stormmglassapikey
                }
            )

            json_data = response.json()

            result[x_code] = 200
            list = json_data["hours"]
            for dict1 in list:

                for key in dict1.keys():

                    dict0 = dict1[key]

                    if type(dict0) is dict:
                        value = valuefromdict(dict=dict0)
                        dict1[key] = value

            result[x_data] = list

        except Exception as e:

            result[x_meesage] = "%s"%e
            result[x_code] = 201

        return json.dumps(result)

@api3.route("/storm/surge/wave")
def stormsurgewave():
        lat = request.args.get('lat', '16.8')
        lng = request.args.get('lng', '112.34')
        timestamp = request.args.get('time', '1585843200')
        starttime = request.args.get('starttime', '1689436800')
        total = request.args.get('total', '1599918717')
        result = {}

        try:

            response = requests.get(
                'https://api.stormglass.io/v2/weather/point',
                params={
                    'lat': lat,
                    'lng': lng,
                    'params': ','.join(
                        [
                         "waterTemperature", 'waveHeight', "waveDirection", "wavePeriod", 'swellDirection', "swellHeight","currentDirection","currentSpeed",
                         "swellPeriod", "windWaveHeight", "windWavePeriod", "windWaveDirection","iceCover","secondarySwellPeriod","secondarySwellDirection","secondarySwellHeight"]),
                    'start': starttime,  # Convert to UTC timestamp
                    'end': int(starttime) + 7 * 86400  # Convert to UTC timestamp
                },
                headers={
                    'Authorization': stormmglassapikey
                }
            )

            json_data = response.json()

            result[x_code] = 200
            list = json_data["hours"]
            nlist = []
            for dict1 in list:

                for key in dict1.keys():

                    dict0 = dict1[key]

                    if type(dict0) is dict:
                        value = valuefromdict(dict=dict0)
                        dict1[key] = value
                ndict = stormsurgemapdict(dict1)
                nlist.append(ndict)

            result[x_data] = nlist

        except Exception as e:

            result[x_meesage] = "%s"%e
            result[x_code] = 201

        return json.dumps(result)

    # return json_data


@api3.route("/storm/surge/bio")
def stormsurgebio():
    lat = request.args.get('lat', '16.8')
    lng = request.args.get('lng', '112.34')
    timestamp = request.args.get('time', '1585843200')
    starttime = request.args.get('starttime', '1585929600')
    total = request.args.get('total', '1599918717')
    result = {}
    try:
        response = requests.get(
            'https://api.stormglass.io/v2/bio/point',
            params={
                'lat': lat,
                'lng': lng,
                'params': ','.join(['iron', 'nitrate',"salinity","ph","silicate","oxygen","chlorophyll","phyto","phytoplankton","phosphate"]),
                'start': starttime,  # Convert to UTC timestamp
                'end': int(starttime)+ 7*86400  # Convert to UTC timestamp
            },
            headers={
                'Authorization': stormmglassapikey
            }
        )

        # Do something with response data.
        json_data = response.json()
        result[x_code] = 200
        list = json_data["hours"]

        for dict1 in list:

            for key in dict1.keys():

                dict0 = dict1[key]

                if type(dict0) is dict:
                    value = biovaluefromdict(dict=dict0)
                    dict1[key] = value
        result[x_data] = list

    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)

@api3.route("/storm/stationlist")
def stormstationlist():


    response = requests.get(
        'https://api.stormglass.io/v2/tide/stations',
        headers={
            'Authorization': stormmglassapikey
        }
    )

    # Do something with response data.
    json_data = response.json()
    return json.dumps(json_data)
    list = json_data["data"]
    n = len(list)
    for i in range(0,n):
        dict = list[i]
        stormobject = StormStation(dict = dict)
        try:
            db.session.add(stormobject)
            db.session.commit()
        except Exception as e:

            db.session.rollback()


    db.session.close()
    return json.dumps(json_data)


@api3.route("/storm/bio")
def stormbio():
    lat = request.args.get('lat', '16.8')
    lng = request.args.get('lng', '112.34')
    timestamp = request.args.get('time', '1585843200')
    starttime = request.args.get('starttime', '1585929600')
    total = request.args.get('total', '1599918717')
    result = {}

    # code = stormchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
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
        response = requests.get(
            'https://api.stormglass.io/v2/bio/point',
            params={
                'lat': lat,
                'lng': lng,
                'params': ','.join(['iron', 'nitrate',"salinity","ph","silicate","oxygen","chlorophyll","phyto","phytoplankton","phosphate"]),
                'start': starttime,  # Convert to UTC timestamp
                'end': int(starttime)+7*86400  # Convert to UTC timestamp
            },
            headers={
                'Authorization': stormmglassapikey
            }
        )

        # Do something with response data.
        json_data = response.json()

        list = json_data["hours"]

        vlist = []
        for dict in list:
            ndict = {}
            for key, value in dict.items():
                try:
                    if key == "time":
                        date_object = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
                        ndict["time"] =  int(date_object.timestamp() + 0.1)

                    else:
                        if "sg" in value:
                            ndict[key] = value["sg"]
                        elif "meto" in value:
                            ndict[key] = value["meto"]
                except :
                    pass
            vlist.append(ndict)
        result[x_code] = 200
        result[x_data] = vlist


    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


def stormchecklatandlon(lat,lng,timestamp,total):
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

@api3.route("/storm/weather/history")
def  stormweatherhistrory():
    lat = request.args.get('lat', '28.481')
    lng = request.args.get('lng', '115.153')
    timestamp = request.args.get('time', '1585929600')
    total = request.args.get('total', '1599918717')
    starttime = request.args.get('starttime', '1585929600')
    result = {}

    code = stormchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
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

    try:

        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat':lat ,
                'lng': lng,
                'params': ','.join(["airTemperature","humidity","windDirection","windSpeed","pressure","precipitation","cloudCover"]),
                'start': starttime , # Convert to UTC timestamp
                'end':int(starttime)+86400   # Convert to UTC timestamp
            },
            headers={
                'Authorization': stormmglassapikey
            }
        )

        # Do something with response data.
        json_data = response.json()

        result[x_code] = 200
        list = json_data["hours"]
        for dict1 in  list:
            # print dict
            # print type(dict)

            for key in dict1.keys():

                dict0 = dict1[key]

                if type(dict0) is dict:
                    value = valuefromdict(dict=dict0)
                    dict1[key] = value

        result[x_data] = list

    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)


def valuefromdict(dict):
    # print jsonstring
    # dict = json.loads(jsonstring)
    if "noaa" in dict:
        value = dict["noaa"]

    else:
        keyitems = list(dict.keys())
        key = keyitems[0]
        value = dict[key]

    return value




def biovaluefromdict(dict):
    # print jsonstring
    # dict = json.loads(jsonstring)
    if "sg" in dict:
        value = dict["sg"]

    else:
        keyitems = list(dict.keys())
        key = keyitems[0]
        value = dict[key]

    return value

def stormsurgemapdict(dict):
    ndict = {}
    ndict["langshi"] = dict["wavePeriod"]
    ndict["langgao"] = dict["waveHeight"]
    ndict["langxiang"] = dict["waveDirection"]
    ndict["shuiwen"] = dict["waterTemperature"]
    ndict["bingai"] = dict["iceCover"]
    ndict["fenglangxiang"] = dict["windWaveDirection"]
    ndict["fenglangshi"] = dict["windWavePeriod"]
    ndict["fenglanggao"] = dict["windWaveHeight"]
    ndict["yongxiang"] = dict["swellDirection"]
    ndict["yongshi"] = dict["swellPeriod"]
    ndict["yonggao"] = dict["swellHeight"]
    ndict["ciyongxiang"] = dict["secondarySwellDirection"]
    ndict["ciyongshi"] = dict["secondarySwellPeriod"]
    ndict["ciyonggao"] = dict["secondarySwellHeight"]
    ndict["yangliusudu"]= dict["currentSpeed"]
    ndict["yangliufangxiang"] = dict["currentDirection"]

    timev = dict["time"]
    date_object = datetime.datetime.strptime(timev, "%Y-%m-%dT%H:%M:%S%z")
    ndict["time"] = int(date_object.timestamp() + 0.1)
    return  ndict
