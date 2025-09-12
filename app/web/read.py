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
from app.allcoupon import allcoupon
import urllib
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import logging
import sys
import random

from app.pintuan import pintuan

from app.appuser import appuser

from config import basedir
from  app.utils.constvalue import appkey,secret,xunquanAppkey,xunquanSecret,solarAppkey,solarSecret,site_id
from app.worldTidalStation import worldTidalStation
from app.chinaTidalStation import chinaTidalStation

from app.Star import Star
from app.NGCC import NGCC
from app.Messier import Messier
from app.Constellation import Constellation
from app.Tycho import Tycho
from app.stardetail import stardetail
from app.ConstellationDetail import ConstellationDetail
from app.Caldwell import Caldwell
import re

from app.MeteorShowers import MeteorShowers
from app.AstroEvent import AstroEvent
from app.Comet import Comet
from app.Galaxy import Galaxy
from app.GlobularClusters import GlobularClusters
from app.OpenClusters import OpenClusters
from app.ProtoplanetaryNebulae import ProtoplanetaryNebulae
from app.PlanetaryNebulae import PlanetaryNebulae
from app.DiffuseNebulae import DiffuseNebulae
from app.DeepskyDetail import DeepskyDetail
from app.CometDetail import CometDetail
from config import basedir
import requests
import zipfile
import shutil




beginTime = datetime.datetime.strptime('2017-10-01', "%Y-%m-%d")





@web.route("/nager/date/countries")
def nagedatecountries():
    driver = webdriver.Chrome()
    result  = []
    try:
        driver.get("https://date.nager.at/Home/Countries")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find("div", attrs={"class": "table-responsive"})
        table = div.find("table", attrs={"class": "table"})
        trs = table.select("tr")
        for tr in trs:
            tds = tr.select("td")
            if len(tds) > 2:
                dict = {}
                td0  = tds[0]
                td1 = tds[1]
                dict["name"] = td0.text
                dict["code"] = td1.text
                result.append(dict)
    except Exception as e:
        print(e)
    finally:
        pass


    driver.quit()
    return json.dumps(result)







@web.route("/star/fix")
def starfix():
    try:

        stars = Star.query.filter(Star.ChineseName.like("%（页面不存在）%")).all()
        for starobject in stars:

            name= starobject.ChineseName




            starobject.ChineseName= name.replace("（页面不存在）","")
            try:
                db.session.commit()
            except Exception as  e:
                print(e)
                db.session.rollback()


    except Exception as  e:
        print (e)
        db.session.rollback()

    finally:
        db.session.close()
    return "done"

@web.route("/star/detail")
def stardetailstring():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(Star).all()
        for starobjcet in stars:
            link = starobjcet.EnglishLink
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                if header.find("p") > 0:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("h2") > 0:
                    textsting = i.text
                    if textsting.find("eferences") > 0:
                        break
                    elif textsting.find("also") > 0:
                        pass
                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"

            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)

            # break

            b = a.encode()

            # break


            try:
                stardetailobject = stardetail(Id=starobjcet.CombinedId)
                stardetailobject.EnglishHtmL = b



                db.session.add(stardetailobject)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

                continue

            # break
            time.sleep(0.5)






    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"





@web.route("/star/detail/zh")
def stardetailstring_zh():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(Star).all()
        for starobjcet in stars:
        # for i in range(0,1):
            link = starobjcet.ChineseLink
            # link = "https://zh.m.wikipedia.org/wiki/%E5%A4%A9%E7%8B%BC%E6%98%9F"
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})

            # print div

            if div is None:
                continue

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                # print header
                if header.find("se") > 0:
                    for j in i.contents:
                        headerj = str(j)[:3]
                        if headerj.find("<p")>-1:
                            strings = strings + "<p>" + j.text + "</p>"
                elif header.find("h2") > 0:
                    textsting = i.text
                    if textsting.find("参考资料") > -1:
                        break
                    elif textsting.find("参考文献") > -1:
                        break
                    elif textsting.find("参见") > -1:
                        break
                    elif textsting.find("外部链接") > -1:
                        pass

                    else:
                        strings = strings + "<h2>" + i.text.replace("编辑","") + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"




            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


            # return strings

            # break

            b = a.encode()


            try:
                stardetailobjects = db.session.query(stardetail).filter(stardetail.CombinedId == starobjcet.CombinedId).all()

                if len(stardetailobjects) > 0:
                    stardetailobject = stardetailobjects[0]
                    stardetailobject.ChineseHTML= b
                    db.session.commit()


                else:
                    newstardetailobject = stardetail(Id=starobjcet.CombinedId)

                    newstardetailobject.ChineseHTML = b
                    db.session.add(newstardetailobject)
                    db.session.commit()
            except Exception as e:
                print(e)

                db.session.rollback()

                continue

            # break
            time.sleep(0.7)






    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"

@web.route("/constellation/detail/zh")
def constellationdetailstring_zh():


    driver = webdriver.Chrome()


    try:
        constellations = db.session.query(Constellation).all()
        for constellationobject in constellations:
        # for i in range(0,1):
            link = constellationobject.chineseLink
            # link = "https://zh.wikipedia.org/wiki/%E4%BB%99%E5%A5%B3%E5%BA%A7"
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div0 = soup.find("div",attrs={"class":"mw-content-ltr"})
            div = div0.find("div", attrs={"class": "mw-parser-output"})

            # print div

            if div is None:
                continue

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                # print header
                if header.find("<ul") > -1:
                    strings = strings + "<ul>"
                    for j in i.contents:
                        headerj = str(j)[:3]
                        if headerj.find("<li")>-1:
                            strings = strings + "<li>" + j.text + "</li>"
                    strings  = strings +"</ul>"
                elif header.find("<p")>-1:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("<h2") > -1:
                    textsting = i.text
                    if textsting.find("参考资料") > -1:
                        break
                    elif textsting.find("参考文献") > -1:
                        break
                    elif textsting.find("参见") > -1:
                        break
                    elif textsting.find("外部链接") > -1:
                        pass

                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"




            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


            # return a

            # break

            b = a.encode()


            try:
                # stardetailobjects = db.session.query(ConstellationDetail).filter(ConstellationDetail.shortname == starobjcet.CombinedId).all()
                #
                # if len(stardetailobjects) > 0:
                #     stardetailobject = stardetailobjects[0]
                #     stardetailobject.ChineseHTML= b
                #     db.session.commit()
                #
                #     print stardetailobject.CombinedId
                # else:
                    newconsetallationobject = ConstellationDetail(name=constellationobject.shortname)
                    # print newstardetailobject.CombinedId
                    newconsetallationobject.ChineseHTML = b
                    newconsetallationobject.ChineseLink = link
                    db.session.add(newconsetallationobject)
                    db.session.commit()
            except Exception as e:


                db.session.rollback()
                print(e)
                continue

            # break
            time.sleep(0.7)






    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"

@web.route("/constellation/detail/en")
def constellationdetailstring_en():


    driver = webdriver.Chrome()


    try:
        constellations = db.session.query(Constellation).all()
        for constellationobject in constellations:
        # for i in range(0,1):
            link = constellationobject.englishLink
            # link = "https://zh.wikipedia.org/wiki/%E4%BB%99%E5%A5%B3%E5%BA%A7"
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div0 = soup.find("div",attrs={"class":"mw-content-ltr"})
            div = div0.find("div", attrs={"class": "mw-parser-output"})

            # print div

            if div is None:
                continue

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                # print header
                if header.find("<ul") > -1:
                    strings = strings + "<ul>"
                    for j in i.contents:
                        headerj = str(j)[:3]
                        if headerj.find("<li")>-1:
                            strings = strings + "<li>" + j.text + "</li>"
                    strings  = strings +"</ul>"
                elif header.find("<p")>-1:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("<h2") > -1:
                    textsting = i.text
                    if textsting.find("Notes") > -1:
                        break
                    elif textsting.find("eferences") > -1:
                        break
                    elif textsting.find("Sources") > -1:
                        break
                    elif textsting.find("External links") > -1:
                        break
                    elif textsting.find("See also")  > -1:
                        break


                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"




            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


            # return a

            # break

            b = a.encode()


            try:
                consetallationDetailobjects = db.session.query(ConstellationDetail).filter(ConstellationDetail.shortname == constellationobject.shortname).all()

                if len(consetallationDetailobjects) > 0:
                    consetallationDetailobject = consetallationDetailobjects[0]
                    consetallationDetailobject.EnglishLink = link
                    consetallationDetailobject.EnglishHTML= b
                    db.session.commit()

                    print (consetallationDetailobject.shortname)
                else:
                    newconsetallationobject = ConstellationDetail(name=constellationobject.shortname)
                    # print newstardetailobject.CombinedId
                    newconsetallationobject.EnglishHTML = b
                    newconsetallationobject.EnglishLink = link
                    db.session.add(newconsetallationobject)
                    db.session.commit()
            except Exception as e:


                db.session.rollback()
                print(e)
                continue

            # break
            time.sleep(0.7)






    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"


@web.route("/constellation/bounduray")
def constellation_bounduray():

    try:
        constellations = db.session.query(Constellation).all()
        for constellationobject in constellations:



            continue



            try:

                abb = constellationobject.shortname

                url = "https://www.iau.org/static/public/constellations/txt/"+abb.lower() +".txt"

                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                content = response.read()
                strings = json.dumps(content)

                strings = strings.replace("r","")
                strings = strings.replace("n","")
                strings = strings.replace("\\","")

                # return strings





                list = strings.split("|"+abb,-1)


                # return json.dumps(list)



                resultlist = []

                n = len(list)

                for i in  range(0,n):
                    location = list[i]
                    if len(location) < 5:
                        continue
                    # newlocation = location.replace("\n","")
                    muple  = location.split("|",-1)
                    dict ={}
                    lon = muple[0]
                    index = lon.find("n")
                    if  index >0:
                        lon = lon[index+1:]
                    index0 = lon.find("\"") > -1
                    if  index0 > -1:
                        lon = lon[index0:]


                    lat = muple[1].replace(" ","")
                    dict["lon"] = lon
                    dict["lat"]  = lat
                    resultlist.append(dict)

                jsonstring = json.dumps(resultlist)
                # print jsonstring
                # resultstring.replace("--","-")
                # resultstring.replace("\"","")

                b = str.encode(jsonstring)




                # print len(b)

                # print jsonstring

                try:
                    constellationobject.boundary = b
                    db.session.commit()
                except Exception as e:

                    db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
                continue

    except Exception as e:

        print(e)
        db.session.rollback()
    finally:
        # db.session.close()
        pass







    return  "done"



