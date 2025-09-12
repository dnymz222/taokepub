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
from app.utils.constvalue import acuuappkey,meteobule_apikey
import metpy.calc as mpcalc
from metpy.units import units
import gzip
from io import StringIO
import requests
import pytz
from pymeeus.Epoch import Epoch
from pymeeus.Sun import Sun
from pymeeus.Moon import Moon
from pymeeus.Earth import Earth
import pymeeus.Coordinates

from datetime import  datetime,timezone
import time
import shutil




tz = pytz.timezone("GMT")

@api3.route('/aurora/minutes')
def auroraminutessolunar():

    result = {}

    url = "https://www.astronomyobserver.net/api/v3.0/aurora/minutes"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        resultdict = json.loads(content)

        datadict = resultdict[x_data]
        dict= {}
        dict["type"] = ""
        dict["forecast_time"] = datadict["forecast_time"]
        coordinates = datadict["coordinates"]
        keys = coordinates.keys()
        cor = {}
        for key in keys:
            value = coordinates[key]
            cor[int(key)] = value
        dict["coordinates"] = coordinates

        result[x_code] = 200
        result[x_data] = dict
        return json.dumps(result)






        # return json.dumps(dict)
        # coordinates = dict["coordinates"]
        # ftime = dict["Forecast Time"]
        #
        #
        #
        # date = datetime.strptime(ftime, "%Y-%m-%dT%H:%M:%SZ")
        #
        #
        # tz_offset = timezonfoffset()
        #
        # forecast_time = int(date.timestamp()) + tz_offset
        # dict["forecast_time"] = forecast_time
        #
        # dict["solunar"] = pymeeusastrodict(forecast_time)
        #
        # list = []
        # for coordinate in coordinates:
        #     value = coordinate[2]
        #     latitude = coordinate[1]
        #     if value > 0 and abs(latitude) > 10:
        #         list.append(coordinate)
        #
        # coordinatedict = {}
        # # dict["coordinates"] = list
        # for coordinate in list:
        #     lng  = coordinate[0]
        #     if lng > 180:
        #         lng = lng - 360
        #     lat = coordinate[1]
        #     v = coordinate[2]
        #     coordinatedict[str(lat * 360 + lng)] = v
        # dict["coordinates"] = coordinatedict
        #
        # result[x_code] = 200
        # result[x_data] = dict
        # return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/aurora/minutes/solunar')
def auroraminutes():

    result = {}

    url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        dict = json.loads(content)
        coordinates = dict["coordinates"]
        ftime = dict["Forecast Time"]

        tz_offset = timezonfoffset()

        date = datetime.strptime(ftime, "%Y-%m-%dT%H:%M:%SZ")
        dict["forecast_time"] = int(date.timestamp()) + tz_offset
        list = []
        for coordinate in coordinates:
            value = coordinate[2]
            latitude = coordinate[1]
            if value > 0 and abs(latitude) > 10:
                list.append(coordinate)

        coordinatedict = {}
        # dict["coordinates"] = list
        for coordinate in list:
            lng  = coordinate[0]
            lat = coordinate[1]
            if lng > 180:
                lng = lng - 360
            v = coordinate[2]
            coordinatedict[lat * 360 + lng] = v
        dict["coordinates"] = coordinatedict

        result[x_code] = 200
        result[x_data] = dict
        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/aurora/hour')
def aurorhour():

    result = {}
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = json.loads(content)
        datalist = []

        n = len(list)

        now = datetime.now()
        nowtimestamp = now.timestamp()

        for i in range(1,n):
            vlist = list[i]
            datadict = {}
            datadict["time_tag"] = vlist[0]
            datadict["kp"] = vlist[1]
            datadict["observed"] = vlist[2]
            datadict["noaa_scale"] = vlist[3]

            ftime = vlist[0]
            date = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")

            tz_offset = timezonfoffset()

            forecast_time = int(date.timestamp()) + tz_offset

            if forecast_time > nowtimestamp - 3600 * 4:
                datadict["solunar"] = pymeeusastrodict(forecast_time)
                datadict["forecast_time"] = forecast_time
                datalist.append(datadict)
                datadict1 = {}
                datadict1["solunar"] = pymeeusastrodict(forecast_time + 3600)
                datadict1["forecast_time"] = forecast_time + 3600
                datalist.append(datadict1)

                datadict2 = {}
                datadict2["solunar"] = pymeeusastrodict(forecast_time + 3600 * 2)
                datadict2["forecast_time"] = forecast_time + 3600 * 2
                datalist.append(datadict2)



        result[x_code] = 200
        result[x_data] = datalist



        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/aurora/kp')
