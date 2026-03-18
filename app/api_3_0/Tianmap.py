#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage,tianmap_key
from flask import request

import json

import requests
from  xml.etree import ElementTree
import xmltodict
from config import basedir
from timezonefinder import TimezoneFinder


tf = TimezoneFinder()

@api3.route("/tian/geocode/tideanalysis")
def tiangeocodetideanalysis():
    path = os.path.join(basedir,"static/TPXO")
    n = 0
    slist = []

    plist = []

    elist = []


    ffile = os.path.join(path,"location.json")
    sfile = os.path.join(path,"chaolocation.json")
    fpath = os.path.join(path, ffile)
    f = open(fpath, "r")
    list = json.loads(f.read())

    for dict in list:
        language = request.args.get('language', 'en-us')
        lat = dict["lat"]
        lng = dict["lng"]
        n =  n + 1


        try:
            response = requests.get(
                'https://www.astronomyobserver.net/api/v3.0/tide/constant/all/' + lat + "/" + lng,
                params={
                    "language": language,

                },

            )

            json_data = response.json()
            dict["chao"] = json_data["data"]["tide"]["h"]
        except Exception as e:
            print(e)


        # city = dict["city_code"]
        # county = dict["province_code"]
        # cc = city + "_" + county
        # if cc not  in plist:
        #     plist.append(cc)
        #     sdict = {}
        #     sdict["province_code"] = dict["province_code"]
        #     sdict["province"] = dict["province"]
        #     sdict["city"] = dict["city"]
        #     sdict["city_code"] = dict["city_code"]
            # sdict["county"] = dict["county"]
            # # sdict["county_code"] = dict["county_code"]
            # slist.append(sdict)
    sf = open(sfile,"w")
    sf.write(json.dumps(list))
    sf.close()
    return json.dumps(list)

@api3.route("/tian/geocode/tide")
def tiangeocodetide():
    path = os.path.join(basedir,"static/TPXO/china")
    n = 0
    slist = []
    flist = []

    ffile = os.path.join(path,"location.json")
    sfile = os.path.join(path,"success.json")

    clist = []

    # for parent, _, fileNames in os.walk(path):
    #     for filename in fileNames:
    if 1:
            fpath = os.path.join(path, sfile)
            f = open(fpath, "r")
            list = json.loads(f.read())


            for dict in list:

                n = n + 1

                try:

                    lat = dict["lat"]
                    lng = dict["lng"]
                    location = dict["location"]
                    addressComponent = location["addressComponent"]
                    addressComponent["lat"] = "%.4f"%lat
                    addressComponent["lng"] = "%.4f"%lng
                    addressComponent["formatted_address"] = location["formatted_address"]
                    addressComponent["town"] = ""
                    addressComponent["town_code"] = ""
                    slist.append(addressComponent)
                    # if addressComponent.has_key("county_code"):
                    #     county_code = addressComponent["county_code"]
                    #     if county_code not in clist:
                    #         clist.append(county_code)
                except:
                    pass
                # for fdict in fix:
                #     result = {}
                #     lat = fdict["lat"]
                #     lng = fdict["lng"]
                #     parma = {}
                #     time.sleep(2)
                #     parma["lat"] = "%.4f"%lat
                #     parma["lon"] = "%.4f"%lng
                #     parma["ver"] = "1"
                #
                #     try:
                #         response = requests.get(
                #             'http://api.tianditu.gov.cn/geocoder',
                #             params={
                #                 "postStr": json.dumps(parma),
                #                 "tk": tianmap_key,
                #                 "type": "geocode"
                #             },
                #
                #         )
                #         json_data = response.json()
                #
                #         if json_data["status"] == "0":
                #             fdict["location"] = json_data["result"]
                #             print dict
                #         else:
                #             result[x_code] = 201
                #             result[x_meesage] = json_data["msg"]
                #             # fdict["location"] = False
                #     except Exception, e:
                #         print e.message
                #         result[x_meesage] = e.message
                #         result[x_code] = 201
            # wf = open(fpath,"w")
            # wf.write(json.dumps(list))
            # wf.close()
            # print filename
    # ff = open(ffile,"w")
    # ff.write(json.dumps(flist))
    # ff.close()
    sf = open(ffile,"w")
    sf.write(json.dumps(slist))
    sf.close()
            # print len(slist)

    return json.dumps(slist)