@web.route("/constellation/detail/jp")
def constellationdetailstring_jp():


    driver = webdriver.Chrome()


    try:
        constellations = db.session.query(Constellation).all()
        for constellationobject in constellations:
        # for i in range(0,1):
            link = constellationobject.japaneseLink
            # link = "https://zh.wikipedia.org/wiki/%E4%BB%99%E5%A5%B3%E5%BA%A7"
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div0 = soup.find("div",attrs={"class":"mw-content-ltr"})
            div = div0.find("div", attrs={"class": "mw-parser-output"})

            # print div

            if div is None:
                continue

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                # print header
                if header.find("<ul") > -1:
                    strings = strings + "<ul>"
                    for j in i.contents:
                        headerj = str(j)[:3]
                        if headerj.find("<li")>-1:
                            strings = strings + "<li>" + j.text + "</li>"
                    strings  = strings +"</ul>"
                elif header.find("<p")>-1:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("<h2") > -1:
                    textsting = i.text
                    if textsting.find("出典") > -1:
                        break
                    elif textsting.find("脚注") > -1:
                        break
                    elif textsting.find("外部リンク")   >-1:
                        break
                    elif textsting.find("関連項目") > -1:
                        break
                    elif textsting.find("注釈") >-1:
                        break

                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"




            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


            # return a

            # break

            b = a.encode()


            try:
                consetallationDetailobjects = db.session.query(ConstellationDetail).filter(ConstellationDetail.shortname == constellationobject.shortname).all()

                if len(consetallationDetailobjects) > 0:
                    consetallationDetailobject = consetallationDetailobjects[0]
                    consetallationDetailobject.JapaneseLink = link
                    consetallationDetailobject.JapaneseHTML= b
                    db.session.commit()


                else:
                    newconsetallationobject = ConstellationDetail(name=constellationobject.shortname)
                    # print newstardetailobject.CombinedId
                    newconsetallationobject.JapaneseHTML = b
                    newconsetallationobject.JapaneseLink = link
                    db.session.add(newconsetallationobject)
                    db.session.commit()
            except Exception as e:


                db.session.rollback()
                print(e)
                continue

            # break
            time.sleep(0.7)






    except Exception as e:
        print (e)
        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"




@web.route("/star/detail/fix")
def stardetailstring_fix():

    try:
        stars = db.session.query(Star).all()
        for starobjcet in stars:



            try:
                stardetailobjects = db.session.query(stardetail).filter(stardetail.CombinedId == starobjcet.CombinedId).all()

                if len(stardetailobjects) > 0:
                    stardetailobject = stardetailobjects[0]
                    stardetailobject.JapaneseLink= starobjcet.JapaneseLink
                    stardetailobject.EnglishLink = starobjcet.EnglishLink
                    stardetailobject.ChineseLink = starobjcet.ChineseLink
                    db.session.commit()



            except Exception as e:


                db.session.rollback()

                continue




    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()







    return  "done"



@web.route("/star/detail/jp")
def stardetailstring_jp():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(Star).all()
        for starobjcet in stars:
            link = starobjcet.JapaneseLink
            # link = "https://zh.wikipedia.org/wiki/%E5%A3%81%E5%AE%BF%E4%BA%8C"
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})

            # print div

            if div is None:
                continue

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                if header.find("p") > 0:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("h2") > 0:
                    textsting = i.text
                    if textsting.find("出典") > -1:
                        break
                    elif textsting.find("脚注") > -1:
                        break
                    elif textsting.find("外部リンク")   >-1:
                        pass
                    elif textsting.find("関連項目") > -1:
                        pass
                    elif textsting.find("注釈") >-1:
                        break


                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"

            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)

            # break

            b = a.encode()


            try:
                stardetailobjects = db.session.query(stardetail).filter(stardetail.CombinedId == starobjcet.CombinedId).all()

                if len(stardetailobjects) > 0:
                    stardetailobject = stardetailobjects[0]
                    stardetailobject.JapaneseHTML= b
                    db.session.commit()


                else:
                    newstardetailobject = stardetail(Id=starobjcet.CombinedId)

                    newstardetailobject.JapaneseHTML = b
                    db.session.add(newstardetailobject)
                    db.session.commit()
            except Exception as e:


                db.session.rollback()

                continue

            # break
            time.sleep(0.7)






    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()






    driver.quit()
    return  "done"


@web.route("/star/list")
def starlist():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find("table",attrs={"class":"multicol"})
    linkArray = []

    for li in table.select("li"):
        dict={}
        dict["title"]  = li.text
        a =  li.find('a')
        dict['link'] = "https://en.wikipedia.org"+ a.attrs["href"]
        linkArray.append(dict)

    # return json.dumps(linkArray)

    linkArray0 = []

    for dict in linkArray:
        url  = dict["link"]
        driver.get(url)
        html0 = driver.page_source
        soup0 = BeautifulSoup(html0, 'lxml')
        content = soup0.find("div",attrs={"id":"bodyContent"})
        table = content.find("table")
        tbody = table.find("tbody")

        items = tbody.select("tr")

        count = len(items)

        for i in range(0,count):
             row = items[i]
             dict0 = {}
             dict0["ConsetellationName"] = dict["title"]
             # print row
             cells = row.select("td")
             if cells is None   or len(cells) <6:
                 continue
             cell0 = cells[0]
             dict0["EnglishName"] = ""
             dict0["ShortName"] =cell0.text

             dict0["EnglishLink"]  =""
             a = cell0.find("a")
             if a:
                 try:
                     dict0["EnglishName"] = a.attrs["title"]
                 except:
                     pass
                 try:
                     dict0["EnglishLink"] = "https://en.wikipedia.org"+a.attrs['href']
                 except:
                     pass
             dict0["BaierId"] = cells[1].text
             cellcount = len(cells)

             dict0["HDId"] = cells[cellcount-9].text
             dict0["HIPId"] = cells[cellcount-8].text
             dict0["CombinedId"] = dict0["HDId"]+"-"+dict0["HIPId"]
             if len(dict0["CombinedId"]) < 2:
                 continue
             dict0["RightAscension"] = cells[cellcount-7].text
             dict0['Declination'] = cells[cellcount-6].text
             dict0["Magnitude"] = cells[cellcount-5].text
             dict0["AbsoluteMagnitude"] = cells[cellcount-4].text
             dict0["Distance"]  = cells[cellcount-3].text
             dict0["SpectralType"] = cells[cellcount-2].text

             starobject = Star(dict = dict0)
             try:
                 db.session.add(starobject)
                 db.session.commit()
             except Exception as  e:

                 db.session.rollback()
             finally:

                 db.session.flush()






        time.sleep(1)


    db.session.close()
    driver.quit()




@web.route("/star/list/zh")
def starlist_zh():
    driver = webdriver.Chrome()
    driver.get("https://zh.m.wikipedia.org/wiki/%E6%98%9F%E5%BA%A7%E6%81%92%E6%98%9F%E5%88%97%E8%A1%A8")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find("table",attrs={"class":"multicol"})
    linkArray = []
    for li in table.select("li"):
        dict={}
        dict["title"]  = li.text
        a =  li.find('a')
        dict['link'] = "https://zh.m.wikipedia.org/"+ a.attrs["href"]
        linkArray.append(dict)

    # return json.dumps(linkArray)

    linkArray0 = []

    for dict in linkArray:
        url  = dict["link"]
        driver.get(url)
        html0 = driver.page_source
        soup0 = BeautifulSoup(html0, 'lxml')
        content = soup0.find("div",attrs={"id":"bodyContent"})
        table = content.find("table")
        tbody = table.find("tbody")

        items = tbody.select("tr")

        count = len(items)

        for i in range(0,count):
             row = items[i]
             dict0 = {}
             # dict0["ConsetellationName"] = dict["title"]
             # print row
             cells = row.select("td")
             if cells is None or len(cells) < 6:
                 continue
             cell0 = cells[0]
             dict0["ChineseName"] = cell0.text
             # dict0["ShortName"] =cell0.text
             # dict0["ChineseLink"]  =""
             a = cell0.find("a")
             if a:

                 try:
                     # dict0["ChineseLink"] = "https://zh.m.wikipedia.org/"+a.attrs['href']
                     dict0["ChineseName"] = a.attrs["title"]
                 except:
                     pass
             # dict0["BaierId"] = cells[1].text
             cellcount = len(cells)

             dict0["HDId"] = cells[cellcount-9].text
             dict0["HIPId"] = cells[cellcount-8].text
             dict0["CombinedId"] = dict0["HDId"]+"-"+dict0["HIPId"]
             if len(dict0["CombinedId"]) < 2:
                 continue
             # dict0["RightAscension"] = cells[cellcount-7].text
             # dict0['Declination'] = cells[cellcount-6].text
             # dict0["Magnitude"] = cells[cellcount-5].text
             # dict0["AbsoluteMagnitude"] = cells[cellcount-4].text
             # dict0["Distance"]  = cells[cellcount-3].text
             # dict0["SpectralType"] = cells[cellcount-2].text

             # starobject = star(dict = dict0)
             try:
                 starobject =  db.session.query(Star).filter(Star.CombinedId == dict0["CombinedId"])[0]
                 starobject.ChineseName = dict0["ChineseName"]
                 # starobject.ChineseLink = dict0["ChineseLink"]
                 db.session.commit()
             except Exception as e:

                 db.session.rollback()
             finally:

                 db.session.flush()






        time.sleep(1)


    db.session.close()
    driver.quit()





@web.route("/star/test")
def startest11():
    driver  = webdriver.Chrome()
    driver.get("https://zh.m.wikipedia.org/wiki/%E6%98%9F%E5%AE%BF%E4%B8%80")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div0 = soup.find("div",attrs={"class":"pre-content heading-holder"})
    div1 = div0.find("div",attrs={"class":"page-heading"})
    h1 = div1.find("h1")
    driver.quit()
    return h1.text