def aurorkp():

    result = {}
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = json.loads(content)
        datalist = []

        n = len(list)

        now = datetime.now()
        nowtimestamp = now.timestamp()

        for i in range(1,n):
            vlist = list[i]
            datadict = {}

            datadict["kp"] = float(vlist[1])
            datadict["a_running"] = int(vlist[2])
            datadict["station_count"] = int(vlist[3])

            ftime = vlist[0][:-4]
            date = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")

            tz_offset = timezonfoffset()

            forecast_time = int(date.timestamp()) + tz_offset







        result[x_code] = 200
        result[x_data] = datalist



        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

# @api3.route('/aurora/day')
# def auroraday():
#
#     result = {}
#
#     url = "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt"
#     try:
#         req = urllib.request.Request(url)
#         response = urllib.request.urlopen(req)
#         content = response.read()
#         list = []
#         beigain = False
#
#         for line in content.splitlines():
#             text = line.decode("utf8").strip()
#
#             if beigain:
#                 tlist = text.split(" ")
#                 for t in tlist:
#                     if len(t) > 0:
#                         list.append(t)
#             else:
#                if text.find("NOAA Kp index forecast") > -1:
#                    beigain = True
#         dict  ={}
#         now = datetime.now(tz)
#         year = now.year
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
#          "Aug", "Sep", "Oct", "Nov", "Dec"]
#         monthstr = list[0]
#         month = 1
#         for i in range(1,13):
#             m = months[i-1]
#             if m == monthstr:
#                 month = i
#                 break
#         day = int(list[1])
#
#         startdate = datetime(year, month, day,0,0,0,tzinfo=tz)
#
#         starttime = int(startdate.timestamp())
#         timelist = []
#         for i in range(0,24):
#             timelist.append(starttime + i * 3600 * 3)
#
#         datalist = []
#         for i in range(0,8):
#             datalist.append(float(list[7 + 4 * i]))
#         for i in range(0,8):
#             datalist.append(float(list[8 + 4 * i]))
#         for i in range(0,8):
#             datalist.append(float(list[9 + 4 * i]))
#         dict["kp"] = datalist
#         dict["time"] = timelist
#         result[x_code] = 200
#         result[x_data] = dict
#         return json.dumps(result)
#     except Exception as e:
#
#         result[x_code] = 201
#         result[x_meesage] = "%s"%e
#         return json.dumps(result)


@api3.route('/aurora/day')
def auroraday():

    result = {}

    url = "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = []
        beigain = False

        for line in content.splitlines():
            text = line.decode("utf8").strip()

            if beigain:
                tlist = text.split(" ")
                for t in tlist:
                    if len(t) > 0:
                        list.append(t)
            else:
               if text.find("NOAA Kp index forecast") > -1:
                   beigain = True
        dict  ={}
        now = datetime.now(tz)
        year = now.year
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
         "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthstr = list[0]
        month = 1
        for i in range(1,13):
            m = months[i-1]
            if m == monthstr:
                month = i
                break
        day = int(list[1])

        startdate = datetime(year, month, day,0,0,0,tzinfo=tz)

        starttime = int(startdate.timestamp())
        timelist = []
        for i in range(0,24):
            timelist.append(starttime + i * 3600 * 3)

        datalist = []
        for i in range(0,8):
            datalist.append(float(list[7 + 4 * i]))
        for i in range(0,8):
            datalist.append(float(list[8 + 4 * i]))
        for i in range(0,8):
            datalist.append(float(list[9 + 4 * i]))
        dict["kp"] = datalist
        dict["time"] = timelist
        result[x_code] = 200
        result[x_data] = dict
        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route('/aurora/hpi')
def aurorahpi():

    result = {}

    url = "https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = []
        beigain = False

        tz_offset = timezonfoffset()

        for line in content.splitlines():
            text = line.decode("utf8").strip()

            if beigain:
                tlist = text.split(" ")
                for t in tlist:
                    if len(t) > 0:
                        list.append(t)
            else:
               if text.find("#-------") > -1:
                   beigain = True
        # obtime =[]
        fctime = []
        nhpi = []
        shpi = []
        datadict = {}
        n = int(len(list)/4)
        for i in range(0,n):
            # otime = list[4 * i]
            ftime = list[4*i + 1]
            fdate = datetime.strptime(ftime, "%Y-%m-%d_%H:%M")
            fctime.append(int(fdate.timestamp()) + tz_offset)

            nhpi.append(int(list[4*i + 2]))
            shpi.append(int(list[4 * i + 3]))

        datadict["forecast_time"] = fctime
        datadict["south_hpi"] = shpi
        datadict["north_hpi"] = nhpi
        result[x_code] = 200
        result[x_data] = datadict
        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)



