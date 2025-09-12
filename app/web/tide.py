#codeing=utf8
# -*- coding: utf-8 -*-
from . import web
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import logging
import sys
from flask import Flask,redirect,render_template,request,url_for,session,escape
import xlrd
import os
import json
from  config import basedir
# from coupon import coupon
import  MySQLdb
from flask_sqlalchemy import SQLAlchemy
import urllib, sys
import ssl
from app import db
import re
from timezonefinder import TimezoneFinder
from app.utils.constvalue import acuuappkey,xinzhi_prinvate_key,xinzhi_public_key,openweather_key,accu_minutecastkey

tf = TimezoneFinder()



statelist = [{'link': '?gid=1393', 'name': u'California'}, {'link': '?gid=1409', 'name': u'Oregon'}, {'link': '?gid=1415', 'name': u'Washington'}, {'link': '?gid=1391', 'name': u'Alaska'}, {'link': '?gid=1401', 'name': u'Maine'}, {'link': '?gid=1405', 'name': u'New Hampshire'}, {'link': '?gid=1403', 'name': u'Massachusetts'}, {'link': '?gid=1411', 'name': u'Rhode Island'}, {'link': '?gid=1394', 'name': u'Connecticut'}, {'link': '?gid=1407', 'name': u'New York'}, {'link': '?gid=1406', 'name': u'New Jersey'}, {'link': '?gid=1395', 'name': u'Delaware'}, {'link': '?gid=1410', 'name': u'Pennsylvania'}, {'link': '?gid=1402', 'name': u'Maryland'}, {'link': '?gid=1414', 'name': u'Virginia'}, {'link': '?gid=1396', 'name': u'Washington DC'}, {'link': '?gid=1408', 'name': u'North Carolina'}, {'link': '?gid=1412', 'name': u'South Carolina'}, {'link': '?gid=1398', 'name': u'Georgia'}, {'link': '?gid=1397', 'name': u'Florida'}, {'link': '?gid=1392', 'name': u'Alabama'}, {'link': '?gid=1404', 'name': u'Mississippi'}, {'link': '?gid=1400', 'name': u'Louisiana'}, {'link': '?gid=1413', 'name': u'Texas'}, {'link': '?gid=1542', 'name': u'Northern Marianas Islands'}, {'link': '?gid=1543', 'name': u'Federated States of Micronesia'}, {'link': '?gid=1544', 'name': u'Marshall Islands'}, {'link': '?gid=1399', 'name': u'Hawaii'}, {'link': '?gid=1484', 'name': u'Kiribati'}, {'link': '?gid=1775', 'name': u'Tokelau'}, {'link': '?gid=1771', 'name': u'American Samoa'}, {'link': '?gid=1482', 'name': u'French Polynesia'}, {'link': '?gid=1752', 'name': u'Cook Islands'}, {'link': '?gid=1483', 'name': u'Fiji'}, {'link': '?gid=1535', 'name': u'Bermuda Islands'}, {'link': '?gid=1536', 'name': u'Bahamas'}, {'link': '?gid=1537', 'name': u'Cuba'}, {'link': '?gid=1538', 'name': u'Jamaica'}, {'link': '?gid=1539', 'name': u'Haiti and Dominican Republic'}, {'link': '?gid=1540', 'name': u'Puerto Rico'}, {'link': '?gid=1541', 'name': u'Lesser Antilles & Virgin Islands'}]