@web.route("/star/fix/chinese")
def starlistfixchinese():
    # list =[]
    driver = webdriver.Chrome()

    i= 0
    try:
        stars = db.session.query(Star).filter(Star.ChineseLink.like("%http%")).all()
        for starobjcet in stars:
            i= i+1
            if i < 2500:
                continue

            driver.get(starobjcet.ChineseLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            try:
              div0 = soup.find("div", attrs={"class": "pre-content heading-holder"})
              div1 = div0.find("div", attrs={"class": "page-heading"})
              h1 = div1.find("h1")
            except Exception as e:

                continue
            try:
                name = h1.text

                if len(name) > 0:
                    starobjcet.ChineseName = name
                    db.session.commit()
            except Exception as e:

                db.session.rollback()
            finally:
                time.sleep(1)



    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    driver.quit()
    return "done"



    # return json.dumps(list)


@web.route("/meter/shower")
def metershower():
    driver = webdriver.Chrome()
    driver.get("https://www.amsmeteors.org/meteor-showers/2017-meteor-shower-list/")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    aticle = soup.find("article",attrs={"class":"post-6876 page type-page status-publish hentry"})
    tabels = aticle.select("table")
    count = len(tabels)
    result = {}
    list = []
    for i in range(0,count-1):
        if i > 1:
            continue
        table = tabels[i]
        trs =  table.select("tr")
        trcount = len(trs)
        for j in  range(2,trcount-2):
            dict ={}
            dict["classlevel"] = i+1
            dict["show"] = i < 1
            tr = trs[j]
            tds = tr.select("td")
            name = tds[0].text
            index1 = name.find("(")
            index2 = name.find(")")
            englishname = name[:index1-1]
            shortname = name[index1+1:index2]
            dict["englishname"] = englishname
            dict["shortname"] = shortname
            dict["ActivityPeriod"] = tds[1].text
            dict["SL"] = tds[3].text
            dict["Maximum"] = tds[2].text
            dict["RightAscension"] = tds[4].text
            dict["Declination"] = tds[5].text
            dict["Velocity"] = tds[6].text
            dict["r"] = tds[7].text
            dict['ZHR'] = tds[8].text
            dict["time"] = tds[9].text
            dict["moon"] = tds[10].text
            dict["year"] = "2020"
            try:
                metershowerobject = MeteorShowers(dict = dict)
                db.session.add(metershowerobject)
                db.session.commit()

            except Exception as e:

                db.session.rollback()

            list.append(dict)
    driver.quit()
    return json.dumps(list)









@web.route("/star/list/jp")
def starlist_jp():
    driver = webdriver.Chrome()
    driver.get("https://ja.wikipedia.org/wiki/%E6%98%9F%E5%BA%A7%E5%88%A5%E3%81%AE%E6%81%92%E6%98%9F%E3%81%AE%E4%B8%80%E8%A6%A7")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find("table",attrs={"class":"multicol"})
    linkArray = []
    for li in table.select("li"):
        dict={}
        dict["title"]  = li.text
        a =  li.find('a')
        dict['link'] = "https://ja.wikipedia.org"+ a.attrs["href"]
        linkArray.append(dict)

    # return json.dumps(linkArray)

    linkArray0 = []

    for dict in linkArray:
        url  = dict["link"]
        driver.get(url)
        html0 = driver.page_source
        soup0 = BeautifulSoup(html0, 'lxml')
        content = soup0.find("div",attrs={"id":"bodyContent"})
        table = content.find("table")
        tbody = table.find("tbody")

        items = tbody.select("tr")

        count = len(items)

        for i in range(0,count):
             row = items[i]
             dict0 = {}
             # dict0["ConsetellationName"] = dict["title"]
             # print row
             cells = row.select("td")

             if cells is None or len(cells) < 6:
                 continue

             cell0 = cells[0]
             dict0["JapaneseName"] = cell0.text
             # dict0["ShortName"] =cell0.text
             dict0["JapaneseLink"]  =""
             a = cell0.find("a")
             if a:

                 try:
                     dict0["JapaneseLink"] = "https://ja.wikipedia.org"+a.attrs['href']
                 except:
                     pass
             # dict0["BaierId"] = cells[1].text
             cellcount = len(cells)

             dict0["HDId"] = cells[cellcount-9].text
             dict0["HIPId"] = cells[cellcount-8].text
             dict0["CombinedId"] = dict0["HDId"]+"-"+dict0["HIPId"]
             if len(dict0["CombinedId"]) < 2:
                 continue
             # dict0["RightAscension"] = cells[cellcount-7].text
             # dict0['Declination'] = cells[cellcount-6].text
             # dict0["Magnitude"] = cells[cellcount-5].text
             # dict0["AbsoluteMagnitude"] = cells[cellcount-4].text
             # dict0["Distance"]  = cells[cellcount-3].text
             # dict0["SpectralType"] = cells[cellcount-2].text

             # starobject = star(dict = dict0)
             try:
                 starobject =  db.session.query(Star).filter(Star.CombinedId == dict0["CombinedId"])[0]
                 starobject.JapaneseName = dict0["JapaneseName"]
                 starobject.JapaneseLink = dict0["JapaneseLink"]

                 db.session.commit()
             except Exception as  e:

                 db.session.rollback()
             finally:

                 db.session.flush()






        time.sleep(1)


    db.session.close()
    driver.quit()


@web.route("/NGCC/list")
def NGCClist():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_NGC_objects")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div0 = soup.find("div",attrs={"id":"mw-content-text"})
    div1 = div0.find("div",attrs={"class":"mw-parser-output"})
    ul = div1.find("ul")
    linkArray = []
    linkList = []
    for li in ul.select("li"):
        dict={}
        dict["title"]  = li.text
        a =  li.find('a')
        dict['link'] = "https://en.wikipedia.org"+ a.attrs["href"]
        linkArray.append(dict)
    for dict in linkArray:
        url = dict["link"]
        driver.get(url)
        html0 = driver.page_source
        soup0 = BeautifulSoup(html0, 'lxml')
        content = soup0.find("div",attrs={"id":"bodyContent"})
        tables = content.select("table")
        for table in tables:
            rows = table.select("tr")
            rowcount = len(rows)

            for i in range(1,rowcount):
                try:
                    resultdict = {}
                    row = rows[i]
                    cells = row.select("td")
                    if  len(cells) < 6:
                        continue

                    cell0 = cells[0]
                    resultdict["title"] = ""


                    resultdict["englishLink"] = ""
                    a = cell0.find("a")
                    if a:
                        try:
                            resultdict["title"] = a.attrs["title"]
                        except:
                            pass
                        try:
                            resultdict["englishLink"] = "https://en.wikipedia.org" + a.attrs['href']
                        except:
                            pass

                    resultdict["number"] = cells[0].text
                    resultdict['otherName'] = cells[1].text
                    resultdict["obejectType"] = cells[2].text
                    resultdict["constellation"] = cells[3].text
                    resultdict["RightAscension"] = cells[4].text
                    resultdict["Declination"] = cells[5].text
                    resultdict["Magnitude"] = cells[6].text
                    # linkList.append(resultdict)
                    try:
                        insert = NGCC(dict=resultdict)
                        db.session.add(insert)
                        db.session.commit()
                    except Exception as  e:

                        db.session.rollback()
                    finally:
                        db.session.flush()
                except Exception as e:
                    print(e)
                finally:
                    pass
            # break


        time.sleep(1)
        # break
    driver.quit()
    return json.dumps(linkList)


@web.route("/messier/fix")
def misserfix():
    messiers = db.session.query(Messier).all()
    driver = webdriver.Chrome()
    for messierobject in messiers:
        url = messierobject.picture

        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find("div", attrs={"class", "fullImageLink"})
        try:

            a = div.find("a")
            link = "https:"+a.attrs["href"]

            messierobject.picture  = link
            db.session.commit()

        except Exception as  e :

            db.session.rollback()
        time.sleep(1)
    driver.quit()
    db.session.close()

@web.route("/messier/list")
def messierlist():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/Messier_object")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find("table",attrs={"class":"wikitable sortable jquery-tablesorter"})
    rows  = table.select("tr")
    rowcount = len(rows)
    list = []
    for i in range(1,rowcount):
        dict = {}
        row = rows[i]

        th  = row.find("th")
        number = th.text
        index = number.find("[")
        if index >0:
            dict["number"] = number[:index]
        else:
            dict["number"] = number
        dict["englishLink"] = ""
        try:
            a = th.find("a")
            dict["englishLink"] = "https://en.wikipedia.org" + a.attrs['href']
            dict["title"] = a.attrs['title']

        except:
            pass
        cells = row.select("td")
        if  len(cells) < 7:
            continue
        dict["NGCCIC_number"]  =cells[0].text
        dict["commonName"] = cells[1].text
        picture = cells[2]
        picture_a = picture.find("a")
        dict["picture"] =  "https://en.wikipedia.org" + picture_a.attrs['href']
        dict["obejectType"] =  cells[3].text
        dict["Distance"] = cells[4].text
        dict["constellation"]  =cells[5].text
        dict["Magnitude"] =cells[6].text
        dict["RightAscension"] = cells[7].text
        dict["Declination"] = cells[8].text
        list.append(dict)
        try:
            insert  = Messier(dict=dict)
            db.session.add(insert)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            pass

    driver.quit()
    db.session.close()
    return json.dumps(list)

@web.route("/caldwell/fix")
def carldwellfix():
    messiers = db.session.query(Caldwell).all()
    driver = webdriver.Chrome()
    for messierobject in messiers:
        # url = messierobject.picture
        #
        # if len(url) < 5:
        #     continue
        # print url
        # driver.get(url)
        # html = driver.page_source
        # soup = BeautifulSoup(html, 'lxml')
        # div = soup.find("div", attrs={"class", "fullImageLink"})


        pic = messierobject.picture
        i = pic.find("en.wikipedia")
        if i> 0:
            try:
                # print messierobject.number
                # num = messierobject.number
                # print messierobject.EnglishLink


                # if num == "C10":
                #     messierobject.RightAscension  ="01h 46.0m"
                # elif num =="C13":
                #     messierobject.RightAscension = "01h 19m 32.6s"
                # elif num == "C4":
                #     messierobject.RightAscension  ="21h 01m 35.60s"
                # elif num == "C76":
                #     messierobject.RightAscension = "16h 54m"
                # elif num == "C9":
                #     messierobject.RightAscension = "22h 57m 17.14s"
                # elif num == "C96":
                #     messierobject.RightAscension = "7h 58m 20s"
                # elif num == "C97":
                #     messierobject.RightAscension = "11h 36.1m"
                # elif num == "C99":
                #     messierobject.RightAscension  ="12h 50m"




                # a = div.find("a")
                # link = "https:"+a.attrs["href"]
                # print link
                # messierobject.Declination ="+27° 58′ 37″"

                driver.get(pic)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"class", "fullImageLink"})
                a = div.find("a")
                fullurl =  "https:"+ a.attrs["href"]
                messierobject.picture  =fullurl


                db.session.commit()

            except Exception as  e:
                print(e)
                # db.session.rollback()

    driver.quit()
    db.session.close()
    return "done"