@api3.route('/aurora/27day')
def auror27day():

    result = {}

    url = "https://services.swpc.noaa.gov/text/27-day-outlook.txt"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = []
        beigain = False

        for line in content.splitlines():
            text = line.decode("utf8").strip()

            if beigain:
                tlist = text.split(" ")
                for t in tlist:
                    t = t.strip()
                    if len(t) > 0:
                        list.append(t)
            else:
               if text.find("#  Date ") > -1:
                   beigain = True

        datalist = []
        n = int(len(list)/6)
        for i in range(0,n):
            # otime = list[4 * i]
            dict = {}
            year = int(list[6 * i + 0])
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                      "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthstr = list[6 * i + 1]
            month = 1
            for j in range(1, 13):
                m = months[j - 1]
                if m == monthstr:
                    month = j
                    break
            day = int(list[6*i + 2])

            startdate = datetime(year, month, day, 0, 0, 0, tzinfo=tz)
            dict["time"] = startdate.timestamp()
            dict["flux"] = int(list[6*i + 3])
            dict["ap"] = int(list[6*i + 4])
            dict["kp"] = int(list[6*i + 5])
            datalist.append(dict)

        result[x_code] = 200
        result[x_data] = datalist
        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route('/aurora/solarwind')
def aurorsolarwind():

    result = {}
    url = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = json.loads(content)
        datalist = []

        tz_offset = timezonfoffset()

        n = len(list)

        for i in range(1,n):
            vlist = list[i]
            datadict = {}
            try:
                datadict["time_tag"] = vlist[0]
                datadict["speed"] = float(vlist[1])
                datadict["density"] = float(vlist[2])
                datadict["bz"] = float(vlist[6])
                datadict["bt"] = float(vlist[7])
                datadict["propagated_time_tag"] = vlist[11]
                ftime = vlist[0][:-4]
                fdate = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")
                datadict["time"] = int(fdate.timestamp()) + tz_offset
                ptime = vlist[11][:-4]
                pdate = datetime.strptime(ptime, "%Y-%m-%d %H:%M:%S")
                datadict["propagated_time"] = int(pdate.timestamp()) + tz_offset
                datalist.append(datadict)
            except Exception as e:
                pass



        result[x_code] = 200
        result[x_data] = datalist



        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)


@api3.route("/aurora/proton")
def auroraproton():
    result = {}
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = json.loads(content)
        datadict = {}

        tz_offset = timezonfoffset()

        mev10list = []
        mev50list = []
        mev100list = []
        mev500list = []



        for dict in list:
            time_tag = dict["time_tag"]
            dict["time"] = timetagtotimestamp(time_tag,tz_offset)
            energy = dict["energy"]
            if energy == ">=10 MeV":
                mev10list.append(dict)
            elif energy == ">=50 MeV":
                mev50list.append(dict)
            elif energy == ">=100 MeV":
                mev100list.append(dict)
            elif energy == ">=500 MeV":
                mev500list.append(dict)





        datadict["mev10"] = mev10list
        datadict["mev50"] = mev50list
        datadict["mev100"] = mev100list
        datadict["mev500"] = mev500list
        result[x_code] = 200
        result[x_data] = datadict



        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

