#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
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

import gzip
from app.utils.constvalue import acuuappkey,accu_minutecastkey
import metpy.calc as mpcalc
from metpy.units import units
import gzip
import requests
from io import StringIO
# from suncalc import get_position,get_times
import pytz


tz = pytz.timezone("GMT")


@api3.route('/accu/loctionkey')
def acuugetloctionkey():
    lat = request.args.get('lat', '22.24925')
    lng = request.args.get('lng', '113.83667')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    language = request.args.get('language', 'en-us')
    result = {}


    url = 'https://dataservice.accuweather.com/locations/v1/geoposition/search?q='+lat+','+lng +'&language='+language

    # print(url)
    try:

        headers = {"Authorization": "Bearer " + acuuappkey}

        # req = urllib.request.Request(url)
        response = requests.get(url,headers=headers)
        content = response.text
        result[x_code] = 200
        locationlist = json.loads(content)
        result[x_data] = locationlist[0]
        return json.dumps(result)
    except Exception as e:
            result[x_code] = 201
            result[x_meesage] = "%s" % e
            return json.dumps(result)








@api3.route('/accu/location/ges')
def acculocationges():

    language = request.args.get('language', 'zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')


    result = {}


    url = 'https://dataservice.accuweather.com/locations/v1/cities/geoposition/search'+"?q="+lat+','+lng+'&details=true&toplevel=true&language=' + language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

@api3.route('/accu/location/regions')
def acculocationregions():
    result = {}

    language = request.args.get('language', 'zh-cn')

    url = 'https://dataservice.accuweather.com/locations/v1/regions' + '?details=true&language=' + language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)



@api3.route('/accu/location/topcity/<code>')
def acculocationtopcity(code):
    result = {}

    language = request.args.get('language', 'zh-cn')

    url = 'https://dataservice.accuweather.com/locations/v1/topcities/'+code+ '?&details=true&language=' + language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

@api3.route('/accu/location/adminareas/<code>')
def acculocationadminareas(code):
    result = {}

    language = request.args.get('language', 'zh-cn')

    url = 'https://dataservice.accuweather.com/locations/v1/adminareas/'+code+ '?&details=true&language=' + language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

@api3.route('/accu/location/countries/<code>')
def acculocationcountries(code):
    result = {}

    language = request.args.get('language', 'zh-cn')

    url = 'https://dataservice.accuweather.com/locations/v1/countries/'+code+ '?apikey=' + acuuappkey + '&details=true&language=' + language

    try:
        # req = urllib.request.Request(url)

        headers = {"Authorization": "Bearer " + acuuappkey}
        response = requests.get(url,headers=headers)
        content = response.text
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route('/accu/location/city')
def acculocationcity():

    language = request.args.get('language', 'en-us')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    q = request.args.get("key","beijing")
    # q = q.encode()

    result = {}


    url = "https://dataservice.accuweather.com/locations/v1/cities/search?"+"&q=" + q +"&details=true&language=" + language


    try:
        headers = {"Authorization": "Bearer " + acuuappkey}
        response = requests.get(url,headers=headers)
        content = response.text
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route('/accu/city/search')
def accucitysearch():
    language = request.args.get('language', 'zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    key = request.args.get("key", "纽约")

    q = key.encode('utf8')


    result = {}


    try:
        headers = {"Authorization": "Bearer " + acuuappkey}
        response = requests.get(
            'https://dataservice.accuweather.com/locations/v1/cities/search',
            params={
                 "details":"false",
                 "language":language,
                  "q":q
            },
            headers=headers
        )

        # Do something with response data.
        json_data = response.json()


        result[x_code] = 200
        result[x_data] = json_data
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route('/accu/location/text')
def acculocationtext():

    language = request.args.get('language', 'zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    key = request.args.get("key","beijing")

    q = key.encode('utf8')

    result = {}



    try:
        headers = {"Authorization": "Bearer " + acuuappkey}
        response = requests.get(
            'https://dataservice.accuweather.com/locations/v1/search',
            params={

                "details": "false",
                "language": language,
                "q": q

            },
            headers=headers
        )

        json_data = response.json()

        if len(json_data) > 0:

            result[x_code] = 200
            result[x_data] = json_data
        else:
            result[x_code] = 201
            result[x_meesage] = "No Data"



        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)




@api3.route('/acuu/weather')
def accuuweather():
    locationkey = request.args.get('locationkey',"2333331")
    language = request.args.get('language','en-us')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    ismetric = request.args.get("metric", "false")

    result = {}


    url = 'https://dataservice.accuweather.com/forecasts/v1/daily/5day/'+locationkey+'?'+'&details=true&metric='+ismetric+'&language='+language

    try:
        headers = {"Authorization": "Bearer " + acuuappkey}
        response = requests.get(url,headers=headers)
        content = response.text
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route('/accu/1hour')
def accuu1hourl():
    locationkey = request.args.get('locationkey',"355574")
    language = request.args.get('language', 'zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    ismetric = request.args.get("metric", "false")

    result = {}


    url = 'https://dataservice.accuweather.com/forecasts/v1/hourly/1hour/' + locationkey + '?details=true&metric=' + ismetric + '&language=' + language

    try:
        headers = {"Authorization": "Bearer " + acuuappkey}

        response = requests.get(url,headers=headers)
        content = response.text
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)




@api3.route('/accu/index')
def accuuindex():
    locationkey = request.args.get('locationkey',"355574")
    language = request.args.get('language','en-us')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}


    url = 'https://dataservice.accuweather.com/indices/v1/daily/5day/'+locationkey+'?details=true&language='+language

    try:
        req = urllib.request.Request(url)
        req.add_header('Accept-Encoding', 'gzip')
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        return content
    except Exception as e:
        return "%s" % e


