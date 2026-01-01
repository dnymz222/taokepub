#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,holiday_key,workingday_api_key
import json
from flask import request,session,url_for,redirect
from app import db


import time
import datetime
import urllib, sys
from urllib.parse import quote

import json

import requests
from app.Holiday import Holiday
from app.WorkingDaysConfig import WorkingDaysConfig
from app.WorkingDaysModel import WorkingDaysModel
from config import basedir
import os



@api3.route("/holiday/day")
def holidayday():
    day= request.args.get("day","2021-05-01")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(Holiday).filter_by(date=day).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.hoildaydict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)

@api3.route("/holiday/year")
def holidayyear():
    year= request.args.get("year","2021")
    code = request.args.get("code","CN")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(Holiday).filter_by(year=int(year),code=code).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.hoildaydict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s" % e

    return json.dumps(dict)



@api3.route("/workingday/all")
def workingdayall():
    year= request.args.get("year","2021")
    code = request.args.get("code","CN")
    month = request.args.get("month","09")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)



    except Exception as e:
        db.session.rollback()


    jsonstring = json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'workingdays.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return json.dumps(dict)



@api3.route("/workingday/month")
def workingdaymonth():
    year= request.args.get("year","2021")
    code = request.args.get("code","CN")
    month = request.args.get("month","09")

    configuration = request.args.get("configuration","")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(year=year,code=code,month = month,configuration=configuration).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)


@api3.route("/workingday/day")
def workingdayday():
    code = request.args.get("code","HK")
    date = request.args.get("date","2022-07-01")
    configuration = request.args.get("configuration","")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(date = date,code=code,configuration=configuration).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)
            try:
                holidayobject.public_holiday_description = "Hong Kong Special Administrative Region Establishment Day"
                db.session.commit()
            except Exception as e:

                db.session.rollback()



        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)

@api3.route("/workingday/year")
def workingdayyear():
    year= request.args.get("year","2025")
    code = request.args.get("code","HK")

    fixcode = request.args.get("fixcode","MO")

    configuration = request.args.get("configuration","")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(year=year,code=code,configuration=configuration).all()
        for holidayobject in holidays:
            hdict = holidayobject.woringdaysdict()
            list.append(hdict)


            try:
                if "0" == holidayobject.weekend_day:
                    working_day ="1"
                else:
                    working_day = "0"
                workingmodel = WorkingDaysModel(year, holidayobject.month, holidayobject.day, fixcode, "", working_day,holidayobject.weekend_day)
                db.session.add(workingmodel)

                db.session.commit()
                print(holidayobject.day)
            except Exception as  e:

                print(e)

                db.session.rollback()




        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)

@api3.route("/workingday/pulicholiday/year")
def workingdaypulicholiday_year():
    year= request.args.get("year","2021")
    code = request.args.get("code","CN")
    configuration = request.args.get("configuration", "")

    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(year=year,code=code, public_holiday= "1",configuration=configuration).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)


@api3.route("/workingday/config/month")
def workingdayconfigmonth():
    year= request.args.get("year","2021")
    code = request.args.get("code","CN")
    month = request.args.get("month","09")
    config = request.args.get("config","")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(year=year,code=code,month = month,configuration=config).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)

@api3.route("/workingday/config/pulicholiday/year")
def workingdayconfigpulicholiday_year():
    year= request.args.get("year","2021")
    code = request.args.get("code","CN")
    config = request.args.get("config", "")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(year=year,code=code, public_holiday= "1",configuration=config).all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s" %e

    return json.dumps(dict)

@api3.route("/workingday/pulicholiday/date")
def workingdaypulicholiday_date():
    date= request.args.get("date","2021-01-01")
    dict= {}
    list = []
    try:
        holidays =  db.session.query(WorkingDaysModel).filter_by(date = date, public_holiday= "1").all()
        for holidayobject in holidays:
            hdict  =  holidayobject.woringdaysdict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s" %e

    return json.dumps(dict)


@api3.route("/holiday/countries")
def holidaycountries():
    url = 'https://api.workingdays.org/1.3/configurations'
    list = []
    codelist = []
    try:
        response = requests.get(url)
        content = response.text
        result = json.loads(content)
        countries  =  result["countries"]

        for country in countries:
            dict = {}
            dict["code"]  =country["code"]
            dict["name"] = country["name"]


            list.append(dict)
            codelist.append(country["code"])


    except Exception as e:
        print(e)

    print(codelist)


    return json.dumps(list)