@api3.route("/tian/geocode")
def tiangeocode():

    lat = request.args.get('lat', '30.287')
    lng = request.args.get('lng', '120.0')

    result = {}
    parma = {}
    parma["lat"] = lat
    parma["lon"] = lng
    parma["ver"] = "1"

    try:
        response = requests.get(
            'http://api.tianditu.gov.cn/geocoder',
            params={
                "postStr":json.dumps(parma),
                "tk":tianmap_key,
                "type":"geocode"
            },

        )

        json_data = response.json()
        if json_data["status"] == "0":
            result[x_code] = 200
            datadict = json_data["result"]

            try:

                timezone_name = tf.timezone_at(lng=float(lng), lat=float(lat))
                if timezone_name is None:
                    pass
                else:
                    if timezone_name == "Asia/Urumqi":
                        timezone_name = "Asia/Shanghai"
                    datadict["TimeZone"] = timezone_name
            except Exception as e:
                pass

            result[x_data] = datadict

        else:
            result[x_code] = 201
            result[x_meesage] = json_data["msg"]
    except Exception as e:
        print(e)
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


@api3.route("/tian/geocode/ves")
def tiangeocodever():

    keyword = request.args.get('keyword', '杭州市余杭区闲林港西路'.encode("utf8"))


    result = {}
    parma = {}
    parma["keyWord"] = keyword


    try:
        response = requests.get(
            'http://api.tianditu.gov.cn/geocoder',
            params={
                "ds":json.dumps(parma),
                "tk":tianmap_key,
                "type": "geocode"
            },

        )


        # print  response

        # Do something with response data.
        json_data = response.json()


        if json_data["status"] == "0":
            result[x_code] = 200
            result[x_data] = json_data["location"]
        else:
            result[x_code] = 201
            result[x_meesage] = json_data["msg"]
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)



@api3.route("/tian/boundry")
def tianboundry():

    keyword = request.args.get("keword","高安市")

    result = {}
    parma = {}
    parma["needPolygon"] = "true"
    parma["searchWord"] = keyword
    parma["searchType"] = "1"


    try:
        response = requests.get(
            'http://api.tianditu.gov.cn/administrative',
            params={
                "postStr":json.dumps(parma),
                "tk":tianmap_key,

            },

        )


        # print  response

        # Do something with response data.
        json_data = response.json()

        return  json.dumps(json_data)

        if json_data["status"] == "0":
            result[x_code] = 200
            result[x_data] = json_data["result"]
        else:
            result[x_code] = 201
            result[x_meesage] = json_data["msg"]
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)



@api3.route("/tian/drive")
def tiandrive():

    orig = request.args.get("orig","115.24,28.17")
    dest = request.args.get("des","120.34,30.26")
    mid  = request.args.get("mid")
    style = request.args.get("style","0")

    result = {}
    parma = {}
    parma["orig"] = orig
    parma["dest"] = dest
    parma["style"] = style
    if mid is not None:
        parma["mid"] = mid


    try:
        response = requests.get(
            'http://api.tianditu.gov.cn/drive',
            params={
                "postStr":json.dumps(parma),
                "tk":tianmap_key,
                "type":"search"

            },

        )
        tree = xmltodict.parse(response.content)

        result[x_code] = 200
        result[x_data] = tree["result"]

    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)

@api3.route("/tian/copeni")
def tiancoperni():

    orig = request.args.get("orig","115.24,28.17")
    dest = request.args.get("des","120.34,30.26")
    mid  = request.args.get("mid")
    style = request.args.get("style","0")

    result = {}
    parma = {}
    parma["orig"] = orig
    parma["dest"] = dest
    parma["style"] = style
    if mid is not None:
        parma["mid"] = mid


    try:
        response = requests.get(
            'https://wmts.marine.copernicus.eu/teroWmts/GLOBAL_ANALYSISFORECAST_WAV_001_027/cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_202411?request=GetCapabilities&service=WMS',


        )
        tree = xmltodict.parse(response.content)

        result[x_code] = 200
        result[x_data] = tree

    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)



@api3.route("/tian/location/search")
def tianlocationsearch():
    keyword = request.args.get('keyword', '高安市')

    result = {}
    parma = {}
    parma["keyWord"] = keyword
    parma["level"] = 12
    parma["mapBound"] = "72,54,135,17"
    parma["queryType"] = 7
    parma["start"] = 0
    parma["count"]  = 20

    try:
        response = requests.get(
            'http://api.tianditu.gov.cn/v2/search',
            params={
                "postStr": json.dumps(parma),
                "tk": tianmap_key,
                "type": "query"
            },

        )

        # print  response

        # Do something with response data.
        json_data = response.json()

        result_type = json_data["resultType"]
        if result_type == 2:
            result[x_code] = 201
            result[x_meesage] = "结果太多，请输入详细地名"
        else:
            try:

                result[x_code] = 200
                result[x_data] = json_data["pois"]
            except:
                result[x_code] = 201
                result[x_meesage] = "没有搜索结果"

    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)