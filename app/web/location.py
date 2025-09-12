#coding=utf8
from . import web
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


import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import logging
import sys
import random


from app.appuser import appuser

from config import basedir
from  app.utils.constvalue import appkey,secret,xunquanAppkey,xunquanSecret,solarAppkey,solarSecret,site_id
from app.worldTidalStation import worldTidalStation
from app.chinaTidalStation import chinaTidalStation


from app.ChinaCounty import ChinaCounty
import requests
import zipfile
import shutil




def hgtdownload(url, title):

    file =  basedir +"/static/hgt/" + title + ".zip"
    direct = basedir +"/static/hgt/"

    r = requests.get(url)
    with open(file, "wb") as code:
        code.write(r.content)
    unzip_file(file,direct)
    os.remove(file)


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


@web.route('/hgt/3/unzip')
def unzip():
    direct = basedir + "/static/ex/"
    extract = basedir + "/static/exctrat"
    for root, ds, fs in os.walk(direct):
        for f in fs:
            file  =direct +"/"+f
            unzip_file(file,extract)
            os.remove(file)
    move()
    return "done"


def move():
    extract = basedir + "/static/exctrat"
    for root, ds, fs in os.walk(extract):


        for f in fs:
            shutil.move(root+"/"+f,extract+"/"+f)

@web.route("/rename")
def rename_func():
    path = basedir + "/static/hgt"
    for file in os.listdir(path):
        fileNew = file.replace("n","N").replace("s","S").replace("w","W").replace("e","E")

        if(fileNew != file):

            os.rename(path+"/" + file, path + "/"+fileNew)
    return "done"

@web.route('/hgt/3/download')
def hgt3download():
    driver = webdriver.Chrome()
    list= []
    try:
        driver.get("http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org15.htm")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        map = soup.find("map")
        areas = soup.select("area")
        size = len(areas)

        for i in range(0,size):

            areaitem = areas[i]
            href =areaitem.attrs["href"]
            title =areaitem.attrs["title"]
            # try:
            #     hgtdownload(href,title)
            # except Exception,e:
            #     print href
            list.append(href)



    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return json.dumps(list)