@api3.route("/aurora/images")
def auroraimages():

    languange = request.args.get("language")


    list = [
        {"name":"Tonight's North America",
         "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png",
         "tip":"This is a prediction of the intensity and location of the aurora borealis tonight and tomorrow night over North America. It also shows a 'viewline' that represents the southern-most locations from which you may see the aurora on the northern horizon.  This product is based on the OVATION model and uses the maximum forecast geomagnetic activity (Kp) between 6pm and 6am US Central Time.  The images are updated continuously, with the transition when \"tomorrow night\" becomes \"tonight\" occurring at 12:00Z (i.e., within an hour of the end of the 6pm-6am Central Time window that is used here to define \"night\").",
         "type":0},

        {"name":"Tomorrow night's North America",
         "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png",
         "tip":"This is a prediction of the intensity and location of the aurora borealis tonight and tomorrow night over North America. It also shows a 'viewline' that represents the southern-most locations from which you may see the aurora on the northern horizon.  This product is based on the OVATION model and uses the maximum forecast geomagnetic activity (Kp) between 6pm and 6am US Central Time.  The images are updated continuously, with the transition when \"tomorrow night\" becomes \"tonight\" occurring at 12:00Z (i.e., within an hour of the end of the 6pm-6am Central Time window that is used here to define \"night\").",
         "type":0},

        {"name":"Space Weather Overview",
         "link":"https://services.swpc.noaa.gov/images/swx-overview-small.gif",
         "tip":"These plots provide a quick look at some of the most frequently examined space weather indices.",
         "type":0},

        {"name":"WSA-Enlil Solar Wind Prediction",
         "link":"https://services.swpc.noaa.gov/images/animations/enlil/latest.jpg",
         "tip":"WSA-Enlil is a large-scale, physics-based prediction model of the heliosphere, used by the Space Weather Forecast Office to provide 1-4 day advance warning of solar wind structures and Earth-directed coronal mass ejections (CMEs) that cause geomagnetic storms.  Solar disturbances have long been known to disrupt communications, wreak havoc with geomagnetic systems, and to pose dangers for satellite operations.",
         "images":"https://services.swpc.noaa.gov/products/animations/enlil.json",
         "type":1},

        {"name":"D Region Absorption Prediction",
         "link":"https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png",
         "tip":"The D-Region Absorption Product addresses the operational impact of the solar X-ray flux and SEP events on HF radio communication. Long-range communications using high frequency (HF) radio waves (3 - 30 MHz) depend on reflection of the signals in the ionosphere. Radio waves are typically reflected near the peak of the F2 layer (~300 km altitude), but along the path to the F2 peak and back the radio wave signal suffers attenuation due to absorption by the intervening ionosphere.\nThe D-Region Absorption Prediction model is used as guidance to understand the HF radio degradation and blackouts this can cause.",
         "images":"https://services.swpc.noaa.gov/products/animations/d-rap_global.json",
         "type":1},

        {"name":"Lasco c2",
         "link":"https://services.swpc.noaa.gov/images/animations/lasco-c2/latest.jpg",
         "tip":"LASCO images have been used by the SWPC forecast office to characterize the solar corona heating and transient events, including CME's, and to see the effects of the corona on the solar wind. More recently, the LASCO images are vital to the WSA-Enlil model that became operational in October of 2011. WSA-Enlil has become an important tool for forecasting the impact of Coronal Mass Ejections and the effects of the Solar Wind on the Earth.",
         "images":"https://services.swpc.noaa.gov/products/animations/lasco-c2.json",
         "type":1},

        {"name":"Lasco c3",
         "link":"https://services.swpc.noaa.gov/images/animations/lasco-c3/latest.jpg",
         "tip":"LASCO images have been used by the SWPC forecast office to characterize the solar corona heating and transient events, including CME's, and to see the effects of the corona on the solar wind. More recently, the LASCO images are vital to the WSA-Enlil model that became operational in October of 2011. WSA-Enlil has become an important tool for forecasting the impact of Coronal Mass Ejections and the effects of the Solar Wind on the Earth.",
         "images":"https://services.swpc.noaa.gov/products/animations/lasco-c3.json",
         "type":1},

        {"name":"GOES Solar Ultraviolet Imager Thematic Map",
         "link":"https://services.swpc.noaa.gov/images/animations/suvi/primary/map/latest.png",
        "tip":"",
         "images":"https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json",
         "type":1},

        {"name": "GOES Solar Ultraviolet Imager 94 Angstroms",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/094/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json",
         "type": 1},

        {"name": "GOES Solar Ultraviolet Imager 131 Angstroms",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/131/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-131.json",
         "type": 1},

        {"name": "GOES Solar Ultraviolet Imager 171 Angstroms",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-171.json",
         "type": 1},

        {"name": "GOES Solar Ultraviolet Imager 195 Angstroms",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-195.json",
         "type": 1},

        {"name": "GOES Solar Ultraviolet Imager 284 Angstroms",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/284/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-284.json",
         "type": 1},

        {"name": "GOES Solar Ultraviolet Imager 304 Angstroms",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-304.json",
         "type": 1},


        {"name": "HMI Intensitygram - Flattened",
         "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
         "tip": "",
         "type": 0},


        {"name": "Solar Synoptic Map",
         "link": "https://services.swpc.noaa.gov/images/synoptic-map.jpg",
         "tip": "SWPC forecasters use their synoptic maps to view the various characteristics of solar surface at a locked-in time, on a daily basis. They create a snapshot of the features of the Sun each day by drawing the various phenomena they see, including active regions, coronal holes, neutral lines (boundary between magnetic polarities),  plages and filaments and prominences. This map is a valuable tool for assessing the conditions on the sun and making the appropriate forecast for those conditions.",
         "type": 0},


    ]


    zhlist = [
        {"name":"今夜北美",
         "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png",
         "tip":"这是对今晚和明晚北美极光强度和位置的预测。它还显示了一条“视线”，代表您可以在北方地平线上看到极光的最南端位置。该产品基于 OVATION 模型，并使用美国中部时间下午 6 点至早上 6 点之间的最大预测地磁活动 (Kp)。图像不断更新，从“明晚”到“今晚”的过渡发生在 12:00Z（即，在中部时间下午 6 点至早上 6 点结束的一小时内，这里用于定义“夜晚”）。\n这两张地图显示了今晚和明晚的极光和视线。极光的亮度和位置通常显示为以地球磁极为中心的绿色椭圆形。当预测极光更强烈时，绿色椭圆形会变成红色。通常可以在日落后或日出前在地球上的某个地方观察到极光。白天看不到极光。极光不一定在正上方，但当极光明亮且条件合适时，从远至 1000 公里外都可以观察到。\n可以在极光 - 30 分钟预报页面上找到短期预报（约 30 分钟）以及过去 24 小时的活动。SWPC 的新极光仪表板（实验性）收集了 SWPC 网站上的产品和信息，提供一站式服务。",
         "type":0},

        {"name":"明夜北美",
         "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png",
         "tip": "这是对今晚和明晚北美极光强度和位置的预测。它还显示了一条“视线”，代表您可以在北方地平线上看到极光的最南端位置。该产品基于 OVATION 模型，并使用美国中部时间下午 6 点至早上 6 点之间的最大预测地磁活动 (Kp)。图像不断更新，从“明晚”到“今晚”的过渡发生在 12:00Z（即，在中部时间下午 6 点至早上 6 点结束的一小时内，这里用于定义“夜晚”）。\n这两张地图显示了今晚和明晚的极光和视线。极光的亮度和位置通常显示为以地球磁极为中心的绿色椭圆形。当预测极光更强烈时，绿色椭圆形会变成红色。通常可以在日落后或日出前在地球上的某个地方观察到极光。白天看不到极光。极光不一定在正上方，但当极光明亮且条件合适时，从远至 1000 公里外都可以观察到。\n可以在极光 - 30 分钟预报页面上找到短期预报（约 30 分钟）以及过去 24 小时的活动。SWPC 的新极光仪表板（实验性）收集了 SWPC 网站上的产品和信息，提供一站式服务。",
         "type":0},

        {"name":"空间天气预览",
         "link":"https://services.swpc.noaa.gov/images/swx-overview-small.gif",
         "tip":"这些图表可以让我们快速浏览一些最常检查的空间天气指数。",
         "type":0},

        {"name":"WSA-Enlil 太阳风预测",
         "link":"https://services.swpc.noaa.gov/images/animations/enlil/latest.jpg",
         "tip":"WSA-Enlil 是一种大规模的、基于物理学的日光层预测模型，空间天气预报办公室使用它来提前 1-4 天发出太阳风结构和地球日冕物质抛射 (CME) 的预警，这些抛射会导致地磁风暴。人们早就知道太阳扰动会干扰通信、破坏地磁系统，并对卫星运行造成危险。",
         "images":"https://services.swpc.noaa.gov/products/animations/enlil.json",
         "type":1},

        {"name":"D 区吸收预测",
         "link":"https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png",
         "tip":"D 区吸收产品解决了太阳 X 射线通量和 SEP 事件对 HF 无线电通信的运行影响。使用高频 (HF) 无线电波 (3 - 30 MHz) 的远程通信取决于电离层中信号的反射。无线电波通常在 F2 层峰顶附近反射（高度约 300 公里），但沿着到 F2 峰顶和返回的路径，无线电波信号会因中间电离层的吸收而衰减。\nD 区吸收预测模型用作指导，以了解由此可能导致的 HF 无线电退化和停电。",
         "images":"https://services.swpc.noaa.gov/products/animations/d-rap_global.json",
         "type":1},

        {"name":"Lasco c2",
         "link":"https://services.swpc.noaa.gov/images/animations/lasco-c2/latest.jpg",
         "tip":"LASCO 图像已被 SWPC 预报办公室用来描述日冕加热和瞬变事件（包括 CME）的特征，并观察日冕对太阳风的影响。最近，LASCO 图像对于 2011 年 10 月开始运行的 WSA-Enlil 模型至关重要。WSA-Enlil 已成为预测日冕物质抛射影响和太阳风对地球影响的重要工具。",
         "images":"https://services.swpc.noaa.gov/products/animations/lasco-c2.json",
         "type":1},

        {"name":"Lasco c3",
         "link":"https://services.swpc.noaa.gov/images/animations/lasco-c3/latest.jpg",
         "tip":"LASCO 图像已被 SWPC 预报办公室用来描述日冕加热和瞬变事件（包括 CME）的特征，并观察日冕对太阳风的影响。最近，LASCO 图像对于 2011 年 10 月开始运行的 WSA-Enlil 模型至关重要。WSA-Enlil 已成为预测日冕物质抛射影响和太阳风对地球影响的重要工具。",
         "images":"https://services.swpc.noaa.gov/products/animations/lasco-c3.json",
         "type":1},

        {"name":"GOES 太阳紫外成像仪主题图",
         "link":"https://services.swpc.noaa.gov/images/animations/suvi/primary/map/latest.png",
        "tip":"",
         "images":"https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json",
         "type":1},

        {"name": "GOES 太阳紫外成像仪 94 埃米",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/094/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json",
         "type": 1},

        {"name": "GOES 太阳紫外成像仪 131 埃米",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/131/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-131.json",
         "type": 1},

        {"name": "GOES 太阳紫外成像仪 171 埃米",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-171.json",
         "type": 1},

        {"name": "GOES 太阳紫外成像仪 195 埃米",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-195.json",
         "type": 1},

        {"name": "GOES 太阳紫外成像仪 284 埃米",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/284/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-284.json",
         "type": 1},

        {"name": "GOES 太阳紫外成像仪 304 埃米",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-304.json",
         "type": 1},

        # {"name": "HMI Magnetogram",
        #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg",
        #  "tip": "",
        #  "type": 0},
        #
        # {"name": "HMI Colorized Magnetogram",
        #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",
        #  "tip": "",
        #  "type": 0},
        #
        # {"name": "HMI Intensitygram - colored",
        #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg",
        #  "tip": "",
        #  "type": 0},
        #
        # {"name": "HMI Intensitygram - Flattened",
        #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
        #  "tip": "",
        #  "type": 0},

        {"name": "HMI Intensitygram - Flattened",
         "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
         "tip": "",
         "type": 0},

        # {"name": "HMI Dopplergram",
        #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMID.jpg",
        #  "tip": "",
        #  "type": 0},

        {"name": "太阳综合图",
         "link": "https://services.swpc.noaa.gov/images/synoptic-map.jpg",
         "tip": "SWPC 预报员使用他们的天气图来查看每天固定时间太阳表面的各种特征。他们通过绘制他们看到的各种现象来创建每天太阳特征的快照，包括活动区域、冕洞、中性线（磁极之间的边界）、斑块、细丝和日珥。这张图是评估太阳状况并针对这些状况做出适当预测的宝贵工具。",
         "type": 0},


    ]


    jplist = [
        {"name": "今夜の北米",
         "link": "https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png",
         "tip": "これは、今夜と明日の夜に北米で発生するオーロラの強度と位置の予測です。また、北の地平線上にオーロラが見える最南端の位置を表す「ビューライン」も表示します。この製品は OVATION モデルに基づいており、米国中部標準時の午後 6 時から午前 6 時までの最大予測地磁気活動 (Kp) を使用します。画像は継続的に更新され、\"明日の夜\" が \"今夜\" に切り替わるのは 12:00Z (つまり、ここで \"夜\" を定義するために使用されている午後 6 時から午前 6 時までの中部標準時ウィンドウの終了から 1 時間以内) です。",
         "type": 0},

        {"name": "明日の夜の北米",
         "link": "https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png",
         "tip": "これは、今夜と明日の夜の北米上空のオーロラの強度と位置の予測です。また、北の地平線上にオーロラが見える最南端の位置を表す「ビューライン」も表示されます。この製品は OVATION モデルに基づいており、米国中部標準時の午後 6 時から午前 6 時までの最大予測地磁気活動 (Kp) を使用します。画像は継続的に更新され、\"明日の夜\"が\"今夜\"に変わるのは12:00Z（つまり、ここで\"夜\"を定義するために使用されている午後6時から午前6時の中央標準時のウィンドウの終了から1時間以内）です。",
         "type": 0},

        {"name": "宇宙天気の概要",
         "link": "https://services.swpc.noaa.gov/images/swx-overview-small.gif",
         "tip": "これらのプロットは、最も頻繁に調査される宇宙天気指標のいくつかを簡単に見ることができます。",
         "type": 0},

        {"name": "WSA-Enlil太陽風予測",
         "link": "https://services.swpc.noaa.gov/images/animations/enlil/latest.jpg",
         "tip": "WSA-Enlilは、宇宙天気予報で使用される大規模な物理ベースの太陽圏予測モデルです。予報所は、地磁気嵐を引き起こす太陽風構造と地球に向けられたコロナ質量放出 (CME) について、1～4 日前に警告を発します。太陽の擾乱は、通信を妨害し、地磁気システムに大混乱をもたらし、衛星の運用に危険をもたらすことが長い間知られています。",
         "images": "https://services.swpc.noaa.gov/products/animations/enlil.json",
         "type": 1},

        {"name": "D 領域吸収予測",
         "link": "https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png",
         "tip": "D 領域吸収製品は、太陽 X 線フラックスと SEP イベントが HF 無線通信に及ぼす運用上の影響を扱っています。高周波 (HF) 無線波 (3～30 MHz) を使用した長距離通信は、電離層での信号の反射に依存します。電波は通常、F2 層のピーク付近 (高度約 300 km) で反射されますが、F2 ピークまでの経路に沿って、また戻る途中で、介在する電離層による吸収により電波信号が減衰します。\nD 領域吸収予測モデルは、これが原因となる可能性のある HF 無線の劣化とブラックアウトを理解するためのガイドとして使用されます。",
         "images": "https://services.swpc.noaa.gov/products/animations/d-rap_global.json",
         "type": 1},

        {"name": "Lasco c2",
         "link": "https://services.swpc.noaa.gov/images/animations/lasco-c2/latest.jpg",
         "tip": "LASCO 画像は、SWPC 予報局によって、太陽コロナの加熱と CME を含む過渡現象の特徴付け、および太陽風に対するコロナの影響を確認するために使用されています。最近では、LASCO 画像は、2011 年 10 月に運用が開始された WSA-Enlil モデルにとって不可欠です。WSA-Enlil は、コロナ質量放出の影響と太陽風が地球に与える影響を予測するための重要なツールとなっています。",
         "images": "https://services.swpc.noaa.gov/products/animations/lasco-c2.json",
         "type": 1},

        {"name": "Lasco c3",
         "link": "https://services.swpc.noaa.gov/images/animations/lasco-c3/latest.jpg",
         "tip": "LASCO 画像は、SWPC 予報局によって、太陽コロナの加熱と CME を含む過渡現象の特徴付け、およびコロナが太陽風に与える影響を調べるために使用されています。最近では、LASCO 画像は 2011 年 10 月に運用が開始された WSA-Enlil モデルにとって不可欠です。WSA-Enlil は、コロナ質量放出の影響と太陽風が地球に与える影響を予測するための重要なツールとなっています。",
         "images": "https://services.swpc.noaa.gov/products/animations/lasco-c3.json",
         "type": 1},

        {"name": "GOES 太陽紫外線イメージャー テーママップ",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/map/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json",
         "type": 1},

        {"name": "GOES 太陽紫外線イメージャー 94 オングストローム",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/094/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json",
         "type": 1},

        {"name": "GOES 太陽紫外線イメージャー131 オングストローム",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/131/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-131.json",
         "type": 1},

        {"name": "GOES ソーラー紫外線イメージャー 171 オングストローム",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-171.json",
         "type": 1},

        {"name": "GOES ソーラー紫外線イメージャー 195オングストローム",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-195.json",
         "type": 1},

        {"name": "GOES ソーラー紫外線イメージャー 284 オングストローム",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/284/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-284.json",
         "type": 1},

        {"name": "GOES ソーラー紫外線イメージャー 304 オングストローム",
         "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png",
         "tip": "",
         "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-304.json",
         "type": 1},

        {"name": "HMI 強度グラム - フラット化",
         "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
         "tip": "",
         "type": 0},

        {"name": "太陽総観図",
         "link": "https://services.swpc.noaa.gov/images/synoptic-map.jpg",
         "tip": "SWPC の予報官は、総観図を使用して、毎日、特定の時間に太陽表面のさまざまな特性を表示します。彼らは、活動領域、コロナホール、中性線（磁気極性の境界）、プラージュ、フィラメント、プロミネンスなど、観測したさまざまな現象を描き、毎日太陽の特徴のスナップショットを作成します。この地図は、太陽の状態を評価し、それらの状態を適切に予測するための貴重なツールです。",
         "type": 0},
    ]



    result = {}
    result[x_code] = 200
    if languange == "zh":
        result[x_data] = zhlist
    elif languange == "jp":
        result[x_data] = jplist
    else:
        result[x_data] = list
    return  json.dumps(result)