currentrregionlist = [{'link': 'Stations?g=454', 'name': u'Maine'}, {'link': 'Stations?g=466', 'name': u'New Hampshire'}, {'link': 'Stations?g=456', 'name': u'Massachusetts'}, {'link': 'Stations?g=461', 'name': u'Rhode Island'}, {'link': 'Stations?g=449', 'name': u'Connecticut'}, {'link': 'Stations?g=458', 'name': u'New York'}, {'link': 'Stations?g=457', 'name': u'New Jersey'}, {'link': 'Stations?g=450', 'name': u'Delaware'}, {'link': 'Stations?g=467', 'name': u'Pennsylvania'}, {'link': 'Stations?g=455', 'name': u'Maryland'}, {'link': 'Stations?g=464', 'name': u'Virginia'}, {'link': 'Stations?g=468', 'name': u'District of Columbia'}, {'link': 'Stations?g=459', 'name': u'North Carolina'}, {'link': 'Stations?g=462', 'name': u'South Carolina'}, {'link': 'Stations?g=452', 'name': u'Georgia'}, {'link': 'Stations?g=451', 'name': u'Florida'}, {'link': 'Stations?g=451', 'name': u'Florida'}, {'link': 'Stations?g=448', 'name': u'Alabama'}, {'link': 'Stations?g=465', 'name': u'Mississippi'}, {'link': 'Stations?g=453', 'name': u'Louisiana'}, {'link': 'Stations?g=463', 'name': u'Texas'}, {'link': 'Stations?g=460', 'name': u'Puerto Rico'}, {'link': 'Stations?g=696', 'name': u'California'}, {'link': 'Stations?g=697', 'name': u'Oregon'}, {'link': 'Stations?g=698', 'name': u'Washington'}, {'link': 'Stations?g=693', 'name': u'Alaska'}, {'link': 'Stations?g=694', 'name': u'Hawaii'}]
@web.route("/noaa/tide/state")
def noaatidestate():
    driver = webdriver.Chrome()
    list = []
    try:
        string = "https://tidesandcurrents.noaa.gov/tide_predictions.html"
        driver.get(string)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        maindiv = soup.find("div", attrs={"id": "divTideTableMain"})
        alinkss = maindiv.select("a")
        for alin in alinkss:
            print (alin.attrs["href"])
            dict = {}
            dict["link"] = alin.attrs["href"]
            dict["name"] = alin.text
            list.append(dict)


    except Exception as e:
        print(e)

    driver.quit()

    return json.dumps(list)
    return "done"



@web.route("/noaa/tide/station")
def noaatidestaion():
    driver = webdriver.Chrome()
    list = []
    try:
        for sdict in statelist:
            link = sdict["link"]
            string = "https://tidesandcurrents.noaa.gov/tide_predictions.html" + link
            slist = []
            driver.get(string)
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            maindiv = soup.find("div", attrs={"id": "divTideTableMain"})
            table = maindiv.find("table",attrs={"class":"table"})
            trs = table.select("tr")
            for tr in trs:
                a = tr.find("a")
                if a is not  None:
                    tds = tr.select("td")
                    tlist = []
                    for td in tds:
                        tlist.append(td.text)
                    slist.append(tlist)
            sdict["list"] = slist




    except Exception as e:
        print(e)

    driver.quit()

    image_path = os.path.join(basedir, 'static/noaa' , "tidestation.json")
    f = open(image_path,"w")
    f.write(json.dumps(statelist))
    f.close()
    return json.dumps(statelist)
    return "done"