@api3.route('/accu/spot/index')
def accuuspotindex():
    locationkey = request.args.get('locationkey',"355574")
    language = request.args.get('language','en-us')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}

    url = 'https://dataservice.accuweather.com/indices/v1/daily/5day/'+locationkey+'/groups/12?&details=true&language='+language

    list = []

    listid = [1, 3, 4, 5]




    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)

        content = response.read()

        contentlist = json.loads(content)
        for cdict in contentlist:
            ID = cdict["ID"]
            if ID in listid:
                list.append(cdict)


        result[x_code] = 200
        result[x_data] = list
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage]  = "%s" % e
        return json.dumps(result)



@api3.route('/accu/health/index')
def accuhealthindex():
    locationkey = request.args.get('locationkey',"355574")
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}
    # code = weatherchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
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

    # url = 'http://dataservice.accuweather.com/indices/v1/daily/5day/'+locationkey+'/groups/10'+'?apikey=' +acuuappkey+'&details=true&language='+language

    url = 'https://dataservice.accuweather.com/indices/v1/daily/5day/' + locationkey + '?details=true&language=' + language


    list = []

    listid = [21, 23, 25, 44, 27, 30]


    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)

        response = urllib.request.urlopen(req)

        # req.add_header('Accept-Encoding', 'gzip')
        content = response.read()
        indicelist = json.loads(content)
        for dict in indicelist:

            ID = dict["ID"]

            for id in listid:
                if ID == id:
                    newdict = {}
                    newdict["indice_id"] = dict["ID"]
                    newdict["value"] = dict["Value"]
                    newdict["name"]= dict["Name"]
                    newdict["time"] = dict["LocalDateTime"]
                    newdict["grade_value"] = dict["CategoryValue"]
                    newdict["grade"] = dict["Category"]
                    newdict["text"] = dict["Text"]
                    newdict["ascending"] = dict["Ascending"]
                    newdict["timestemp"] = dict["EpochDateTime"]
                    list.append(newdict)
                    break


        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        print(e)
        print(dir(e))
        result[x_code] = 201
        result[x_meesage]  = "%s" % e
    return json.dumps(result)




# def gzip_decompress(buf):
#     obj = StringIO.StringIO(buf)
#     with gzip.GzipFile(fileobj=obj) as f:
#         result = f.read()
#     return result