@web.route('/gov/static')
def govstatic():
    driver = webdriver.Chrome()
    list= []
    try:
        driver.get("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        trs = soup.select(".provincetr")
        size = len(trs)

        for i in range(3,4):

            tr = trs[i]
            tds = tr.select("td")
            m = len(tds)
            for j in range(0,m):

                try:
                    time.sleep(2)
                    td = tds[j]
                    a = td.find("a")
                    dict = {}
                    href = a.attrs["href"]
                    dict["title"] = a.text
                    provinceurl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"+href
                    driver.get(provinceurl)
                    chtml = driver.page_source
                    csoup = BeautifulSoup(chtml, 'lxml')
                    ctrs = csoup.select(".citytr")
                    csize = len(ctrs)

                    clist =  []



                    for i in range(0, csize):
                        time.sleep(2)
                        ctr = ctrs[i]
                        ctds = ctr.select("td")
                        ca0 = ctds[0].find("a")
                        ca1  =ctds[1].find("a")
                        cdict = {}
                        cdict["code"] = ca0.text
                        cdict["title"] = ca1.text
                        chref = ca0.attrs["href"]
                        try:
                            cityurl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/" + chref
                            driver.get(cityurl)
                            dhtml = driver.page_source
                            dsoup = BeautifulSoup(dhtml, 'lxml')
                            dtrs = dsoup.select(".countytr")
                            dsize = len(dtrs)

                            dlist = []

                            for j in range(0, dsize):
                                try:
                                    dtr = dtrs[j]
                                    dtds = dtr.select("td")
                                    da0 = dtds[0].find("a")
                                    da1 = dtds[1].find("a")
                                    ddict = {}
                                    ddict["code"] = da0.text
                                    ddict["title"] = da1.text
                                    dlist.append(ddict)
                                except:
                                    pass




                            cdict["counties"] = dlist
                        except Exception as  e:

                            cdict["counties"] = [{'code': u'130102000000', 'title': u'\u957f\u5b89\u533a'}, {'code': u'130104000000', 'title': u'\u6865\u897f\u533a'}, {'code': u'130105000000', 'title': u'\u65b0\u534e\u533a'}, {'code': u'130107000000', 'title': u'\u4e95\u9649\u77ff\u533a'}, {'code': u'130108000000', 'title': u'\u88d5\u534e\u533a'}, {'code': u'130109000000', 'title': u'\u85c1\u57ce\u533a'}, {'code': u'130110000000', 'title': u'\u9e7f\u6cc9\u533a'}, {'code': u'130111000000', 'title': u'\u683e\u57ce\u533a'}, {'code': u'130121000000', 'title': u'\u4e95\u9649\u53bf'}, {'code': u'130123000000', 'title': u'\u6b63\u5b9a\u53bf'}, {'code': u'130125000000', 'title': u'\u884c\u5510\u53bf'}, {'code': u'130126000000', 'title': u'\u7075\u5bff\u53bf'}, {'code': u'130127000000', 'title': u'\u9ad8\u9091\u53bf'}, {'code': u'130128000000', 'title': u'\u6df1\u6cfd\u53bf'}, {'code': u'130129000000', 'title': u'\u8d5e\u7687\u53bf'}, {'code': u'130130000000', 'title': u'\u65e0\u6781\u53bf'}, {'code': u'130131000000', 'title': u'\u5e73\u5c71\u53bf'}, {'code': u'130132000000', 'title': u'\u5143\u6c0f\u53bf'}, {'code': u'130133000000', 'title': u'\u8d75\u53bf'}, {'code': u'130171000000', 'title': u'\u77f3\u5bb6\u5e84\u9ad8\u65b0\u6280\u672f\u4ea7\u4e1a\u5f00\u53d1\u533a'}, {'code': u'130172000000', 'title': u'\u77f3\u5bb6\u5e84\u5faa\u73af\u5316\u5de5\u56ed\u533a'}, {'code': u'130181000000', 'title': u'\u8f9b\u96c6\u5e02'}, {'code': u'130183000000', 'title': u'\u664b\u5dde\u5e02'}, {'code': u'130184000000', 'title': u'\u65b0\u4e50\u5e02'}]





                        clist.append(cdict)

                    dict["cities"] = clist
                except Exception as e:

                    print(e)

                list.append(dict)

    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return json.dumps(list)

@web.route('/tide/read')
def tideread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")
        sh = bk.sheets()[0]
        nrows = sh.nrows
        ncols = sh.ncols




        for i in range(1, nrows):
            dict = {}
            row_data = sh.row_values(i)
            dict['station']  = row_data[0]
            dict['province'] = row_data[1]
            dict['lat'] = row_data[3]
            dict['lon'] = row_data[2]
            dict['sealevel'] = row_data[4]
            dict['locationId'] = row_data[5]
            dict['pinyin']  =row_data[6]


            try:
                insert = chinaTidalStation(dict=dict)
                db.session.add(insert)
                db.session.commit()
            except Exception as  e:
                print(e)
                db.session.rollback()
        return 'done'

@web.route('/worldstattion')
def worldstation():
    driver = webdriver.Chrome()
    driver.get('https://cdn.xunquan.shop/html/tidestation.html')

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    containerdiv = soup.find_all('div', attrs={'class': 'container'})[1]
    rowcontainer = containerdiv.find('div', attrs={'class': 'row'})
    rowlist =  rowcontainer.find_all('div', attrs={'class': 'row'})
    for row in rowlist:
        try:
            contry_line = row.find_all('div')[0]
            contry  =contry_line.find('h4')
            if contry:
                # h4 = contry.find('h4')
                contry_name = contry.text
            else:
                contry_name = ""
        except:
            contry_name = ''

        stations = row.find_all('div', attrs={'class': 'col-md-3'})

        for station in stations:
            result = {}
            a = station.find('a')
            herf = a.attrs['href']
            items = herf.split('&')
            lat = items[0].split('=')[1]
            long = items[1].split('=')[1]
            result['countryName'] = contry_name
            result['lat'] = lat
            result['long'] = long
            result['stationName'] = a.text

            try:
                insert = worldTidalStation(dict=result)
                db.session.add(insert)
                db.session.commit()
            except:
                db.session.rollback()


    driver.quit()
    return 'done'

@web.route('/checkstation')
def checkstation():
    dict = {}
    africa  ='Africa'
    dict['Angola'] = africa
    dict['Benin'] = africa
    dict['Cameroun'] = africa
    dict['Congo'] = africa
    dict['Egypt'] = africa
    dict['Gabon'] = africa
    dict['Gambia'] = africa
    dict['Ghana']  =africa
    dict['Guinea']  =africa
    dict['Guinea Ecuatorial']  =africa
    dict['Kenya'] = africa
    dict['Liberia'] = africa
    dict['Madagasikara']  =africa
    dict['Morocco'] = africa
    dict['Mozambique']  =africa
    dict['Namibia']  =africa
    dict['Nigeria']  =africa
    dict['São Tomé e Príncipe']  =africa
    dict['Senegal']  =africa
    dict['Sierra Leone']  =africa
    dict['Somalia']  =africa
    dict['South Africa']  =africa
    dict['Spain']  = africa
    dict['Tanzania']  =africa
    dict['Togo']  =africa
    dict['Tunisia']  =africa
    dict['Yemen']  =africa


    asia = 'Asia'
    dict['Brunei']  =asia
    dict['Burma']  = asia
    dict['China']  =asia
    dict['Cyprus'] = asia
    dict['Greece']  =asia
    dict ['India'] =asia
    dict['Indonesia']  =asia
    dict['Iran']  =asia
    dict['Japan']  = asia
    dict['Lebanon'] = asia
    dict['Malaysia']  =asia
    dict['North Korea'] =asia
    dict['Oman'] = asia
    dict['Pakistan']  =asia
    dict['Paracel Islands']  =asia
    dict['Philippines']  =asia
    dict['Russia']  =asia
    dict['South Korea']  =asia
    dict['Taiwan']  =asia
    dict['Thailand']  =asia
    dict['Timor-Leste']  =asia
    dict['United Arab Emirates']  =asia
    dict['Viet Nam']  =asia
    dict['Yemen']  =asia


@web.route("/china/city")
def chinacity():
    uploadath = os.path.join(basedir, 'static/uploads')
    xlspath = os.path.join(uploadath, "china_city_data.json")

    with open(xlspath, "r") as f:
        arr = json.load(f)

    for province in arr:
        for city in province["list"]:
            for county in city["list"]:
                countyobject  = ChinaCounty()
                countyobject.countyCode = county["code"]
                countyobject.countyName= county["name"]
                countyobject.cityName = city["name"]
                countyobject.cityCode =city["code"]
                countyobject.provinceCode = province["code"]
                countyobject.provinceName = province["name"]
                try:
                    db.session.add(countyobject)
                    db.session.commit()

                except Exception as e:

                    db.session.rollback()


    return "done"