@web.route("/caldwell/list")
def caldwell():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/Caldwell_catalogue")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find("table",attrs={"class":"wikitable sortable jquery-tablesorter"})
    rows  = table.select("tr")
    rowcount = len(rows)
    list = []
    for i in range(1,rowcount-1):
        dict = {}
        row = rows[i]



        cells = row.select("td")
        dict["number"] = cells[0].text
        dict["NGCCIC_number"]  =cells[1].text
        try:
            link = cells[1].find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + link.attrs["href"]
        except:
            try:
                link = cells[2].find("a")
                dict["EnglishLink"] = "https://en.wikipedia.org" + link.attrs["href"]
            except:
                pass
        dict["commonName"] = cells[2].text
        picture = cells[3]
        try:
            picture_a = picture.find("a")
            dict["picture"] =  "https://en.wikipedia.org" + picture_a.attrs['href']
        except:
            dict["picture"] = ""


        dict["obejectType"] =  cells[4].text
        dict["Distance"] = cells[5].text
        dict["constellation"]  =cells[6].text
        dict["Magnitude"] =cells[7].text
        dict["RightAscension"] = ""
        dict["Declination"] = ""
        try:
            driver.get(dict["EnglishLink"])
            html2 = driver.page_source
            soup2 = BeautifulSoup(html2, 'lxml')

            table2 = soup2.find("table", attrs={"class": "infobox"})
            rows2 = table2.select("tr")
            for row2 in rows2:
                try:
                    th2  = row2.find("th")
                    a2 = th2.find("a")
                    atext2 = a2.text
                    if atext2 == "Right ascension":
                        rctd = row2.find("td", attrs={"class": "infobox-data"})
                        rcspan = rctd.find("span")
                        rac = rcspan.text
                        i = rac.find("[")
                        if i > 0:
                            dict["RightAscension"] = rac[:i]
                        else:
                            dict["RightAscension"] = rac
                    elif atext2 == "Declination":
                        dectd = row2.find("td", attrs={"class": "infobox-data"})
                        dec = dectd.text
                        i = dec.find("[")
                        if i > 0:
                            dict["Declination"] =dec[:i]
                        else:

                            dict["Declination"] = dec
                except Exception as e:
                    print(e)






        except Exception as e:
            print(e)
            pass
        finally:
            time.sleep(1)
        list.append(dict)
        try:
            insert  = Caldwell(dict=dict)
            db.session.add(insert)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            pass

    driver.quit()
    db.session.close()
    return json.dumps(list)




@web.route("/constellation/list")
def constellationlist():
    driver = webdriver.Chrome()
    driver.get("https://zh.wikipedia.org/wiki/%E6%98%9F%E5%BA%A7%E5%88%97%E8%A1%A8")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find("table",attrs={"class":"wikitable sortable jquery-tablesorter"})
    rows  = table.select("tr")
    rowcount = len(rows)
    list = []

    for i in  range(1,rowcount):
        dict = {}
        row = rows[i]
        cells = row.select("td")
        cell0  = cells[0]
        dict["chinesename"] = cell0.text
        dict["chineseLink"] = ""
        try:
            a = cell0.find("a")
            dict["chineseLink"] ="https://zh.wikipedia.org/"+ a.attrs["href"]
        except Exception as  e :
            print(e)
        dict["shortname"] = cells[1].text
        dict["latinname"] = cells[2].text
        dict["size"] = cells[3].text
        dict["RightAscension"]  =cells[4].text
        dict["Declination"] = cells[5].text
        dict["quadrant"]  =cells[6].text
        dict["family"] = cells[7].text
        dict["brightest_ch"] = cells[8].text

        try:
            insert = Constellation(dict = dict)
            db.session.add(insert)
            db.session.commit()
        except Exception as  e:
            print(e)
            db.session.rollback()

        list.append(dict)
    driver.quit()
    db.session.close()
    return json.dumps(list)




@web.route("/constellation/list/en")
def constellationlist_en():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/IAU_designated_constellations")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find("div",attrs={"class":"mw-parser-output"})

    table = div.find("table")
    rows  = table.select("tr")
    rowcount = len(rows)
    list = []

    for i in  range(2,rowcount):
        try:
            dict = {}
            row = rows[i]
            cells = row.select("td")
            if len(cells) < 1:
                continue
            cell0  = cells[0]
            englishname = cell0.text
            index = englishname.find("/")
            dict["englishname"] = englishname[:index]


            dict["englishLink"] = ""
            try:
                a = cell0.find("a")
                dict["englishLink"] ="https://en.wikipedia.org"+ a.attrs["href"]
            except Exception as  e :
                print(e)
            shortname = cells[1].text
            dict["shortname"] = shortname.upper()

            list.append(dict)
            try:
                consterllationobject = db.session.query(Constellation).filter(Constellation.shortname == dict["shortname"])[0]
                consterllationobject.englishname = dict["englishname"]
                consterllationobject.englishLink = dict["englishLink"]
                consterllationobject.nasashortname = cells[2].text
                genetive = cells[3].text
                index1 = genetive.find("/")
                consterllationobject.genitive = genetive[:index1]
                consterllationobject.oringin_en = cells[4].text
                consterllationobject.meaning_en  =cells[5].text
                consterllationobject.brightest_en = cells[6].text

                db.session.commit()

            except Exception as  e:
                print (e)

                db.session.rollback()
        except Exception as  e:
            print(e)
            continue





    driver.quit()
    db.session.close()
    return json.dumps(list)


@web.route("/constellation/list/jp")
def constellationlist_jp():
    driver = webdriver.Chrome()
    driver.get("https://ja.wikipedia.org/wiki/%E6%98%9F%E5%BA%A7%E3%81%AE%E4%B8%80%E8%A6%A7")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find("div",attrs={"class":"mw-parser-output"})

    table = div.find("table")
    rows  = table.select("tr")
    rowcount = len(rows)
    list = []

    for i in  range(1,rowcount):
        try:
            dict = {}
            row = rows[i]
            cells = row.select("td")
            if len(cells) < 1:
                continue
            cell0  = cells[0]

            dict["japanesename"] = cell0.text


            dict["japaneseLink"] = ""
            try:
                a = cell0.find("a")
                dict["japaneseLink"] ="https://ja.wikipedia.org"+ a.attrs["href"]
            except Exception as  e :
                print(e)
            shortname = cells[1].text
            dict["shortname"] = shortname.upper()

            list.append(dict)
            try:
                consterllationobject = db.session.query(Constellation).filter(Constellation.shortname == dict["shortname"])[0]
                consterllationobject.japanesename = dict["japanesename"]
                consterllationobject.japaneseLink= dict["japaneseLink"]

                consterllationobject.oringin_jp = cells[4].text
                consterllationobject.meaning_jp  =cells[5].text
                consterllationobject.brightest_jp = cells[6].text
                db.session.commit()



            except Exception as e:
                print(e)

                db.session.rollback()
        except Exception as e:
            print(e)
            continue





    driver.quit()
    db.session.close()
    return json.dumps(list)


@web.route('/comet')
def webcomet():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_numbered_comets")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})
    table = div.find("table")
    rows = table.select("tr")
    rowcount = len(rows)
    list = []
    for i in range(1, rowcount):
        dict = {}
        row = rows[i]
        cells = row.select("td")
        if len(cells) < 1:
            continue
        cell0 = cells[0]
        dict["number"] = row.attrs["id"]
        dict["Englishname"] = cell0.text
        dict["EnglishLink"] = ""
        try:
            a = cell0.find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
        except Exception as e:
            print(e)
        dict["Discovers"]   = cells[1].text
        dict["OrbitalPeriod"]  =cells[2].text
        dict["SemeMajorAxis"] = cells[3].text
        dict["Inclination"] = cells[4].text
        dict["Ecc"] = cells[5].text
        dict["Magnitude"] = cells[6].text
        dict["Classname"] = cells[7].text
        str = cells[8].text
        if   str == "✓":
            dict["NEC"] = True
        else:
            dict["NEC"] = False
        cell9  = cells[9]
        dict["Ref"]  =""
        try:
            a9 = cell9.find("a")
            dict["Ref"] =  a9.attrs["href"]
        except Exception as  e:
            print(e)
        list.append(dict)
        cometobject = Comet(dict=dict)
        try:
            db.session.add(cometobject)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()
    driver.quit()
    return json.dumps(list)