@api3.route("/workingday/add/config")
def addworkingconfig():
    list = [
             {"configId":"Belarus",
              "code":"BY",
              "flag":"",
              "website":"https://belarus.workingdays.org/setup",
              "default_configuration":"",
              "configurations":[]
              },
        {"configId": "Croatia",
         "code": "HR",
         "flag": "",
         "website": "https://croatia.workingdays.org/setup",
         "default_configuration": "",
         "configurations": []
         },

        {"configId": "Ecuador",
         "code": "EC",
         "flag": "",
         "website": "https://ecuador.workingdays.org/setup",
         "default_configuration": "",
         "configurations": []
         },

        {"configId": "Estonia",
         "code": "EE",
         "flag": "",
         "website": "https://estonia.workingdays.org/setup",
         "default_configuration": "",
         "configurations": []
         },

        {"configId": "Guatemala",
         "code": "GT",
         "flag": "",
         "website": "https://guatemala.workingdays.org/setup",
         "default_configuration": "Días festivos nacionales",
         "configurations": ["Días festivos nacionales","Ciudad de Guatemala"]
         },

        {"configId": "República Dominicana",
         "code": "DO",
         "flag": "",
         "website": "https://dominican-republic.workingdays.org/setup",
         "default_configuration": "",
         "configurations": []
         },

        {"configId": "Serbia",
         "code": "RS",
         "flag": "",
         "website": "https://serbia.workingdays.org/setup",
         "default_configuration": "",
         "configurations": []
         },

        {"configId": "Slovenia",
         "code": "SI",
         "flag": "",
         "website": "https://slovenia.workingdays.org/setup",
         "default_configuration": "",
         "configurations": []
         },

    ]

    for  dict in list:
        try:
            config  =WorkingDaysConfig(dict=dict)
            db.session.add(config)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    return "done"


@api3.route("/workingday/config")
def workingdayconfig():
    dict = {}
    list = []




    try:
        # db.session.query(WorkingDaysConfig).filter_by(code="HK").update({"configId": "Hong-Kong(China)"})
        workingdays =  db.session.query(WorkingDaysConfig).all()
        for wcobject in workingdays:
            hdict  =  wcobject.workingdayconfigdict()
            list.append(hdict)


        dict[x_code]=200
        dict[x_data] = list
    except Exception as e:
        db.session.rollback()
        dict[x_code]=201
        dict[x_meesage] = "%s"%e

    return json.dumps(list)





@api3.route("/workingday/dayinfo/<code>/<day>")
def workingdaygetdayinfo(code,day):
    dict = {}
    configuration = request.args.get("configuration","")
    url = 'https://api.workingdays.org/1.2/api.php?key=' + workingday_api_key+"&country_code="+code+"&command=get_info_day&date="+day
    print (url)
    if  len(configuration)>0:
        url = url +"&configuration="+configuration

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        result = json.loads(content)
        resultdict = result["result"]
        dict[x_data] = resultdict
        dict[x_code] = 200




    except Exception as e:

        dict[x_code] = 201
        dict[x_meesage] = "%s"%e

    return json.dumps(dict)