@api3.route("/aurora/win")
def winiie():
    url = "https://services.swpc.noaa.gov/products/animations/enlil.json"

@api3.route("/aurora/dg")
def dg():
    url = "https://services.swpc.noaa.gov/products/animations/d-rap_global.json"

@api3.route("/aurora/lac3")
def lac3():
    url = "https://services.swpc.noaa.gov/products/animations/lasco-c3.json"

@api3.route("/aurora/lacw")
def lac2():
    url = "https://services.swpc.noaa.gov/products/animations/lasco-c2.json"

@api3.route("/aurora/suvi")
def suvi():
    url94 = "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json"
    urlmap = "https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json"
@api3.route('/aurora/xray')
def aurorsolarxray():

    result = {}
    url = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        list = json.loads(content)
        datalist = []

        tz_offset = timezonfoffset()

        n = len(list)



        for i in range(0,n):
            datadict = list[i]

            try:
                time_tag = datadict["time_tag"]
                datadict["time"] = timetagtotimestamp(time_tag,tz_offset)
                datadict["begin_time"] = timetagtotimestamp(datadict["begin_time"],tz_offset)
                maxtime = timetagtotimestamp(datadict["max_time"],tz_offset)
                datadict["max_time"] = maxtime
                datadict["end_time"] = timetagtotimestamp(datadict["end_time"],tz_offset)
                datadict["max_ratio_time"] = timetagtotimestamp(datadict["max_ratio_time"],tz_offset)

                max_class = datadict["max_class"]
                if max_class.find("M") > -1 or max_class.find("X") > -1:
                    datalist.append(datadict)
            except Exception as e:
                pass



        result[x_code] = 200
        result[x_data] = datalist



        return json.dumps(result)
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e
        return json.dumps(result)