@web.route("/comet/zh")
def cometzh():
    driver = webdriver.Chrome()
    try:
        comets = db.session.query(Comet).all()
        for comet in comets:
            try:
                driver.get(comet.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        comet.Chinesename = title
                        comet.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:
                        print(e)
                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        db.session.rollback()

    return "done"


@web.route("/comet/jp")
def cometjp():
    driver = webdriver.Chrome()
    try:
        comets = db.session.query(Comet).all()
        for comet in comets:
            try:
                driver.get(comet.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        comet.Japanesename = title
                        comet.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print (e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/globourcluster/milky")
def globoucluster():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_globular_clusters")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})
    table = div.find("table")
    list = []
    rows = table.select("tr")
    rowcount = len(rows)
    for j in range(2, rowcount):
        dict = {}

        dict["Region"] = "Milky Way"


        row = rows[j]
        cells = row.select("td")
        try:
            cell0 = cells[0]
        except:
            continue
        dict["Identifier"] = cell0.text
        dict["EnglishLink"] = ""
        try:
            a = cell0.find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
        except Exception as e:
            print(e)
        dict["RightAscension"] = cells[1].text
        dict["Declination"] = cells[2].text
        dict["Constellation"] = cells[3].text
        dict["ApparentMagnitude"] = cells[4].text
        dict["Diameter"] = cells[5].text

        try:
            globularclusterobject = GlobularClusters(dict=dict)
            db.session.add(globularclusterobject)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    driver.quit()
    db.session.close()
    return json.dumps(list)


@web.route("/globourcluster/localgroup")
def globouclusterlocalgroup():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_globular_clusters")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})
    tables = div.select("table")
    list = []
    table = tables[1]
    rows = table.select("tr")
    rowcount = len(rows)
    for j in range(2, rowcount):
        dict = {}

        dict["Region"] = "Local Group"


        row = rows[j]
        cells = row.select("td")
        try:
            cell0 = cells[0]
        except:
            continue
        dict["Identifier"] = cell0.text
        dict["EnglishLink"] = ""
        try:
            a = cell0.find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
        except Exception as e:
            print(e)
        dict["RightAscension"] = cells[1].text
        if cells[1].text == "N/A":
            continue
        dict["Declination"] = cells[2].text
        # dict["Constellation"] = cells[3].text
        dict["ApparentMagnitude"] = cells[3].text
        dict["Diameter"] = cells[4].text
        dict["Galaxy"] = cells[5].text

        try:
            globularclusterobject = GlobularClusters(dict=dict)
            db.session.add(globularclusterobject)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    driver.quit()
    db.session.close()
    return json.dumps(list)

@web.route("/opencluster")
def opencluster():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_open_clusters")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})

    list = []
    table = div.find("table")
    rows = table.select("tr")
    rowcount = len(rows)
    for j in range(3, rowcount):
        dict = {}



        row = rows[j]
        cells = row.select("td")
        try:
            cell0 = cells[0]
        except:
            continue
        dict["Identifier"] = cell0.text
        dict["EnglishLink"] = ""
        try:
            a = cell0.find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
        except Exception as  e:
            print(e)
        dict["RightAscension"] = cells[1].text
        if cells[1].text == "N/A":
            continue
        dict["Declination"] = cells[2].text
        dict["Constellation"] = cells[3].text
        dict["Distance"] = cells[4].text
        dict["Age"] = cells[5].text
        dict["Diameter"] = cells[6].text
        dict["ApparentMagnitude"] = cells[7].text
        list.append(dict)


        try:
            openclusterobject = OpenClusters(dict=dict)
            db.session.add(openclusterobject)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    driver.quit()
    db.session.close()
    return json.dumps(list)

@web.route("/galaxy")
def galaxy():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_galaxies")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})

    list = []
    table = div.find("table")
    rows = table.select("tr")
    rowcount = len(rows)
    for j in range(1, rowcount):
        dict = {}

        row = rows[j]
        cells = row.select("td")
        try:
            cell0 = cells[0]
        except:
            continue

        dict["Image"] = ""
        try:
            a = cell0.find("a")
            dict["Image"] = "https://en.wikipedia.org" + a.attrs["href"]
        except Exception as  e:
            print(e)
        cell1 = cells[1]
        dict["EnglishName"] = cell1.text[:-1]
        dict["EnglishLink"] = ""
        try:
            a1 = cell1.find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + a1.attrs["href"]
        except Exception as e:
            print(e)

        dict["Constellation"] = cells[2].text[:-1]
        dict["OriginOfName"] = cells[3].text

        list.append(dict)


        try:
            galaxyobject = Galaxy(dict=dict)
            db.session.add(galaxyobject)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    driver.quit()
    db.session.close()
    return json.dumps(list)



@web.route("/planetnebula")
def planetnebula():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_planetary_nebulae")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})

    list = []
    tables = div.select("table")
    for i in range(0,len(tables)):
        table = tables[i]
        rows = table.select("tr")
        rowcount = len(rows)
        for j in range(1, rowcount):
            dict = {}

            if i == 0:
                dict["Zone"] = "Northern Hemisphere"
            else:
                dict["Zone"] = "Southern Hemisphere"

            row = rows[j]
            cells = row.select("td")
            try:
                cell0 = cells[0]
            except:
                continue

            dict["Image"] = ""
            try:
                a = cell0.find("a")
                dict["Image"] = "https://en.wikipedia.org" + a.attrs["href"]
            except Exception as  e:
                print(e)

            cell1 = cells[1]
            dict["Name"] = cells[1].text

            dict["EnglishLink"] = ""
            try:
                a = cell1.find("a")
                dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
            except Exception as e:
                print(e)

            cell2 = cells[2]
            dict["Messier"] = cell2.text
            if len(dict["EnglishLink"]) < 1:
                try:
                    a = cell2.find("a")
                    dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
                except Exception as e:
                    print(e)

            cell3 = cells[3]
            dict["NGC"] = cell3.text
            if len(dict["EnglishLink"]) < 1:
                try:
                    a = cell3.find("a")
                    dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
                except Exception as e:
                    print(e)

            cell4 = cells[4]
            dict["Other"] = cell4.text
            if len(dict["EnglishLink"]) < 1:
                try:
                    a = cell4.find("a")
                    dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
                except Exception as e:

                    print(e)

            dict["DateDiscove"] = cells[5].text
            dict["Distance"] = cells[6].text
            dict["ApparentMagnitude"]  =cells[7].text
            dict["Constellation"] = cells[8].text


            list.append(dict)


            try:
                palnetnebulaobject = PlanetaryNebulae(Dict=dict)
                db.session.add(palnetnebulaobject)
                db.session.commit()
            except Exception as e:

                db.session.rollback()

    driver.quit()
    db.session.close()
    return json.dumps(list)

@web.route("/planetnubulae/read")
def planetnubulaeread():

    driver = webdriver.Chrome()

    try:
        diffuseobjects = db.session.query(PlanetaryNebulae).all()
        for disffuseobject in diffuseobjects:
            driver.get(disffuseobject.EnglishLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})
            table = div.find("table")
            dict = {}
            try:
                imagea = table.find("a", attrs={"class": "image"})
                img = imagea.find("img")
                dict["image"] = "https:" + img.attrs["src"]
                disffuseobject.Image = dict["image"]
            except:
                pass

            alinks = table.select("a")
            for i in range(0, len(alinks)):
                alink = alinks[i]
                title = ""
                try:
                    try:
                        title = alink.attrs["title"]
                    except:
                        pass
                    if title == "Right ascension":
                        try:
                            thra = alink.parent
                            trra = thra.parent
                            tdra = trra.find("td")
                            disffuseobject.RightAscension = tdra.text
                        except Exception as  e:
                            print(e)
                    elif title == "Declination":
                        try:
                            thdec = alink.parent
                            trdec = thdec.parent
                            tddec = trdec.find("td")
                            disffuseobject.Declination = tddec.text
                        except Exception as e:
                            print (e)

                    elif title == "Constellation":
                        try:
                            thcon = alink.parent
                            trcon = thcon.parent
                            tdcon = trcon.find("td")
                            disffuseobject.Constellation = tdcon.text
                        except Exception as  e:
                            print(e)
                    elif title == "Apparent magnitude":
                        try:
                            tham = alink.parent
                            tram = tham.parent
                            tdam = tram.find("td")
                            disffuseobject.ApparentMagnitude = tdam.text
                        except Exception as  e:
                            print(e)



                except Exception as e:
                    print(e)
            try:
                ths = table.select("th")
                for j in range(0, len(ths)):
                    th = ths[j]
                    thtilte = th.text
                    if thtilte == "Distance":
                        trdis = th.parent
                        tddis = trdis.find("td")
                        disffuseobject.Distance = tddis.text
            except Exception as  e:
                print(e)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()

            time.sleep(1)


    except Exception as e:

        db.session.rollback()







    driver.quit()
    return "done"


@web.route("/pronebula")
def pronebula():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_protoplanetary_nebulae")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})

    list = []
    tables = div.select("table")
    for i in range(0,len(tables)):
        table = tables[i]
        rows = table.select("tr")
        rowcount = len(rows)
        for j in range(1, rowcount):
            dict = {}

            row = rows[j]
            cells = row.select("td")
            try:
                cell0 = cells[0]
            except:
                continue

            dict["Image"] = ""
            try:
                a = cell0.find("a")
                dict["Image"] = "https://en.wikipedia.org" + a.attrs["href"]
            except Exception as  e:
                print(e)

            cell1 = cells[1]
            dict["Name"] = cells[1].text

            dict["EnglishLink"] = ""
            try:
                a = cell1.find("a")
                dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
            except Exception as  e:
                print(e)



            cell3 = cells[3]
            dict["Other"] = cell3.text
            if len(dict["EnglishLink"]) < 1:
                try:
                    a = cell3.find("a")
                    dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
                except Exception as  e:
                    print(e)



            dict["DateDiscove"] = cells[4].text
            dict["Distance"] = cells[5].text
            # dict["ApparentMagnitude"]  =cells[7].text
            # dict["Constellation"] = cells[8].text

            list.append(dict)


            try:
                pronebulaobject = ProtoplanetaryNebulae(Dict=dict)
                db.session.add(pronebulaobject)
                db.session.commit()
            except Exception as e:

                db.session.rollback()

    driver.quit()
    db.session.close()
    return json.dumps(list)

@web.route("/diffuse")
def disffuseebula():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_diffuse_nebulae")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "mw-parser-output"})
    div0 = div.find("div",attrs={"class":"div-col"})
    ul =div0.find("ul")
    lis = ul.select("li")
    list = []
    for i in  range(0,len(lis)):
        dict ={}
        li = lis[i]
        dict["Name"] = li.text
        dict["title"] = ""
        dict["EnglishLink"] = ""
        try:
            a = li.find("a")
            dict["EnglishLink"] = "https://en.wikipedia.org" + a.attrs["href"]
            dict["title"] = a.attrs["title"]
        except Exception as  e:
            print(e)
        list.append(dict)
        try:
            diffuseobject = DiffuseNebulae(Dict=dict)
            db.session.add(diffuseobject)
            db.session.commit()
        except Exception as  e:

            db.session.rollback()
    driver.quit()
    db.session.close()
    return json.dumps(list)



@web.route("/diffuse/read")
def diffuseread():

    driver = webdriver.Chrome()

    try:
        diffuseobjects = db.session.query(DiffuseNebulae).all()
        for disffuseobject in diffuseobjects:
            driver.get(disffuseobject.EnglishLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            try:
                div = soup.find("div", attrs={"class": "mw-parser-output"})
                table = div.find("table")
            except:
                continue
            dict = {}
            try:
                imagea = table.find("a", attrs={"class": "image"})
                img = imagea.find("img")
                dict["image"] = "https:" + img.attrs["src"]
                disffuseobject.Image = dict["image"]
            except:
                pass

            alinks = table.select("a")
            for i in range(0, len(alinks)):
                alink = alinks[i]
                title = ""
                try:
                    try:
                        title = alink.attrs["title"]
                    except:
                        pass
                    if title == "Right ascension":
                        try:
                            thra = alink.parent
                            trra = thra.parent
                            tdra = trra.find("td")
                            disffuseobject.RightAscension = tdra.text
                        except Exception as  e:
                            print(e)
                    elif title == "Declination":
                        try:
                            thdec = alink.parent
                            trdec = thdec.parent
                            tddec = trdec.find("td")
                            disffuseobject.Declination = tddec.text
                        except Exception as  e:
                            print(e)

                    elif title == "Constellation":
                        try:
                            thcon = alink.parent
                            trcon = thcon.parent
                            tdcon = trcon.find("td")
                            disffuseobject.Constellation = tdcon.text
                        except Exception as  e:
                            print (e)
                    elif title == "Apparent magnitude":
                        try:
                            tham = alink.parent
                            tram = tham.parent
                            tdam = tram.find("td")
                            disffuseobject.ApparentMagnitude = tdam.text
                        except Exception as  e:
                            print(e)



                except Exception as  e:
                    print(e)
            try:
                ths = table.select("th")
                for j in range(0, len(ths)):
                    th = ths[j]
                    thtilte = th.text
                    if thtilte == "Distance":
                        trdis = th.parent
                        tddis = trdis.find("td")
                        disffuseobject.Distance = tddis.text
            except Exception as  e:
                print(e)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            time.sleep(1)


    except Exception as e:
        print(e)
        db.session.rollback()







    driver.quit()
    return "done"



@web.route("/galaxy/read")
def galaxyread():

    driver = webdriver.Chrome()

    try:
        galaxyobjects = db.session.query(Galaxy).all()
        for galaxyeobject in galaxyobjects:
            driver.get(galaxyeobject.EnglishLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})
            table = div.find("table")
            dict = {}
            # try:
            #     imagea = table.find("a", attrs={"class": "image"})
            #     img = imagea.find("img")
            #     dict["image"] = "https:" + img.attrs["src"]
            #     disffuseobject.Image = dict["image"]
            # except:
            #     pass

            alinks = table.select("a")
            for i in range(0, len(alinks)):
                alink = alinks[i]
                title = ""
                try:
                    try:
                        title = alink.attrs["title"]
                    except:
                        pass
                    if title == "Right ascension":
                        try:
                            thra = alink.parent
                            trra = thra.parent
                            tdra = trra.find("td")
                            galaxyeobject.RightAscension = re.sub(u"\\[.*?]|\\【.*?】", "", tdra.texta)
                        except Exception as e:
                            print (e)
                    elif title == "Declination":
                        try:
                            thdec = alink.parent
                            trdec = thdec.parent
                            tddec = trdec.find("td")
                            galaxyeobject.Declination = re.sub(u"\\[.*?]|\\【.*?】", "", tddec.text)
                        except Exception as  e:
                            print (e)


                    elif title == "Apparent magnitude":
                        try:
                            tham = alink.parent
                            tram = tham.parent
                            tdam = tram.find("td")
                            galaxyeobject.ApparentMagnitude = re.sub(u"\\[.*?]|\\【.*?】", "", tdam.text)
                        except Exception as e:
                            print (e)



                except Exception as  e:
                    print(e)
            try:
                ths = table.select("th")
                for j in range(0, len(ths)):
                    th = ths[j]
                    thtilte = th.text
                    if thtilte == "Distance":
                        trdis = th.parent
                        tddis = trdis.find("td")
                        galaxyeobject.Distance = re.sub(u"\\[.*?]|\\【.*?】", "", tddis.text)
            except Exception as  e:
                print (e)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()

            time.sleep(1)


    except Exception as e:

        db.session.rollback()


    driver.quit()
    return "done"






@web.route("/messier/zh")
def messierzh():
    driver = webdriver.Chrome()
    try:
        messiers = db.session.query(Messier).all()
        for messierobject in messiers:
            try:
                driver.get(messierobject.englishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]


                        messierobject.chineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/messier/jp")
def messierjp():
    driver = webdriver.Chrome()
    try:
        messiers = db.session.query(Messier).all()
        for messierobject in messiers:
            try:
                driver.get(messierobject.englishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]


                        messierobject.japaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/galaxy/zh")
def galaxyzh():
    driver = webdriver.Chrome()
    try:
        galaxys = db.session.query(Galaxy).all()
        for galaxyobject in galaxys:
            try:
                driver.get(galaxyobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        galaxyobject.ChineseName = title
                        galaxyobject.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/galaxy/jp")
def galaxyjp():
    driver = webdriver.Chrome()
    try:
        galaxys = db.session.query(Galaxy).all()
        for galaxyobject in galaxys:
            try:
                driver.get(galaxyobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        galaxyobject.JapaneseName  = title
                        galaxyobject.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/golobular/zh")
def golobularzh():
    driver = webdriver.Chrome()
    try:
        golobulars = db.session.query(GlobularClusters).all()
        for golobularobject in golobulars:
            try:
                if len(golobularobject.EnglishLink) < 3:
                    continue
                driver.get(golobularobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        golobularobject.ChineseName = title
                        golobularobject.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/golobular/jp")
def golobularjp():
    driver = webdriver.Chrome()
    try:
        golobulars = db.session.query(GlobularClusters).all()
        for golobularobject in golobulars:
            try:
                if len(golobularobject.EnglishLink) < 3:
                    continue
                driver.get(golobularobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        golobularobject.JapaneseName  = title
                        golobularobject.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
               print(e)
    except Exception as e:
        print(e)
        db.session.rollback()

    return "done"


@web.route("/opencluster/zh")
def openclusterzh():
    driver = webdriver.Chrome()
    try:
        openclusters = db.session.query(OpenClusters).all()
        for openclusterobject in openclusters:
            try:
                if len(openclusterobject.EnglishLink) < 3:
                    continue
                driver.get(openclusterobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        openclusterobject.ChineseName = title
                        openclusterobject.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:
                        print(e)
                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        db.session.rollback()

    return "done"


@web.route("/opencluster/jp")
def openclusterjp():
    driver = webdriver.Chrome()
    try:
        openclusters = db.session.query(OpenClusters).all()
        for openclusterobject in openclusters:
            try:
                if len(openclusterobject.EnglishLink) < 3:
                    continue
                driver.get(openclusterobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        openclusterobject.JapaneseName  = title
                        openclusterobject.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:
                        print(e)
                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        db.session.rollback()

    return "done"


@web.route("/diffuse/zh")
def diffusezh():
    driver = webdriver.Chrome()
    try:
        diffuses = db.session.query(DiffuseNebulae).all()
        for diffuseobject in diffuses:
            try:
                if len(diffuseobject.EnglishLink) < 3:
                    continue
                driver.get(diffuseobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        diffuseobject.ChineseName = title
                        diffuseobject.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:
                        print(e)
                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e :
        print(e)
        db.session.rollback()

    return "done"


@web.route("/diffuse/jp")
def diffusejp():
    driver = webdriver.Chrome()
    try:
        diffuses = db.session.query(DiffuseNebulae).all()
        for diffuseobject in diffuses:
            try:
                if len(diffuseobject.EnglishLink) < 3:
                    continue
                driver.get(diffuseobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        diffuseobject.JapaneseName  = title
                        diffuseobject.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:
                        print(e)
                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        db.session.rollback()

    return "done"



@web.route("/planetary/zh")
def planetaryzh():
    driver = webdriver.Chrome()
    try:
        planetarys = db.session.query(PlanetaryNebulae).all()
        for planetaryobject in planetarys:
            try:
                if len(planetaryobject.EnglishLink) < 3:
                    continue
                driver.get(planetaryobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        planetaryobject.ChineseName = title
                        planetaryobject.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/planetary/jp")
def planetaryjp():
    driver = webdriver.Chrome()
    try:
        planetarys = db.session.query(PlanetaryNebulae).all()
        for planetaryobject in planetarys:
            try:
                if len(planetaryobject.EnglishLink) < 3:
                    continue
                driver.get(planetaryobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        planetaryobject.JapaneseName  = title
                        planetaryobject.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/protoplanetary/zh")
def protoplanetaryzh():
    driver = webdriver.Chrome()
    try:
        protoplanetarys = db.session.query(ProtoplanetaryNebulae).all()
        for protoplanetaryobject in protoplanetarys:
            try:
                if len(protoplanetaryobject.EnglishLink) < 3:
                    continue
                driver.get(protoplanetaryobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-zh"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Chinese")
                        if index > -1:
                            title =title[:index]

                        protoplanetaryobject.ChineseName = title
                        protoplanetaryobject.ChineseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"


@web.route("/protoplanetary/jp")
def protoplanetaryjp():
    driver = webdriver.Chrome()
    try:
        protoplanetarys = db.session.query(ProtoplanetaryNebulae).all()
        for protoplanetaryobject in protoplanetarys:
            try:
                if len(protoplanetaryobject.EnglishLink) < 3:
                    continue
                driver.get(protoplanetaryobject.EnglishLink)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div = soup.find("div", attrs={"id": "mw-panel"})
                div1 = div.find("div", attrs={"id": "p-lang"})
                div2 = div1.find("div", attrs={"class": "body"})
                ul = div2.find("ul")
                li = ul.find("li", attrs={"class": "interwiki-ja"})

                dict = {}


                try:
                        a = li.find("a")
                        title = a.attrs["title"]
                        index = title.find("– Japanese")
                        if index > -1:
                            title =title[:index]

                        protoplanetaryobject.JapaneseName  = title
                        protoplanetaryobject.JapaneseLink = a.attrs["href"]
                        db.session.commit()
                except Exception as e:

                        db.session.rollback()

                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:

        db.session.rollback()

    return "done"




@web.route("/protoplanetary/read")
def protoplanetaryread():

    driver = webdriver.Chrome()

    try:
        protoplanetarys = db.session.query(ProtoplanetaryNebulae).all()
        for protoplanetaryobject in protoplanetarys:
            if len(protoplanetaryobject.EnglishLink) <1:
                continue
            driver.get(protoplanetaryobject.EnglishLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            # div = soup.find("div", attrs={"class": "mw-parser-output"})
            # table = div.find("table")
            # dict = {}


            try:
                div = soup.find("div", attrs={"class": "mw-parser-output"})
                table = div.find("table")
            except:
                continue
            dict = {}
            try:
                imagea = table.find("a", attrs={"class": "image"})
                img = imagea.find("img")
                dict["image"] = "https:" + img.attrs["src"]
                protoplanetaryobject.Image = dict["image"]
            except:
                pass



            alinks = table.select("a")
            for i in range(0, len(alinks)):
                alink = alinks[i]
                title = ""
                try:
                    try:
                        title = alink.attrs["title"]
                    except:
                        pass
                    if title == "Right ascension":
                        try:
                            thra = alink.parent
                            trra = thra.parent
                            tdra = trra.find("td")
                            protoplanetaryobject.RightAscension = tdra.text
                        except Exception as e:
                            print (e)
                    elif title == "Declination":
                        try:
                            thdec = alink.parent
                            trdec = thdec.parent
                            tddec = trdec.find("td")
                            protoplanetaryobject.Declination = tddec.text
                        except Exception as e:
                            print (e)

                    elif title == "Constellation":
                        try:
                            thcon = alink.parent
                            trcon = thcon.parent
                            tdcon = trcon.find("td")
                            protoplanetaryobject.Constellation = tdcon.text
                        except Exception as  e:
                            print(e)
                    elif title == "Apparent magnitude":
                        try:
                            tham = alink.parent
                            tram = tham.parent
                            tdam = tram.find("td")
                            protoplanetaryobject.ApparentMagnitude = tdam.text
                        except Exception as  e:
                            print (e)



                except Exception as  e:
                    print(e)
            try:
                ths = table.select("th")
                for j in range(0, len(ths)):
                    th = ths[j]
                    thtilte = th.text
                    if thtilte == "Distance":
                        trdis = th.parent
                        tddis = trdis.find("td")
                        protoplanetaryobject.Distance = tddis.text
            except Exception as  e:
                print(e)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            time.sleep(1)


    except Exception as e:
        print(e)
        db.session.rollback()

    driver.quit()
    return "done"


@web.route("/opencluster/read")
def openclusterread():

    driver = webdriver.Chrome()

    try:
        protoplanetarys = db.session.query(OpenClusters).all()
        for protoplanetaryobject in protoplanetarys:
            if len(protoplanetaryobject.EnglishLink) <1:
                continue
            driver.get(protoplanetaryobject.EnglishLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            # div = soup.find("div", attrs={"class": "mw-parser-output"})
            # table = div.find("table")
            # dict = {}


            try:
                div = soup.find("div", attrs={"class": "mw-parser-output"})
                table = div.find("table")
            except:
                continue
            dict = {}
            try:
                imagea = table.find("a", attrs={"class": "image"})
                img = imagea.find("img")
                dict["image"] = "https:" + img.attrs["src"]
                protoplanetaryobject.Image = dict["image"]
            except:
                pass





            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            time.sleep(1)


    except Exception as e:
        print(e)
        db.session.rollback()

    driver.quit()
    return "done"



@web.route("/golubular/read")
def golubularread():

    driver = webdriver.Chrome()

    try:
        protoplanetarys = db.session.query(GlobularClusters).all()
        for protoplanetaryobject in protoplanetarys:
            if len(protoplanetaryobject.EnglishLink) <1:
                continue
            driver.get(protoplanetaryobject.EnglishLink)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            # div = soup.find("div", attrs={"class": "mw-parser-output"})
            # table = div.find("table")
            # dict = {}


            try:
                div = soup.find("div", attrs={"class": "mw-parser-output"})
                table = div.find("table")
            except:
                continue
            dict = {}
            try:
                imagea = table.find("a", attrs={"class": "image"})
                img = imagea.find("img")
                dict["image"] = "https:" + img.attrs["src"]
                protoplanetaryobject.Image = dict["image"]
            except:
                pass



            alinks = table.select("a")
            for i in range(0, len(alinks)):
                alink = alinks[i]
                title = ""
                try:
                    try:
                        title = alink.attrs["title"]
                    except:
                        pass


                    if title == "Constellation":
                        try:
                            thcon = alink.parent
                            trcon = thcon.parent
                            tdcon = trcon.find("td")
                            protoplanetaryobject.Constellation = tdcon.text
                        except Exception as e:
                            print(e)



                except Exception as  e:
                    print(e)
            try:
                ths = table.select("th")
                for j in range(0, len(ths)):
                    th = ths[j]
                    thtilte = th.text
                    if thtilte == "Distance":
                        trdis = th.parent
                        tddis = trdis.find("td")
                        protoplanetaryobject.Distance = tddis.text
            except Exception as  e:
                print(e)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            time.sleep(1)


    except Exception as e:
        print(e)
        db.session.rollback()

    driver.quit()
    return "done"


@web.route("/deepsky/detail")
def deepskydetail():
    try:
        messiers = db.session.query(Messier).all()
        for messierobject in messiers:

            deepskydetailobject = DeepskyDetail(Identifier=messierobject.number)
            deepskydetailobject.EnglishLink = messierobject.englishLink
            deepskydetailobject.ChineseLink = messierobject.chineseLink
            deepskydetailobject.JapaneseLink = messierobject.japaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()

    try:
        galaxys = db.session.query(Galaxy).all()
        for galaxyobject in galaxys:
            identifier = "G"+str(galaxyobject.Id)

            deepskydetailobject = DeepskyDetail(Identifier=identifier)
            deepskydetailobject.EnglishLink = galaxyobject.EnglishLink
            deepskydetailobject.ChineseLink = galaxyobject.ChineseLink
            deepskydetailobject.JapaneseLink = galaxyobject.JapaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()

    try:
        galaxys = db.session.query(GlobularClusters).all()
        for galaxyobject in galaxys:
            identifier = "GC"+str(galaxyobject.Id)

            deepskydetailobject = DeepskyDetail(Identifier=identifier)
            deepskydetailobject.EnglishLink = galaxyobject.EnglishLink
            deepskydetailobject.ChineseLink = galaxyobject.ChineseLink
            deepskydetailobject.JapaneseLink = galaxyobject.JapaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()

    try:
        galaxys = db.session.query(OpenClusters).all()
        for galaxyobject in galaxys:
            identifier = "OC"+str(galaxyobject.Id)

            deepskydetailobject = DeepskyDetail(Identifier=identifier)
            deepskydetailobject.EnglishLink = galaxyobject.EnglishLink
            deepskydetailobject.ChineseLink = galaxyobject.ChineseLink
            deepskydetailobject.JapaneseLink = galaxyobject.JapaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()


    try:
        galaxys = db.session.query(DiffuseNebulae).all()
        for galaxyobject in galaxys:
            identifier = "DN"+str(galaxyobject.Id)

            deepskydetailobject = DeepskyDetail(Identifier=identifier)
            deepskydetailobject.EnglishLink = galaxyobject.EnglishLink
            deepskydetailobject.ChineseLink = galaxyobject.ChineseLink
            deepskydetailobject.JapaneseLink = galaxyobject.JapaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()

    try:
        galaxys = db.session.query(PlanetaryNebulae).all()
        for galaxyobject in galaxys:
            identifier = "PN"+str(galaxyobject.Id)

            deepskydetailobject = DeepskyDetail(Identifier=identifier)
            deepskydetailobject.EnglishLink = galaxyobject.EnglishLink
            deepskydetailobject.ChineseLink = galaxyobject.ChineseLink
            deepskydetailobject.JapaneseLink = galaxyobject.JapaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()

    try:
        galaxys = db.session.query(ProtoplanetaryNebulae).all()
        for galaxyobject in galaxys:
            identifier = "PRN"+str(galaxyobject.Id)

            deepskydetailobject = DeepskyDetail(Identifier=identifier)
            deepskydetailobject.EnglishLink = galaxyobject.EnglishLink
            deepskydetailobject.ChineseLink = galaxyobject.ChineseLink
            deepskydetailobject.JapaneseLink = galaxyobject.JapaneseLink
            try:
                db.session.add(deepskydetailobject)
                db.session.commit()
            except:
                db.session.rollback()
    except:
        db.session.rollback()

    return "done"

@web.route("/deepsky/cadlwell")
def deepskycaldwell():
    driver = webdriver.Chrome()
    try:
        galaxys = db.session.query(Caldwell).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            deepskydetailobject = DeepskyDetail(Identifier=galaxyobject.number)
            deepskydetailobject.EnglishLink =  link
            deepskydetailobject.JapaneseLink = ""
            deepskydetailobject.ChineseLink = ""

            dict["link"] = ""


            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #
                    # except Exception,e:
                    #     db.session.rollback()

                    for li in lis:
                        a = li.find("a")
                        lang = a.attrs["lang"]

                        if lang == "ja":


                            href = a.attrs["href"]
                            if href is not None:
                                if len(href) > 2:
                                    deepskydetailobject.JapaneseLink = href
                        elif lang  == "zh":
                            href = a.attrs["href"]
                            if href is not None:
                                if len(href) > 2:
                                    deepskydetailobject.ChineseLink = href

                    try:
                        db.session.add(deepskydetailobject)
                        db.session.commit()
                    except Exception as e:

                        db.session.rollback()









                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as e:
        print (e)


    finally:
        db.session.close()

    driver.quit()


    return "done"





@web.route("/deepsky/detail/en")
def deeskydetailstring_en():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(DeepskyDetail).all()
        for starobjcet in stars:
            link = starobjcet.EnglishLink
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                if header.find("p") > 0:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("h2") > 0:
                    textsting = i.text
                    if textsting.find("eferences") > 0:
                        break
                    elif textsting.find("also") > 0:
                        pass
                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"

            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)

            # break

            b = a.encode()

            # break


            try:

                starobjcet.EnglishHTML = b




                db.session.commit()
            except Exception as e:
                db.session.rollback()



            # break
            time.sleep(0.5)






    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"


@web.route("/deepsky/detail/jp")
def deepskydetailstring_jp():


    driver = webdriver.Chrome()


    try:
        constellations = db.session.query(DeepskyDetail).all()
        for constellationobject in constellations:
        # for i in range(0,1):

            link = constellationobject.JapaneseLink
            # link = "https://zh.wikipedia.org/wiki/%E4%BB%99%E5%A5%B3%E5%BA%A7"
            if  len(link) < 5:
                continue
            try:
                driver.get(link)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div0 = soup.find("div",attrs={"class":"mw-content-ltr"})
                div = div0.find("div", attrs={"class": "mw-parser-output"})
                if div is None:
                    continue
            except Exception as e:

                continue

            # print div



            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                # print header
                if header.find("<ul") > -1:
                    strings = strings + "<ul>"
                    for j in i.contents:
                        headerj = str(j)[:3]
                        if headerj.find("<li")>-1:
                            strings = strings + "<li>" + j.text + "</li>"
                    strings  = strings +"</ul>"
                elif header.find("<p")>-1:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("<h2") > -1:
                    textsting = i.text
                    if textsting.find("出典") > -1:
                        break
                    elif textsting.find("脚注") > -1:
                        break
                    elif textsting.find("外部リンク")   >-1:
                        break
                    elif textsting.find("関連項目") > -1:
                        break
                    elif textsting.find("注釈") >-1:
                        break

                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"




            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


            # return a

            # break

            b = a.encode()


            try:
                constellationobject.JapaneseHTML = b
                db.session.commit()
            except Exception as e:


                db.session.rollback()

                continue

            # break
            time.sleep(0.7)






    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"




@web.route("/deepsky/detail/zh")
def deepskydetailstring_zh():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(DeepskyDetail).all()

        n = 0
        for starobjcet in stars:
        # for i in range(0,1):
            n = n +1

            try:
                link = starobjcet.ChineseLink
                # link = "https://zh.m.wikipedia.org/wiki/%E5%A4%A9%E7%8B%BC%E6%98%9F"
                if  len(link) < 5:
                    continue
                html = starobjcet.ChineseHTML
                if html is None:

                    pass
                else:
                    continue

                driver.get(link)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div0 = soup.find("div", attrs={"id": "mw-content-text"})

                div = div0.find("div", attrs={"class": "mw-parser-output"})

                # print div

                if div is None:
                    continue

                strings = ""
                for i in div.contents:
                    header = str(i)[:3]
                    # print header

                    if header.find("<p")>-1:
                                strings = strings + "<p>" + i.text + "</p>"
                    elif header.find("h2") > 0:
                        textsting = i.text
                        if textsting.find("参考资料") > -1:
                            break
                        elif textsting.find("参考文献") > -1:
                            break
                        elif textsting.find("参见") > -1:
                            break
                        elif textsting.find("外部链接") > -1:
                            break
                        elif textsting.find("图片集") > -1:
                            pass
                        elif textsting.find("图集") > -1:
                            pass
                        elif textsting.find("相关条目") >-1:
                            pass
                        elif textsting.find("引文") >-1:
                            pass
                        elif textsting.find("外链") >-1:
                            pass
                        elif textsting.find("资料来源")>-1:
                            pass
                        elif textsting.find("幻想作品")>-1:
                            pass
                        elif textsting.find("注释")>-1:
                            pass
                        elif textsting.find("来源")>-1:
                            pass
                        elif textsting.find("恒星列表")>-1:
                            pass
                        elif textsting.find("注解")>-1:
                            pass
                        else:
                            strings = strings + "<h2>" + i.text.replace("编辑","") + "</h2>"


                    elif header.find("h3") > 0:
                        strings = strings + "<h3>" + i.text + "</h3>"




                a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


                # return strings

                # break

                b = a.encode()


                try:

                        starobjcet.ChineseHTML = b

                        db.session.commit()
                except Exception as e:


                    db.session.rollback()

                    continue

                # break

                time.sleep(0.7)

            except Exception as e:
                print(e)


    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"




@web.route("/comet/detail/en")
def cometdetailstring_en():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(CometDetail).all()
        for starobjcet in stars:
            link = starobjcet.EnglishLink
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find("div", attrs={"class": "mw-parser-output"})

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                if header.find("p") > 0:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("h2") > 0:
                    textsting = i.text
                    if textsting.find("eferences") > 0:
                        break
                    elif textsting.find("also") > 0:
                        pass
                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"

            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)

            b = a.encode()

            # break


            try:

                starobjcet.EnglishHTML = b

                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

            time.sleep(0.5)


    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    driver.quit()
    return  "done"


@web.route("/comet/detail/jp")
def cometdetailstring_jp():


    driver = webdriver.Chrome()


    try:
        constellations = db.session.query(CometDetail).all()
        for constellationobject in constellations:
        # for i in range(0,1):
            link = constellationobject.JapaneseLink
            # link = "https://zh.wikipedia.org/wiki/%E4%BB%99%E5%A5%B3%E5%BA%A7"
            if  len(link) < 5:
                continue
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            try:
                div0 = soup.find("div",attrs={"class":"mw-content-ltr"})
                div = div0.find("div", attrs={"class": "mw-parser-output"})
            except:
                continue

            # print div

            if div is None:
                continue

            strings = ""
            for i in div.contents:
                header = str(i)[:3]
                # print header
                if header.find("<ul") > -1:
                    strings = strings + "<ul>"
                    for j in i.contents:
                        headerj = str(j)[:3]
                        if headerj.find("<li")>-1:
                            strings = strings + "<li>" + j.text + "</li>"
                    strings  = strings +"</ul>"
                elif header.find("<p")>-1:
                    strings = strings + "<p>" + i.text + "</p>"
                elif header.find("<h2") > -1:
                    textsting = i.text
                    if textsting.find("出典") > -1:
                        break
                    elif textsting.find("脚注") > -1:
                        break
                    elif textsting.find("外部リンク")   >-1:
                        break
                    elif textsting.find("関連項目") > -1:
                        break
                    elif textsting.find("注釈") >-1:
                        break

                    else:
                        strings = strings + "<h2>" + i.text + "</h2>"


                elif header.find("h3") > 0:
                    strings = strings + "<h3>" + i.text + "</h3>"

            a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)




            b = a.encode()


            try:
                constellationobject.JapaneseHTML = b
                db.session.commit()
            except Exception as e:


                db.session.rollback()

                continue

            # break
            time.sleep(0.7)


    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"




@web.route("/comet/detail/zh")
def cometdetailstring_zh():


    driver = webdriver.Chrome()


    try:
        stars = db.session.query(CometDetail).all()

        n = 0
        for starobjcet in stars:
        # for i in range(0,1):
            n = n +1

            try:
                link = starobjcet.ChineseLink
                # link = "https://zh.m.wikipedia.org/wiki/%E5%A4%A9%E7%8B%BC%E6%98%9F"
                if  len(link) < 5:
                    continue

                driver.get(link)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                div0 = soup.find("div", attrs={"id": "mw-content-text"})

                div = div0.find("div", attrs={"class": "mw-parser-output"})

                # print div

                if div is None:
                    continue

                strings = ""
                for i in div.contents:
                    header = str(i)[:3]
                    # print header

                    if header.find("<p")>-1:
                                strings = strings + "<p>" + i.text + "</p>"
                    elif header.find("h2") > 0:
                        textsting = i.text
                        if textsting.find("参考资料") > -1:
                            break
                        elif textsting.find("参考文献") > -1:
                            break
                        elif textsting.find("参见") > -1:
                            break
                        elif textsting.find("外部链接") > -1:
                            break
                        elif textsting.find("图片集") > -1:
                            pass
                        elif textsting.find("图集") > -1:
                            pass
                        elif textsting.find("相关条目") >-1:
                            pass
                        elif textsting.find("引文") >-1:
                            pass
                        elif textsting.find("外链") >-1:
                            pass
                        elif textsting.find("资料来源")>-1:
                            pass
                        elif textsting.find("幻想作品")>-1:
                            pass
                        elif textsting.find("注释")>-1:
                            pass
                        elif textsting.find("来源")>-1:
                            pass
                        elif textsting.find("恒星列表")>-1:
                            pass
                        elif textsting.find("注解")>-1:
                            pass
                        else:
                            strings = strings + "<h2>" + i.text.replace("编辑","") + "</h2>"


                    elif header.find("h3") > 0:
                        strings = strings + "<h3>" + i.text + "</h3>"




                a = re.sub(u"\\[.*?]|\\【.*?】", "", strings)


                # return strings

                # break

                b = a.encode()


                try:

                        starobjcet.ChineseHTML = b

                        db.session.commit()
                except Exception as e:


                    db.session.rollback()

                    continue

                # break

                time.sleep(0.7)

            except Exception as e:
                print(e)






    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()


    driver.quit()
    return  "done"



@web.route("/event/jd/delete")
def eventdeletejp():

    try:
        events  =db.session.query(AstroEvent).filter(AstroEvent.timezone == "9.5",AstroEvent.year == "2022").all()
        for event in events:
            try:
                db.session.delete(event)
                db.session.commit()

            except Exception as e:
                print(e)
                db.session.rollback()
    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    return "done"


@web.route("/event/jp/<month>")
def evnetjpmonth(month):
    year = "2023"
    driver = webdriver.Chrome()
    link = "https://www.astroarts.co.jp/phenomena/2023/"+month+"/index-j.shtml"
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div0 = soup.find("div",attrs={"class":"container"})
    section = div0.find("section",attrs ={"class":"section"})
    table = section.find("table")
    tbody =table.find("tbody")
    trs = tbody.select("tr")
    count = len(trs)
    for i  in  range(0,count):
        tr = trs[i]
        td0 = tr.find("td")
        try:
            a = td0.find("a")
            day = a.text
        except:
            try:
                day = a.text
            except:
                day = "0"
        tdps = tr.find("td",attrs={"class":"phenomena"})
        lis = tdps.select("li")
        licount = len(lis)
        for j in range(0,licount):
            li = lis[j]
            event = li.text
            time = str(j)
            recordindex = int(month)*30*10+ int(day)*10 +int(time)
            try:
                astroevent = AstroEvent(year=year,month=month,day=day,time=time,Event=event,RecodIndex=recordindex)
                db.session.add(astroevent)
                db.session.commit()

            except Exception as e:

                db.session.rollback()

    driver.quit()
    db.session.close()
    return "done"


@web.route("/surf/jp/location")
def surfjplocation():
    uploadpath = os.path.join(basedir, 'static/uploads')
    driver = webdriver.Chrome()
    link = "http://www.surf-reps.com/point.html"
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div0 = soup.find("div",attrs={"id":"container2"})
    section = div0.find("div",attrs ={"id":"blkMain"})
    table = section.find("table")
    tbody =table.find("tbody")
    trs = tbody.select("tr")
    list = []
    for tr in trs:
        a = tr.find("a")
        if a is not None:
            href = a.attrs["href"]
            list.append(href)
    resultlist = []
    for url in list:
        fullurl = "http://www.surf-reps.com/" +url
        try:
            driver.get(fullurl)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div0 = soup.find("div", attrs={"id": "container2"})
            section = div0.find("div", attrs={"id": "blkMain"})
            table = section.find("table")
            tbody = table.find("tbody")
            trs = tbody.select("tr")
            for tr in trs:
                stable  = tr.find("table")
                if stable is not None:
                    stbody = stable.find("tbody")
                    strs = stbody.select("tr")
                    for str in strs:
                        stds = str.select("td")
                        if len(stds) > 5:
                            dict = {}
                            dict["name"] = stds[0].text
                            dict["direction"] = stds[1].text
                            dict["terrian"] = stds[2].text
                            dict["adapt"] = stds[3].text
                            a = stds[5].find("a")
                            if a is not None:
                                dict["location"] = a.attrs["href"]
                            resultlist.append(dict)

        except Exception as e:
            print(e)









    driver.quit()
    filepath = os.path.join(uploadpath,"surfjapan.json")
    f = open(filepath,"w")
    f.write(json.dumps(resultlist))
    f.close()
    return json.dumps(list)

@web.route("/surf/jp/json")
def surfjpjson():

    uploadpath = os.path.join(basedir, 'static/uploads')
    filepath = os.path.join(uploadpath,"surfjapan.json")
    f = open(filepath,"r")
    j = f.read()
    f.close()
    result = json.loads(j)
    resultlist = []
    for dict in result:
        if "location" in dict:
            url = dict["location"]
            paras = url.split("&")
            for para in paras:
                if para.find("ll=") > -1:
                    latlong= para[3:]
                    latlongs = latlong.split(",")
                    ndict = {}
                    ndict["lat"] = latlongs[0]
                    ndict["lng"] = latlongs[1]
                    ndict["name"] = dict["name"]
                    ndict["direction"] = dict["direction"]
                    ndict["terrian"] = dict["terrian"]
                    ndict["adapt"] = dict["adapt"]
                    resultlist.append(ndict)
    nfilepath = os.path.join(uploadpath,"surfjapann.json")
    nf = open(nfilepath,"w")
    nf.write(json.dumps(resultlist))
    nf.close()


    return json.dumps(resultlist)


@web.route("/surf/tw/json")
def surftwjson():
    driver = webdriver.Chrome()
    uploadpath = os.path.join(basedir, 'static/uploads')
    filepath = os.path.join(uploadpath,"surfchina.json")
    f = open(filepath,"r")
    jf = f.read()
    flist = json.loads(jf)
    rfilepath = os.path.join(uploadpath, "surftw.json")
    rf = open(rfilepath,"r")
    return rf.read()
    resultlist = []
    for dict in flist:
        timezone = dict["timezone"]
        if timezone.find("Asia/Taipei")> -1:
            url = dict["magicsea_guide"]
            if url.find("https:")> -1:
                try:
                    driver.get(url)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    div0 = soup.find("div", attrs={"class": "surf-spot-characteristics-tablet"})
                    divs = div0.select("div")
                    for div in divs:
                        ps = div.select("p")
                        key = ps[0].text.strip()
                        value = ps[1].text.strip()
                        dict[key] = value
                    resultlist.append(dict)

                except Exception as e:
                    print(e)
    driver.quit()

    rf = open(rfilepath,"w")
    rf.write(json.dumps(resultlist))
    rf.close()
    return "done"


@web.route("/surf/wanna/json")
def surfwannajson():
    acuuappkey = 'W6P5PdRwzo1PL0lhEgH6aW2KN4rKxao2'
    uploadpath = os.path.join(basedir, 'static/uploads')
    filepath = os.path.join(uploadpath, "surf2.json")
    f = open(filepath,"r")
    jf = f.read()
    list = json.loads(jf)
    resultlist = []
    for dict in list:
        lat = str(dict["lat"])
        lng = str(dict['lng'])

        url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?q=' + lat + ',' + lng + '&apikey=' + acuuappkey + '&language=en'

        try:

            response = requests.get(url)
            content = response.text
            result = json.loads(content)
            timezone = result["TimeZone"]

            if timezone is not None:
                if "Name" in timezone:
                    dict["timezone"] = timezone["Name"]
        except Exception as e:
            print(e)



    wf = open(filepath,"w")
    wf.write(json.dumps(list))
    wf.close()
    return "done"


