@api3.route("/workingday/year/<year>")
def workingdaygyeartotalinfo(year):

    try:
        workingdays = db.session.query(WorkingDaysConfig).all()

        # list = [
        #     {"configId": "Belarus",
        #      "code": "BY",
        #      "flag": "",
        #      "website": "https://belarus.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #     {"configId": "Croatia",
        #      "code": "HR",
        #      "flag": "",
        #      "website": "https://croatia.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #
        #     {"configId": "Ecuador",
        #      "code": "EC",
        #      "flag": "",
        #      "website": "https://ecuador.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #
        #     {"configId": "Estonia",
        #      "code": "EE",
        #      "flag": "",
        #      "website": "https://estonia.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #
        #     {"configId": "Guatemala",
        #      "code": "GT",
        #      "flag": "",
        #      "website": "https://guatemala.workingdays.org/setup",
        #      "default_configuration": "Días festivos nacionales",
        #      "configurations": ["Días festivos nacionales", "Ciudad de Guatemala"]
        #      },
        #
        #     {"configId": "República Dominicana",
        #      "code": "DO",
        #      "flag": "",
        #      "website": "https://dominican-republic.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #
        #     {"configId": "Serbia",
        #      "code": "RS",
        #      "flag": "",
        #      "website": "https://serbia.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #
        #     {"configId": "Slovenia",
        #      "code": "SI",
        #      "flag": "",
        #      "website": "https://slovenia.workingdays.org/setup",
        #      "default_configuration": "",
        #      "configurations": []
        #      },
        #
        # ]
        codelist = ['AR', 'AU', 'AT', 'BY', 'BE', 'BR', 'BG', 'CA', 'CL', 'CN', 'CO', 'HR', 'CZ', 'DK', 'DE', 'EC', 'ES', 'EE', 'FI', 'FR', 'GR', 'GT', 'HK', 'HU', 'IN', 'IL', 'IT', 'JP', 'LU', 'MC', 'MX', 'NL', 'NZ', 'NO', 'PE', 'PL', 'PT', 'DO', 'RO', 'RU', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'CH', 'SE', 'TW', 'TR', 'US', 'UA', 'GB', 'VE']
        hasbr = False
        for wcobject in workingdays:
            code = wcobject.code
            if code in codelist:
                pass
            else:
                continue

            print(code)
            configurations = wcobject.configurations
            print(configurations)



            try:
                count = db.session.query(WorkingDaysModel).filter_by(year=year, code=wcobject.code).count()
                if count < 30:
                    workingdaygconfigyearinfo(year, code ,wcobject.default_configuration)
                    print(code)
                    print("less")
                else:
                    if count < 365:
                        workingdaygconfigcheckyearinfo(year,code,wcobject.default_configuration)

            except Exception as e:
                print(e)
            # if len(configurations) > 0:
            #     continue
            #     # if len(wcobject.website) > 0:
            #     #     if wcobject.code == "CN":
            #     #         pass
            #     #     else:
            #     # configuration = configurations[1]
            #     # workingdaygconfigyearinfo(year,code,configuration)
            #     # time.sleep(0.2)
            # else:
            #     workingdaygconfigyearinfo(year,code,"")



    except Exception as e:

        db.session.rollback()

    return "done"



@api3.route("/workingday/config/year/<year>")
def workingdaygyearconfigtotalinfo(year):

    i = 0
    try:
        workingdays = db.session.query(WorkingDaysConfig).all()
        has_ca  = True
        has_ls = True
        for wcobject in workingdays:

            code = wcobject.code

            if has_ca:

                list = json.loads(wcobject.configurations)
                print (wcobject.default_configuration)

                for config in list:
                    if wcobject.default_configuration == config:
                        pass


                    else:
                        count = db.session.query(WorkingDaysModel).filter_by(year=year, code=wcobject.code,configuration=config).count()
                        if count < 30:
                            workingdaygconfigyearinfo(year, code, config)
                            print(code)
                            print("less")
                        else:
                            if count < 365:
                                workingdaygconfigcheckyearinfo(year, code, config)

                        # if has_ls:
                        #     print(config)
                        #     workingdaygconfigyearinfo(year,wcobject.code,config)
                        # else:
                        #     has_ls = (config == "New Hampshire")
            else:
                has_ca = (wcobject.code == "AU")



    except Exception as e:
        print(e)
        db.session.rollback()
    return "done"


@api3.route("/workingday/config/check/<year>")
def workingdaygyearconfigcheckinfo(year):
    i = 0
    try:
        workingdays = db.session.query(WorkingDaysConfig).all()
        for wcobject in workingdays:

            count = db.session.query(WorkingDaysModel).filter_by(year=year, code=wcobject.code,
                                                                 configuration="").count()
            if count < 366:
                print (count)
                print (wcobject.code)
                print ("defalult")
                print ("\n")
                if count > 1:
                    workingdaygconfigcheckyearinfo(year, wcobject.code, "")

            list = json.loads(wcobject.configurations)

            for config in list:
                if wcobject.default_configuration == config:
                    pass



                else:
                    count = db.session.query(WorkingDaysModel).filter_by(year=year, code=wcobject.code,
                                                                            configuration=config).count()
                    if count < 365:
                        print (count)
                        print (wcobject.code)
                        print (config)
                        print ("\n")

                        if count > 1:
                            workingdaygconfigcheckyearinfo(year,wcobject.code,config)







    except Exception as e:
        print (e)
        db.session.rollback()

    return "done"

@api3.route("/working/add/fix")
def addfixworkingday():
    try:
        workingmodel = WorkingDaysModel("2022","11","25","CA","Federal Holidays","1","0")
        db.session.add(workingmodel)
        db.session.commit()
    except Exception as e:
        print  (e)
        db.session.rollback()

    return "done"