@web.route("/noaa/harmonic/station")
def noaaharmonicstaion():
    driver = webdriver.Chrome()
    list = []
    try:


            string = "https://tidesandcurrents.noaa.gov/stations.html?type=Harmonic+Constituents"


            driver.get(string)
            time.sleep(5)
            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')
            maindiv = soup.find("div", attrs={"class": "span9"})
            trs = maindiv.select("a")
            for a in trs:
                try:
                    name =  a.text
                    href = a.attrs["href"]
                    index =  href.find("id=")
                    if index > 0:
                        id = href[index + 3:]
                        dict = {}
                        dict["stationId"] = id
                        title =  name[len(id):].strip()

                        dict["name"] =  title
                        list.append(dict)
                except Exception as e :
                    print(e)





    except Exception as e:
        print(e)

    driver.quit()

    image_path = os.path.join(basedir, 'static/noaa', "harmonicstation.json")
    f = open(image_path, "w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(list)


@web.route("/noaa/current/table")
def noaacurrenttable():
    driver = webdriver.Chrome()
    hlist = []
    slist = []
    try:


            string = "https://opendap.co-ops.nos.noaa.gov/axis/webservices/currentpredictionstations/response.jsp?format=html"


            driver.get(string)
            time.sleep(5)
            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')
            maindiv = soup.find("table", attrs={"class": "metadata"})
            trs = maindiv.select("tr")
            i = 0
            for tr in trs:
                tds = tr.select("td")
                if i > 0 :
                    id =  tds[0].text.strip()
                    type = tds[6].text.strip()
                    if type == "Harmonic":
                        if id not in hlist:
                            hlist.append(id)
                    elif type == "Subordinate":
                        if id not in slist:
                            slist.append(id)

                else:
                    pass

                i =  i + 1





    except Exception as e:
        print(e)

    driver.quit()

    result = {}
    result["h"] = hlist
    result["s"] =  slist
    image_path = os.path.join(basedir, 'static/noaa', "currenttable.json")
    f = open(image_path, "w")
    f.write(json.dumps(result))
    f.close()
    return json.dumps(result)

@web.route("/noaa/current/state")
def noaacurrentstate():
    driver = webdriver.Chrome()
    list = []
    try:
        string = "https://tidesandcurrents.noaa.gov/noaacurrents/Regions"
        driver.get(string)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.select(".span2")
        for div in divs:
            tablle = div.find("table")
            if tablle is not  None:
                trs = tablle.select("tr")
                for tr in trs:
                    a = tr.find("a")
                    if a is not  None:
                        dict = {}
                        dict["link"] = a.attrs["href"]
                        dict["name"] = a.text
                        list.append(dict)


    except Exception as e:
        print(e)

    driver.quit()

    return json.dumps(list)
    return "done"



@web.route("/noaa/current/station")
def noaacurrentstaion():
    driver = webdriver.Chrome()
    list = []
    try:
        for sdict in currentrregionlist:
            link = sdict["link"]
            string = "https://tidesandcurrents.noaa.gov/noaacurrents/" + link
            slist = []
            driver.get(string)
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            maindiv = soup.find("div", attrs={"class": "span10"})
            divs = maindiv.select(".span12")
            div = divs[len(divs)-1]
            table = div.find("table")
            trs = table.select("tr")
            for tr in trs:
                a = tr.find("a")
                if a is not  None:

                    tds = tr.select("td")
                    tlist = []
                    tlist.append(a.attrs["href"])
                    for td in tds:
                        tlist.append(td.text)
                    slist.append(tlist)
            sdict["list"] = slist




    except Exception as e:
        print(e)

    driver.quit()

    image_path = os.path.join(basedir, 'static/noaa' , "currentstation.json")
    f = open(image_path,"w")
    f.write(json.dumps(currentrregionlist))
    f.close()
    return json.dumps(currentrregionlist)
    return "done"

@web.route("/noaa/tide/station/list")
def noaatidestaionlist():
    image_path = os.path.join(basedir, 'static/noaa', "tidestation.json")
    sf = open(image_path,"r")
    fr = sf.read()
    js = json.loads(fr)
    sf.close()
    list = []
    n = 0
    for sdict in js:
        slit = sdict["list"]
        for sarray in slit:
            dict = {}
            dict["name"] = sarray[0].strip()
            dict["stationId"] = sarray[1]
            dict["lat"] = sarray[2]
            dict["lon"] = sarray[3]
            dict["predictions"] = sarray[4]
            if sarray[4] == "Harmonic":
                n = n + 1
            list.append(dict)

    print(n)
    image_path = os.path.join(basedir, 'static/noaa' , "tidestationlist.json")
    f = open(image_path,"w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(list)

@web.route("/noaa/tide/hormic")
def noaatidestatehormic():
    driver = webdriver.Chrome()
    list = []
    try:
        string = "https://tidesandcurrents.noaa.gov/stations.html?type=Harmonic+Constituents"
        driver.get(string)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        maindiv = soup.find("div", attrs={"class": "span9"})
        alinkss = maindiv.select("a")
        print(len(alinkss))
        # for alin in alinkss:
        #     print (alin.attrs["href"])
        #     dict = {}
        #     dict["link"] = alin.attrs["href"]
        #     dict["name"] = alin.text
        #     list.append(dict)


    except Exception as e:
        print(e)

    driver.quit()

    return json.dumps(list)
    return "done"


@web.route("/noaa/tide/station/harmoric/list")
def noaatidestaionharmoriclist():
    driver = webdriver.Chrome()
    image_path = os.path.join(basedir, 'static/noaa', "tidestationlist.json")
    sf = open(image_path,"r")
    fr = sf.read()
    js = json.loads(fr)
    sf.close()
    list = []
    n = 0
    for sdict in js:
        type = sdict["predictions"]
        if type == "Harmonic":
            try:
                id = sdict["stationId"]
                string = "https://tidesandcurrents.noaa.gov/harcon.html?id=" + id
                driver.get(string)
                time.sleep(5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                maindiv = soup.find("table", attrs={"class": "table-striped"})
                tbody = maindiv.find("tbody")
                trs = tbody.select("tr")
                hdict = {}
                hdict["stationId"] = id
                hlsit = []
                for tr in trs:
                    tds = tr.select("td")
                    tlist = []
                    tlist.append(tds[1].text)
                    tlist.append(tds[2].text)
                    tlist.append(tds[3].text)
                    tlist.append(tds[4].text)

                    hlsit.append(tlist)
                hdict["cons"]  = hlsit
                list.append(hdict)

            except Exception as e:
                print(e)





    print(n)
    image_path = os.path.join(basedir, 'static/noaa' , "tidehormoniiclist.json")
    f = open(image_path,"w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(list)

@web.route("/noaa/cons")
def noaacons():
    listb = ["Sa","Ssa", "Mm","MSf","Mf","Q1","Rho1","O1","M1","P1","S1","K1","J1","OO1","2N2","Mu2","N2","Nu2",
    "M2",
    "Lam2"
    "L2",
    "T2",
    "S2",
    "R2",
    "K2",
    "2SM2",
    "M3",
    "MK3",
    "M4",
    "MS4",
    "M6"]
    lisa =[]
    for l in listb:
        lisa.append(l.upper())
    slist = ["M2", "S2", "N2", "K1", "M4", "O1", "M6", "MK3", "S4", "MN4", "NU2", "S6", "MU2", "2N2", "OO1", "LAM2",
             "S1", "M1", "J1", "MM", "SSA", "SA", "MSF", "MF", "RHO", "Q1", "T2", "R2", "2Q1", "P1", "2SM2", "M3", "L2",
             "2MK3", "K2", "M8", "MS4"]
    list = []
    for s in slist:
        if s not  in lisa:
            list.append(s)

    return json.dumps(list)


@web.route("/noaa/tide/harmonic/list")
def noaatideharmonmiclist():
    image_path = os.path.join(basedir, 'static/noaa', "tidehormonicnlist2.json")
    sf = open(image_path,"r")
    fr = sf.read()
    js = json.loads(fr)
    # return json.dumps(js)
    sf.close()
    n = 0
    list = []
    slist = ["M2","S2","N2","K1","M4","O1","M6","MK3","S4","MN4","NU2","S6","MU2","2N2","OO1","LAM2","S1","M1","J1","MM","SSA","SA","MSF","MF","RHO","Q1","T2","R2","2Q1","P1","2SM2","M3","L2","2MK3","K2","M8","MS4"]
    for sdict in js:
        dict = {}
        dict["id"] = sdict["id"]

        clist = []
        try:
            for con in slist:
                if con in sdict:
                    cons = sdict[con]
                    clist.append(cons[0])
                    clist.append(cons[1])
                else:

                    clist.append("")
                    clist.append("")

            dict["cons"] = clist
            list.append(dict)
        except Exception  as  e:
            print (e)



    print(n)
    image_path = os.path.join(basedir, 'static/noaa' , "tidehormonicnlist3.json")
    f = open(image_path,"w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(list)

@web.route("/noaa/tide/station/read/list")
def noaatidereadstaionlist():
    driver = webdriver.Chrome()
    image_path = os.path.join(basedir, 'static/noaa', "tidestationlist.json")
    sf = open(image_path,"r")
    fr = sf.read()
    js = json.loads(fr)
    sf.close()
    list = []
    n = 0
    m = 0
    for j in js:
        predictions = j["predictions"]
        if predictions == "Harmonic":
            n =  n + 1
        else:
            m = m + 1
            dict = {}
            id = j["stationId"]
            dict["id"] = id
            try:
                string = "https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=" + id
                driver.get(string)
                time.sleep(5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                maindiv = soup.find("div", attrs={"id": "container"})
                text = maindiv.find("text",attrs={"class":"highcharts-title"})
                content = text.text

                index = content.find("Subordinate")
                dict["text"] = content[index:].split("|")

                list.append(dict)


            except Exception as  e:
                print(e)



    list_path = os.path.join(basedir, 'static/noaa' , "tidesubordinateiclist.json")
    f = open(list_path,"w")
    f.write(json.dumps(list))
    f.close()
    return  json.dumps(list)


@web.route("/noaa/tide/station/read/list/check")
def noaatidereadstaionlistcheck():
    # driver = webdriver.Chrome()
    # image_path = os.path.join(basedir, 'static/noaa', "tidestationlist.json")
    # sf = open(image_path,"r")
    # fr = sf.read()
    # js = json.loads(fr)
    # sf.close()
    list = []

    list_path = os.path.join(basedir, 'static/noaa', "tidesubordinateiclist.json")
    f = open(list_path,"r")
    lr = f.read()
    ls = json.loads(lr)
    for l in ls:
        dict = {}
        dict["id"] = l["id"]
        texts = l["text"]
        patten = r'\d+'
        mainportid = texts[1].strip()
        mindex = mainportid.rfind(" ")
        dict["main_port"] = mainportid[mindex:-1].strip()
        timeiffset = texts[2].strip()
        timehigh = timeiffset.find("high:")
        timelow = timeiffset.find("low:")
        timehigh_text = timeiffset[timehigh +5: timelow].strip()
        timelow_text = timeiffset[timelow + 4:-1].strip()
        dict["time_offset"] = [timehigh_text[:-4].strip(),timelow_text[:-4].strip()]

        heightiffset = texts[3].strip()
        heigthigh = heightiffset.find("high:")
        heightlow = heightiffset.find("low:")
        heighthigh_text =  heightiffset[heigthigh +5: heightlow].strip()
        heightlow_text = heightiffset[heightlow + 4:-1].strip()
        dict["height_offset"] = [heighthigh_text[:-3].strip(),heightlow_text[:-3].strip()]
        list.append(dict)

        # list.append(l["id"])
    # for j in js:
    #     predictions = j["predictions"]
    #     if predictions == "Harmonic":
    #         pass
    #     else:
    #         id = j["stationId"]
    #         if id not in list:
    #             try:
    #                 string = "https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=" + id
    #                 driver.get(string)
    #                 time.sleep(5)
    #                 html = driver.page_source
    #                 soup = BeautifulSoup(html, 'lxml')
    #                 maindiv = soup.find("div", attrs={"id": "container"})
    #                 text = maindiv.find("text", attrs={"class": "highcharts-title"})
    #                 content = text.text
    #
    #                 index = content.find("Subordinate")
    #                 dict = {}
    #                 dict["id"] = id
    #                 dict["text"] = content[index:].split("|")
    #
    #                 ls.append(dict)
    #                 print content
    #
    #             except Exception, e:
    #                 print e.message
    # f = open(list_path,"w")
    # f.write(json.dumps(ls))
    # f.close()

    list_path = os.path.join(basedir, 'static/noaa' , "tidesubordinatechecklist.json")
    f = open(list_path,"w")
    f.write(json.dumps(list))
    f.close()

    return json.dumps(list)



@web.route("/noaa/tide/station/sperate")
def noaatidereadstaionlistspperate():
    list_path = os.path.join(basedir, 'static/noaa', "tidesubordinatechecklist.json")
    f = open(list_path, "r")
    subs = json.loads(f.read())
    f.close()
    slist = []
    for sub in subs:
        slist.append(sub["id"])

    list_path = os.path.join(basedir, 'static/noaa', "tidehormonicnlist3.json")
    f = open(list_path, "r")
    hors = json.loads(f.read())
    f.close()
    hlist = []
    for hor in hors:
         hlist.append(hor["id"])

    sublist = []
    hormoniclist = []
    image_path = os.path.join(basedir, 'static/noaa', "tidestationlist.json")
    sf = open(image_path, "r")
    fr = sf.read()
    js = json.loads(fr)
    sf.close()
    for j in js:

        predictions = j["predictions"]
        if predictions == "Harmonic":
            id = j["stationId"]
            if id in hlist:
                hormoniclist.append(j)
        else:

            id = j["stationId"]
            if id in slist:
                sublist.append(j)

    list_path = os.path.join(basedir, 'static/noaa' , "tidestationhormoniclist.json")
    f = open(list_path,"w")
    f.write(json.dumps(hormoniclist))
    f.close()

    list_path = os.path.join(basedir, 'static/noaa' , "tidestationsubordinatelist.json")
    f = open(list_path,"w")
    f.write(json.dumps(sublist))
    f.close()


    return json.dumps(sublist)



@web.route("/noaa/tide/current/sperate")
def noaacurrentsperate():
    list_path = os.path.join(basedir, 'static/noaa', "currentstation.json")
    f = open(list_path, "r")
    subs = json.loads(f.read())
    f.close()

    list = []
    for sub in subs:
        slist = sub["list"]
        for s in slist:
            dict = {}
            dict["link"] = s[0]
            dict["name"] = s[1].strip()
            link = s[0]
            index = link.find("id=")
            id = link[index + 3:]
            indexhua = id.find("_")
            if indexhua > 0:
                dict["id"] = id[:indexhua]
                dict["sub_id"]  = id[indexhua + 1:]
            else:
                dict["id"] = id
            dict["latitude"] = s[3]
            dict["longitude"] = s[4]
            dict["type"] = s[5]
            list.append(dict)



    list_path = os.path.join(basedir, 'static/noaa' , "currentstationlist.json")
    f = open(list_path,"w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(list)


@web.route("/noaa/tide/current/check")
def noaacurrentcheck():
    list_path = os.path.join(basedir, 'static/noaa', "currentstationlist.json")
    f = open(list_path, "r")
    subs = json.loads(f.read())
    f.close()

    list = []
    for sub in subs:
        name = sub["name"]
        index = name.find("(Depth")
        if index > 0:
            id = sub["id"]
            truename = name[:index].strip()
            depth = name[index + 6:-1].strip()
            dict = None
            for l in list:
                lid = l["id"]
                if id == lid:
                    dict = l
                    break
            if dict is None:
                dict = {}
                dict["id"] = id
                dict["name"] = truename
                dict["type"] = sub["type"]
                dict["latitude"] =  currentlatitudevalue( sub["latitude"])
                dict["longitude"] = currentlongititudevalue(sub["longitude"])
                try:

                    timezone_name = tf.timezone_at(lng=dict["longitude"], lat=dict["latitude"] )
                    if timezone_name is None:
                        pass
                    else:

                        dict["TimeZone"] = timezone_name
                except Exception as e:
                    print (e)
                depathdict = {}
                depathdict["depth"] = depth
                depathdict["link"] = sub["link"]
                depathdict["sub_id"] = sub["sub_id"]
                dict["depth"] = [depathdict]
            else:
                depathdict = {}
                depathdict["depth"] = depth
                depathdict["sub_id"] = sub["sub_id"]
                depathdict["link"] = sub["link"]
                dict["depth"].append(depathdict)


            list.append(dict)
        else:
            dict = {}
            dict["name"] = sub["name"].strip()
            dict["id"] = sub["id"]
            dict["type"] = sub["type"]
            dict["latitude"] = currentlatitudevalue( sub["latitude"])
            dict["longitude"] = currentlongititudevalue(sub["longitude"])
            dict["link"] = sub["link"]
            try:

                timezone_name = tf.timezone_at(lng=dict["longitude"], lat=dict["latitude"])
                if timezone_name is None:
                    pass
                else:

                    dict["TimeZone"] = timezone_name
            except Exception as e:
                print(e)
            list.append(dict)
        # slist = sub["list"]
        # for s in slist:
        #     dict = {}
        #     dict["link"] = s[0]
        #     dict["name"] = s[1].strip()
        #     link = s[0]
        #     index = link.find("id=")
        #     id = link[index + 3:]
        #     indexhua = id.find("_")
        #     if indexhua > 0:
        #         dict["id"] = id[:indexhua]
        #         dict["sub_id"]  = id[indexhua + 1:]
        #     else:
        #         dict["id"] = id
        #     dict["latitude"] = s[3]
        #     dict["longitude"] = s[4]
        #     dict["type"] = s[5]
        #     list.append(dict)



    list_path = os.path.join(basedir, 'static/noaa' , "currentstationdepthlist.json")
    f = open(list_path,"w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(list)



def currentlatitudevalue(lat):
    index = lat.find("°")
    latv = lat[:index]
    latd = float(latv)
    if lat.find("S") >0:
        return  latd * -1
    else:
        return latd
def currentlongititudevalue(lng):
    index = lng.find("°")
    lngv = lng[:index]
    lngd = float(lngv)
    if lng.find("W") >0:
        return  lngd * -1
    else:
        return lngd

@web.route("/noaa/tide/hormonic/timezone")
def noaatidehormonictimezonecheck():
    list_path = os.path.join(basedir, 'static/noaa', "tideshormonic.json")
    f = open(list_path, "r")
    subs = json.loads(f.read())
    f.close()

    # sub_path = os.path.join(basedir, 'static/noaa', "tidehormonicnlist3.json")
    # sf = open(sub_path, "r")
    # offsets = json.loads(sf.read())
    # sf.close()

    list = []
    for sub in subs:
        # id = sub["stationId"]
        # for offset in offsets:
        #     offid = offset["id"]
        #     if offid == id:
        #         sub["cons"] = offset["cons"]
        #         break
        list.append(sub)

    # f = open(list_path, "w")
    # f.write(json.dumps(list))
    # f.close()


    return json.dumps(list)


@web.route("/noaa/tide/subordinate/timezone")
def noaatidesubordinatetimezonecheck():
    list_path = os.path.join(basedir, 'static/noaa', "tidesubordinate.json")
    f = open(list_path, "r")
    subs = json.loads(f.read())
    f.close()

    sub_path = os.path.join(basedir, 'static/noaa', "tideshormonic.json")
    sf = open(sub_path, "r")
    offsets = json.loads(sf.read())
    sf.close()
    list = []
    for off in offsets:
        list.append(off)
    for sb in subs:
        list.append(sb)




    # for sub in subs:
    #     id = sub["stationId"]
    #     for offset in offsets:
    #         offid = offset["id"]
    #         if offid == id:
    #             offdict = {}
    #             offdict["main_port"] = offset["main_port"]
    #             offdict["height_offset"] = offset["height_offset"]
    #             offdict["time_offset"] = offset["time_offset"]
    #             sub["offset"] = offdict
    #             break
    #     list.append(sub)
    #
    #

    tidal_path = os.path.join(basedir, 'static/noaa', "tidalstation.json")
    f = open(tidal_path, "w")
    f.write(json.dumps(list))
    f.close()
    return json.dumps(subs)


@web.route("/noaa/tide/current/timezone")
def noaatidecurrenttimezonecheck():
    list_path = os.path.join(basedir, 'static/noaa', "currentstation.json")
    f = open(list_path, "r")
    subs = json.loads(f.read())
    f.close()



    list = []
    for sub in subs:
        if "link" in sub:
            sub.pop("link")
            list.append(sub)
        else:
            if "depth" in sub:
                depths = sub["depth"]
                for depth in depths:
                    depth.pop("link")
            list.append(sub)

    f = open(list_path,"w")
    f.write(json.dumps(list))
    f.close()

    return json.dumps(list)