@api3.route('/accu/current')
def accuucurrent():
    locationkey = request.args.get('locationkey',"355574")
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '30.513')
    lng = request.args.get('lng', '120.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    elevation = request.args.get("elevation","0")

    result = {}


    url = 'https://dataservice.accuweather.com/currentconditions/v1/'+locationkey+'?apikey=' +acuuappkey+'&details=true&language='+language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        datalist = json.loads(content)
        # for datadict in datalist:
        #     epoctime = int(datadict["EpochTime"])
        #     forecasttime = datetime.datetime.fromtimestamp(epoctime,tz=tz)
        #     sun_position = get_position(forecasttime,float(lng),float(lat))
        #     sun_altitude = sun_position["altitude"]
        #     datadict["SunAltitude"] = sun_altitude * 180.0 / math.pi
        #     datadict["ClearSkyUV"] = estimatecleaskuv(sun_altitude,float(elevation))
        result[x_data] = datalist
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

def estimatecleaskuv(sunAltitude, elevation):
    elevationFactor = 1 + 0.1 * (elevation / 1000.0)
    clearSkyUV = 12.5 * math.sin(sunAltitude) * elevationFactor
    if clearSkyUV < 0:
        return 0
    return clearSkyUV


@api3.route('/accu/history')
def accuuhistory():
    locationkey = request.args.get('locationkey',"61653")
    language = request.args.get('language', 'zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}


    url = 'https://dataservice.accuweather.com/currentconditions/v1/' + locationkey + '/historical/24?apikey=' + acuuappkey + '&details=true&language=' + language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route('/accu/hourly')
def accuuhourly():
        locationkey = request.args.get('locationkey')
        language = request.args.get('language', 'zh-cn')

        lat = request.args.get('lat', '37.513')
        lng = request.args.get('lng', '122.12')
        timestamp = request.args.get('time', '1550069439')
        total = request.args.get('total', '1599918717')
        ismetric = request.args.get("metric", "false")
        elevation = request.args.get("elevation","0")

        result = {}


        url = 'https://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + locationkey + '?details=true&metric=' + ismetric + '&language=' + language

        try:
            req = urllib.request.Request(url)
            req.add_header("Authorization", "Bearer " + acuuappkey)
            response = urllib.request.urlopen(req)
            content = response.read()
            result[x_code] = 200
            datalist = json.loads(content)
            # for datadict in datalist:
            #     epoctime = int(datadict["EpochDateTime"])
            #     forecasttime = datetime.datetime.fromtimestamp(epoctime, tz=tz)
            #     sun_position = get_position(forecasttime, float(lng), float(lat))
            #     sun_altitude = sun_position["altitude"]
            #     datadict["SunAltitude"] = sun_altitude * 180.0 / math.pi
            #     datadict["ClearSkyUV"] = estimatecleaskuv(sun_altitude, float(elevation))
            result[x_data] = datalist
            return json.dumps(result)
        except Exception as e:

            result[x_code] = 201
            result[x_meesage] = "%s" % e
            return json.dumps(result)


@api3.route('/accu/radar')
def accuuradar():
    locationkey = request.args.get('locationkey',"6165")
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    image = request.args.get('image', '1024x1024')

    result = {}


    url = 'https://dataservice.accuweather.com/imagery/v1/maps/radsat/'+image+'/'+locationkey+'?details=true&language='+language


    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

@api3.route('/accu/region')
def accuregion():
    locationkey = request.args.get('locationkey')
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}


    url = 'https://dataservice.accuweather.com/locations/v1/regions?details=true&language='+language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

@api3.route('/accu/country')
def accucountry():
    locationkey = request.args.get('locationkey')
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    region = request.args.get('region','ASI')

    result = {}


    url = 'https://dataservice.accuweather.com/locations/v1/countries/'+region+'?details=true&language='+language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)
@api3.route('/accu/area')
def accuarea():
    locationkey = request.args.get('locationkey')
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    country = request.args.get('country','CN')

    result = {}


    url = 'https://dataservice.accuweather.com/locations/v1/adminareas/'+country+'?details=true&language='+language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)

@api3.route('/accu/city')
def accucity():
    locationkey = request.args.get('locationkey')
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')
    group = request.args.get('group','150')

    result = {}


    url = 'https://dataservice.accuweather.com/locations/v1/topcities/'+group+'?details=true&language='+language

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)


@api3.route('/accu/alarms')
def accuualarms():
    locationkey = request.args.get('locationkey')
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}


    url = 'https://dataservice.accuweather.com/alarms/v1/1day/'+locationkey+'?details=true&language='+language

    # print url

    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + acuuappkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
        return json.dumps(result)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e
        return json.dumps(result)



@api3.route('/accu/minutecast')
def accuminutecast():
    # locationkey = request.args.get('locationkey')
    language = request.args.get('language','zh-cn')

    lat = request.args.get('lat', '45.013')
    lng = request.args.get('lng', '122.35')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    result = {}


    url = 'https://dataservice.accuweather.com/forecasts/v1/minute?q='+lat+","+lng+"&language="+language



    try:
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + accu_minutecastkey)
        response = urllib.request.urlopen(req)
        content = response.read()
        result[x_code] = 200
        result[x_data] = json.loads(content)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s" % e


    return json.dumps(result)