def timezonfoffset():

    return time.localtime().tm_gmtoff
def timetagtotimestamp(time,tz_offset):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return  int(date.timestamp()) + tz_offset

def pymeeusastrodict(timestamp):
    dict = {}

    dt = datetime.fromtimestamp(timestamp, tz=tz)
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24.0 + dt.minute / 60.0 / 24.0 + dt.second / 3600.0 / 24.0
    epoch = Epoch(year, month, day)
    jd = epoch.jde()

    es = pymeeus.Coordinates.true_obliquity(year,month,day)
    el = pymeeus.Coordinates.nutation_longitude(year,month,day)

    delta_t = round(Epoch.tt2ut(year, month), 3)
    ast = round(epoch.apparent_sidereal_time(es,el),9)
    sun_ra,sun_dec,sun_r = Sun.apparent_rightascension_declination_coarse(epoch)
    moon_ra, moon_dec, moon_r, moon_ppi = Moon.apparent_equatorial_pos(epoch)
    moon_ill = Moon.illuminated_fraction_disk(epoch)
    dict["time"] = timestamp
    dict["jd"] = jd
    dict["delta_t"] = delta_t
    dict["es"] = float(es)
    dict["ast"] = ast * 24
    dict["sun_ra"] = float(sun_ra) / 15.0
    dict["sun_dec"]= float(sun_dec)
    dict["sun_r"] = sun_r
    dict["moon_ra"] = float(moon_ra) / 15.0
    dict["moon_dec"] = float(moon_dec)
    dict["moon_r"] = moon_r
    dict["moon_ill"] = moon_ill


    return dict