@api3.route("/workingday/year/<year>/<code>")
def workingdaygyearinfo(year,code):
    newyear = year + "-01-01"
    dayTime = datetime.datetime.strptime(newyear, "%Y-%m-%d")

    offset = datetime.timedelta(days = 1)

    for i in  range(0,366):
        date = dayTime.strftime('%Y-%m-%d')

        print (date+"_"+code)

        if date == "2026-01-01":
            return "done"

        url = 'https://api.workingdays.org/1.2/api.php?key=' + workingday_api_key + "&country_code=" + code + "&command=get_info_day&date=" + date
        print (url)

        try:
            response = requests.get(url)
            content = response.text
            result = json.loads(content)
            resultdict = result["result"]
            resultdict["code"] =code
            resultdict["configuration"] = ""
            ls = date.split("-")
            resultdict["year"] = ls[0]
            resultdict["month"] = ls[1]
            resultdict["day"] = ls[2]
            print (resultdict)

            try:
                workingmodel = WorkingDaysModel(resultdict)
                db.session.add(workingmodel)
                db.session.commit()
            except Exception as e:
                print (e)
                db.session.rollback()






        except Exception as e:
            print(e)



        dayTime = dayTime +offset


    return "done"

@api3.route("/workingday/config/fix")
def configfix():
    # workingdaygconfigyearinfo("2022","CH","Basel-Stadt")

    workingdaygyearinfo("2023","PL")

    return "done"



def workingdaygconfigyearinfo(year,code,config):
    newyear = year + "-01-01"
    dayTime = datetime.datetime.strptime(newyear, "%Y-%m-%d")

    offset = datetime.timedelta(days = 1)

    for i in  range(0,365):
        date = dayTime.strftime('%Y-%m-%d')

        if date == "2027-01-01":
            return "done"

        print (date + "_" + code + "_" + config)

        encdoeconfig = config.encode(encoding='UTF-8')

        if len(config) > 0:

            url = 'https://api.workingdays.org/1.2/api.php?key=' + workingday_api_key + "&country_code=" + code + "&command=get_info_day&date=" + date + "&configuration=" + quote(
            encdoeconfig)
        else:
            url = 'https://api.workingdays.org/1.2/api.php?key=' + workingday_api_key + "&country_code=" + code + "&command=get_info_day&date=" + date

        print (url)
        try:
            try:
                req = requests.get(url)
                content = req.text
                result = json.loads(content)
                print (result)
                resultdict = result["result"]
                resultdict["code"] =code
                resultdict["configuration"] = config
                ls = date.split("-")
                resultdict["year"] = ls[0]
                resultdict["month"] = ls[1]
                resultdict["day"] = ls[2]

                try:
                    workingmodel = WorkingDaysModel(resultdict)
                    db.session.add(workingmodel)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()






            except Exception as  e:
                print(e)

        except Exception as e:
            print(e)




        dayTime = dayTime +offset


    return "done"

def workingdaygconfigcheckyearinfo(year,code,config):
    newyear = year + "-01-01"
    dayTime = datetime.datetime.strptime(newyear, "%Y-%m-%d")

    offset = datetime.timedelta(days = 1)

    for i in  range(0,365):
        date = dayTime.strftime('%Y-%m-%d')

        if date == "2027-01-01":
            return "done"



        try:
            count = db.session.query(WorkingDaysModel).filter_by(date=date, code=code,
                                                                 configuration=config).count()
            if count<1:

                print ("date:"+date)

                encdoeconfig = config.encode(encoding='UTF-8')



                if len(config)> 0:

                    url = 'https://api.workingdays.org/1.2/api.php?key=' + workingday_api_key + "&country_code=" + code + "&command=get_info_day&date=" + date + "&configuration=" + quote(
                        encdoeconfig)
                else:
                    url = 'https://api.workingdays.org/1.2/api.php?key=' + workingday_api_key + "&country_code=" + code + "&command=get_info_day&date=" + date
                print (url)

                try:
                    req = requests.get(url)
                    content = req.text
                    result = json.loads(content)
                    resultdict = result["result"]
                    resultdict["code"] = code
                    resultdict["configuration"] = config
                    ls = date.split("-")
                    resultdict["year"] = ls[0]
                    resultdict["month"] = ls[1]
                    resultdict["day"] = ls[2]

                    print(resultdict)

                    try:
                        workingmodel = WorkingDaysModel(resultdict)
                        db.session.add(workingmodel)
                        db.session.commit()
                    except Exception as e:
                        print (e)
                        db.session.rollback()



                except Exception as e:
                    print(e)




        except Exception as e:
            print(e)
            db.session.rollback()




        dayTime = dayTime +offset


    return "done"