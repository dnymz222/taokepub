#coding=utf8
from . import web
from flask import Flask,redirect,render_template,request,url_for,session,escape
import xlrd
import os
import json

from app import db


from selenium import webdriver
from bs4 import BeautifulSoup
import time


from app.Star import Star

from app.Messier import Messier
from app.Constellation import Constellation

from app.Caldwell import Caldwell
import re

from app.Galaxy import Galaxy
from app.GlobularClusters import GlobularClusters
from app.OpenClusters import OpenClusters
from app.ProtoplanetaryNebulae import ProtoplanetaryNebulae
from app.PlanetaryNebulae import PlanetaryNebulae
from app.DiffuseNebulae import DiffuseNebulae

from app.HRStar import HRStar

from config import basedir










@web.route("/star/json")
def starlistjson():
    list =[]
    try:
        stars = db.session.query(Star).all()
        for starobjcet in stars:
            englishname = starobjcet.EnglishName
            if len(englishname)< 1:

                HD = starobjcet.HDId
                if len(HD)>0:
                    starobjcet.EnglishName = "HD "+HD
                else:
                    HIP =  starobjcet.HIPId
                    if len(HIP) > 0:
                        starobjcet.EnglishName = "HIP " + HIP
                try:

                    db.session.commit()
                except Exception as e:

                    db.session.rollback()

            if(len(starobjcet.EnglishName))>1:

                dict = starobjcet.stardict()
                list.append(dict)
            else:
                pass

    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    jsonstring =  json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'star.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return "done"


@web.route("/star/main/json")
def starlmainistjson():
    list =[]
    try:
        stars = db.session.query(Star).filter(Star.Magnitude < 2.21).all()
        for starobjcet in stars:
            englishname = starobjcet.EnglishName
            if len(englishname)< 1:

                HD = starobjcet.HDId
                if len(HD)>0:
                    starobjcet.EnglishName = "HD "+HD
                else:
                    HIP =  starobjcet.HIPId
                    if len(HIP) > 0:
                        starobjcet.EnglishName = "HIP " + HIP
                try:

                    db.session.commit()
                except Exception as e:

                    db.session.rollback()

            if(len(starobjcet.EnglishName))>1:

                dict = starobjcet.stardict()
                list.append(dict)
            else:
                pass

    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    jsonstring =  json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'lsstar.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return "done"

@web.route("/constellation/json")
def constellationjson():
    list =[]
    try:
        stars = db.session.query(Constellation).all()
        for starobjcet in stars:
            dict = starobjcet.constellationDict()
            list.append(dict)

    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    jsonstring = json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'constellation.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return "done"

@web.route("/messier/json")
def messierjson():
    list =[]
    try:
        stars = db.session.query(Messier).all()
        for starobjcet in stars:
            dict = starobjcet.messierdict()
            list.append(dict)

    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    jsonstring = json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'messier.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return "done"


@web.route("/caldwell/json")
def caldwelljson():
    list =[]
    try:
        stars = db.session.query(Caldwell).all()
        for starobjcet in stars:
            dict = starobjcet.caldwellDict()
            list.append(dict)

    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    jsonstring = json.dumps(list)
    json_path = os.path.join(basedir, 'static/uploads', 'caldwell.json')
    f = open(json_path, 'w')
    f.write(jsonstring)
    f.close()

    return "done"










@web.route("/constellation/translate")
def constellationtranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "constellation_lishu_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        constellations = db.session.query(Constellation).all()

        efilename = "constellation_lishu_" + "en" + ".txt"

        etxt_path = os.path.join(basedir, 'static/uploads', efilename)
        ef = open(etxt_path, 'w')

        for constellationobject in constellations:
            link = constellationobject.englishLink
            dict = {}
            dict["englishname"] = constellationobject.englishname
            dict["name"] = constellationobject.englishname
            dict["link"] = ""


            estr1 = "\"" + constellationobject.englishname + "\"=\"" + dict["name"] + "\";"
            ef.write(estr1)
            ef.write("\n")

            # continue


            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + constellationobject.englishname + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + constellationobject.englishname + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    # f.write(str2)
                    # f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = constellationobject.englishname
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + constellationobject.englishname + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + constellationobject.englishname + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        # f.write(str2)
                        # f.write("\n")





                except Exception as e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"



@web.route("/star/translate")
def startranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "star_lishu_"+ str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        # stars = db.session.query(star).all()

        stars = db.session.query(Star).filter(Star.Magnitude < 2.21).all()

        efilename = "star_lishu_" + "en" + ".txt"

        etxt_path = os.path.join(basedir, 'static/uploads', efilename)
        ef = open(etxt_path, 'w')



        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            dict["englishname"] = starobject.EnglishName
            dict["name"] = starobject.EnglishName
            dict["link"] = ""
            estr1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
            ef.write(estr1)
            ef.write("\n")
            continue




            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    # f.write(str2)
                    # f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = starobject.EnglishName
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        # f.write(str2)
                        # f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"

@web.route("/star/translate/en")
def startranslateen():




    filename =  "en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(Star).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            dict["englishname"] = starobject.EnglishName
            dict["name"] = starobject.EnglishName
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return "done"

@web.route("/star/translate/read/<lan>")
def startranslateRead(lan):
    filename = lan + ".txt"


    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'r')
    for line in f.readlines():
        str = line.strip('\n')  # 去掉列表中每一个元素的换行符
        n= str.count('"')  # 计算substr在S中出现的次数
        if n > 4:
            print(str)


    return "done"

@web.route("/star/translate/lan/<lan>")
def startranslate(lan):
    driver = webdriver.Chrome()
    result = []


    filename =  lan +".txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(Star).all()



        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            dict["englishname"] = starobject.EnglishName
            dict["name"] = starobject.EnglishName
            dict["link"] = ""
            if len(link) < 5:
                str1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
                str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"]  + "\";"
                f.write(str1)
                f.write("\n")
                f.write(str2)
                f.write("\n")

                continue

            else:
                pass




            if link is not None:
                try:
                    driver.get(link)


                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav  =soup.find("nav",attrs={"id":"p-lang"})

                    div = nav.find("div",attrs={"class":"vector-menu-content"})
                    ul =  div.find("ul",attrs = {"class":"vector-menu-content-list"})
                    lis = ul.select("li")
                    h1 = soup.find("h1",attrs={"id":"firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for li in lis:
                        a = li.find("a")
                        lang  = a.attrs["lang"]

                        if lang == lan:
                            title = a.attrs["title"]
                            name = title.split("–")[0].strip()
                            if name.find("恒星列表") > 0:
                                starobject.EnglishLink = ""
                                try:
                                    print(name)
                                    db.session.commit()
                                except Exception as e:
                                    db.session.rollback()


                            else:
                                dict["name"]=name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href)> 2:
                                        dict["link"] = href

                except Exception as e:

                    pass
                finally:
                    result.append(dict)
                    str1 = "\""+starobject.EnglishName+"\"=\""+dict["name"]+"\";"
                    str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                    time.sleep(1)




    except Exception as e:
        print(e)


    finally:
        db.session.close()

    driver.quit()
    return json.dumps(result)



@web.route("/constellation/translate/en")
def constellationtranslateen():




    filename =  "constellation_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(Constellation).all()



        for starobject in stars:
            link = starobject.englishLink
            dict = {}
            dict["englishname"] = starobject.englishname
            dict["name"] = starobject.englishname
            dict["link"] = starobject.englishLink

            str1 = "\"" + starobject.englishname + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.englishname + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return "done"



@web.route("/star/translate/cn")
def startranslatecn():


    filename =  "star_cn.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(Star).all()



        for starobject in stars:
            dict = {}
            dict["englishname"] = starobject.EnglishName
            dict["name"] = starobject.EnglishName
            dict["link"] = ""

            if len(starobject.ChineseName) > 1:
                dict["name"] = starobject.ChineseName
            if len(starobject.ChineseLink)> 10:
                dict["link"] = starobject.ChineseLink

            str1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return "done"


@web.route("/galaxy/translate")
def galaxytranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "galaxy_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(Galaxy).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.EnglishName
            dict["name"] = galaxyobject.EnglishName
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.EnglishName + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.EnglishName + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.EnglishName
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + galaxyobject.EnglishName + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.EnglishName + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/galaxy/translate/en")
def galaxytranslateen():




    filename =  "galaxy_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(Galaxy).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            dict["englishname"] = starobject.EnglishName
            dict["name"] = starobject.EnglishName
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.EnglishName + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.EnglishName + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return "done"



@web.route("/opencluster/translate")
def openclustertranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "opencluster_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(OpenClusters).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.Identifier
            dict["name"] = galaxyobject.Identifier
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.Identifier + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.Identifier + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.Identifier
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + galaxyobject.Identifier + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.Identifier + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/opencluster/translate/en")
def openclustertranslateen():




    filename =  "opencluster_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(OpenClusters).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            identifier  = starobject.Identifier
            starobject.Identifier =  identifier.strip("\n")
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            dict["englishname"] = starobject.Identifier
            dict["name"] = starobject.Identifier
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.Identifier + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.Identifier + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return "done"



@web.route("/DiffuseNebulae/translate")
def DiffuseNebulaetranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "DiffuseNebulae_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(DiffuseNebulae).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.Name
            dict["name"] = galaxyobject.Name
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.Name + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.Name + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.Name
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + galaxyobject.Name + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.Name + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/DiffuseNebulae/translate/en")
def DiffuseNebulaetranslateen():




    filename =  "DiffuseNebulae_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(DiffuseNebulae).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            # identifier  = starobject.Identifier
            # starobject.Identifier =  identifier.strip("\n")
            # try:
            #     db.session.commit()
            # except Exception,e:
            #     db.session.rollback()
            #     print e.message
            dict["englishname"] = starobject.Name
            dict["name"] = starobject.Name
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.Name + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.Name + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    return "done"



@web.route("/GlobularCluster/translate")
def GlobularClustertranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "GlobularCluster_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(GlobularClusters).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.Identifier
            dict["name"] = galaxyobject.Identifier
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.Identifier + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.Identifier + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.Identifier
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + galaxyobject.Identifier + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.Identifier + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/GlobularCluster/translate/en")
def GlobularClustertranslateen():




    filename =  "GlobularCluster_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(GlobularClusters).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            identifier  = starobject.Identifier
            starobject.Identifier =  identifier.strip("\n")
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            dict["englishname"] = starobject.Identifier
            dict["name"] = starobject.Identifier
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.Identifier + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.Identifier+ "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    return "done"



@web.route("/PlanetaryNebulae/translate")
def PlanetaryNebulaetranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "PlanetaryNebulae_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(PlanetaryNebulae).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.Name
            dict["name"] = galaxyobject.Name
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.Name + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.Name + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.Name
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + galaxyobject.Name + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.Name + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/PlanetaryNebulae/translate/en")
def PlanetaryNebulaetranslateen():




    filename =  "PlanetaryNebulae_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(PlanetaryNebulae).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            identifier  = starobject.Name
            starobject.Name =  identifier.strip("\n")
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()

            dict["englishname"] = starobject.Name
            dict["name"] = starobject.Name
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.Name + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.Name + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return "done"





@web.route("/ProtoplanetaryNebulae/translate")
def ProtoplanetaryNebulaetranslateall():
    list = ["zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "ProtoplanetaryNebulae_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(ProtoplanetaryNebulae).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.Name
            dict["name"] = galaxyobject.Name
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.Name + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.Name + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

            if link is not None:
                try:
                    driver.get(link)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    nav = soup.find("nav", attrs={"id": "p-lang"})

                    div = nav.find("div", attrs={"class": "vector-menu-content"})
                    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
                    lis = ul.select("li")
                    # h1 = soup.find("h1", attrs={"id": "firstHeading"})
                    # try:
                    #     dict["englishname"] = h1.text
                    #     starobject.EnglishName = h1.text
                    #     db.session.commit()
                    # except Exception,e:
                    #     db.session.rollback()

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.Name
                        dict["link"] = ""

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href

                        f = f_list[i]
                        str1 = "\"" + galaxyobject.Name + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.Name + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as  e:
                    print(e)

                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/ProtoplanetaryNebulae/translate/en")
def ProtoplanetaryNebulaetranslateen():




    filename =  "ProtoplanetaryNebulae_en.txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')
    try:
        stars = db.session.query(ProtoplanetaryNebulae).all()

        for starobject in stars:
            link = starobject.EnglishLink
            dict = {}
            identifier  = starobject.Name
            starobject.Name =  identifier.strip("\n")
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            dict["englishname"] = starobject.Name
            dict["name"] = starobject.Name
            dict["link"] = starobject.EnglishLink

            str1 = "\"" + starobject.Name + "\"=\"" + dict["name"] + "\";"
            str2 = "\"" + starobject.Name + "_link\"=\"" + dict["link"]  + "\";"
            f.write(str1)
            f.write("\n")
            f.write(str2)
            f.write("\n")
    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    return "done"




@web.route("/messier/translate")
def messiertranslateall():
    list = ["en","zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "messier_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(Messier).all()

        for galaxyobject in galaxys:
            link = galaxyobject.englishLink
            dict = {}
            dict["englishname"] = galaxyobject.number
            dict["name"] = galaxyobject.commonName
            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]
                    str1 = "\"" + galaxyobject.number + "\"=\"" + dict["name"] + "\";"
                    str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"
                    f.write(str1)
                    f.write("\n")
                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

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

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.commonName
                        dict["link"] = ""
                        if lan == "en":
                            dict["link"] = galaxyobject.englishLink

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name.strip("\n")
                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href


                        f = f_list[i]
                        str1 = "\"" + galaxyobject.number + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/caldwell/translate")
def caldwelltranslateall():
    list = ["en","zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "cadlwell_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(Caldwell).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.number

            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]

                    str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"


                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

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

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.commonName
                        dict["link"] = ""
                        if lan == "en":
                            dict["link"] = galaxyobject.EnglishLink

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]

                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href


                        f = f_list[i]

                        str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"

                        f.write(str2)
                        f.write("\n")





                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"



@web.route("/messier/translate/en")
def messiertranslateen():


    filename = "messier_eb" + ".txt"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')

    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(Messier).all()

        for galaxyobject in galaxys:
            link = galaxyobject.englishLink
            dict = {}
            dict["englishname"] = galaxyobject.number
            dict["name"] = galaxyobject.commonName
            dict["link"] = link
            if len(link) < 5:

                str1 = "\"" + galaxyobject.number + "\"=\"" + dict["name"] + "\";"
                str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"
                f.write(str1)
                f.write("\n")
                f.write(str2)
                f.write("\n")

                continue

            else:
                pass

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
                    try:
                        dict["name"] = h1.text.strip("\n")
                        str1 = "\"" + galaxyobject.number + "\"=\"" + dict["name"] + "\";"
                        str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        f.write(str2)
                        f.write("\n")
                        print (str1)
                        print (str2)
                        galaxyobject.commonName = dict["name"]
                        db.session.commit()




                    except Exception as e:
                        print(e)
                        db.session.rollback()






                except Exception as  e:

                    pass
                finally:

                    time.sleep(1)




    except Exception as  e:
        print(e)


    finally:
        db.session.close()

    driver.quit()


    return "done"


@web.route("/wikipedia/translate",methods=['POST'])
def wikipediatranslateall():
    list = ["zh","ja","de","fr","es","pt","vi","ru","ko","it"]
    f_list  = []

    urlstring =  request.form.get("url")




    driver = webdriver.Chrome()
    result = []
    driver.get(urlstring)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    nav = soup.find("nav", attrs={"id": "p-lang"})

    div = nav.find("div", attrs={"class": "vector-menu-content"})
    ul = div.find("ul", attrs={"class": "vector-menu-content-list"})
    lis = ul.select("li")
    n = len(list)
    for i in range(0, n):
        lan = list[i]


        for li in lis:
            a = li.find("a")
            lang = a.attrs["lang"]

            if lang == lan:
                title = a.attrs["title"]
                name = title.split("–")[0].strip()
                print ("\n")
                print (lan +":"+name)






    driver.quit()
    return "done"




@web.route("/star/main/translate")
def starmaintranslateall():
    list = ["en","zh","de","es","fr","ko","it","ja","pt","ru","vi"]
    f_list  = []

    n = len(list)
    for str in list:
        filename = "mainstar_"+str + ".txt"

        txt_path = os.path.join(basedir, 'static/uploads', filename)
        f = open(txt_path, 'w')
        f_list.append(f)
    driver = webdriver.Chrome()
    result = []

    try:
        galaxys = db.session.query(Star).filter(Star.Magnitude < 2.21).all()

        for galaxyobject in galaxys:
            link = galaxyobject.EnglishLink
            dict = {}
            dict["englishname"] = galaxyobject.EnglishName

            dict["link"] = ""
            if len(link) < 5:
                for i in  range(0,n):
                    f = f_list[i]

                    str2 = "\"" + galaxyobject.number + "_link\"=\"" + dict["link"] + "\";"


                    f.write(str2)
                    f.write("\n")

                continue

            else:
                pass

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

                    for i in range(0, n):
                        lan = list[i]
                        dict["name"] = galaxyobject.EnglishName
                        dict["link"] = ""
                        if lan == "en":
                            dict["link"] = galaxyobject.EnglishLink

                        for li in lis:
                            a = li.find("a")
                            lang = a.attrs["lang"]

                            if lang == lan:
                                title = a.attrs["title"]
                                name = title.split("–")[0].strip()

                                dict["name"] = name.strip("\n")

                                href = a.attrs["href"]
                                if href is not None:
                                    if len(href) > 2:
                                        dict["link"] = href


                        f = f_list[i]

                        str1 = "\"" + galaxyobject.EnglishName + "\"=\"" + dict["name"] + "\";"
                        # str2 = "\"" + galaxyobject.EnglishName + "_link\"=\"" + dict["link"] + "\";"
                        f.write(str1)
                        f.write("\n")
                        # f.write(str2)
                        # f.write("\n")







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

@web.route("/japan/era/json")
def japanerajson():
    filename = "japanera" + ".json"

    json_path = os.path.join(basedir, 'static/uploads', filename)
    jsonf = open(json_path)
    jsondata = json.load(jsonf)

    filename1 = "japanera_japan" + ".json"

    json_path1 = os.path.join(basedir, 'static/uploads', filename1)
    f1 = open(json_path1,"w")

    filename2 = "japanera_en" + ".json"

    json_path2 = os.path.join(basedir, 'static/uploads', filename2)
    f2 = open(json_path2, "w")

    for dict in jsondata:
        str1 = "\"" + dict["english"] + "\"=\"" + dict["name"] + "\";"
        f1.write(str1)
        f1.write("\n")

        str2 = "\"" + dict["english"] + "\"=\"" + dict["english"] + "\";"
        f2.write(str2)
        f2.write("\n")
        # print dict

    return "done"


@web.route("/star/name/txt")
def starnametxt():
    starpath   = os.path.join(basedir, 'static/uploads', "star_names.txt")


    string = ""

    en = 1


    zn = 1

    json_path = os.path.join(basedir, 'static/uploads', "star_names_zh.txt")
    f1 = open(json_path, "w")

    with open(starpath, "r") as f:
        for line in f.readlines():




            lines = re.split("\t| |\n", line)

            hr =  lines[len(lines)-2]
            en  = en +1
            line = line.strip("\n")

            if  len(hr) ==2:
                hr ="  "+ hr
            elif len(hr) == 3:
                hr = " "+ hr



            try:
                hrstar = db.session.query(HRStar).filter_by(HR = hr)[0]

                hd = hrstar.HD.strip()
                try:
                    starobject = db.session.query(Star).filter_by(HDId = hd)[0]

                    chinesestring = starobject.ChineseName + "\t" + hr
                    string = string + "\n" + chinesestring

                    f1.write(chinesestring)

                    f1.write("\n")

                    zn = zn +1
                except Exception as e:
                    db.session.rollback()
                    string = string + "\n" + line
                    f1.write(line)
                    f1.write("\n")



            except Exception as e:
                db.session.rollback()

                f1.write(line)
                f1.write("\n")
                string = string +"\n"+line





    print ("done")
    print (en)
    print (zn)

    return string

def mkdir(path):
    # 引入模块


    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)


        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在

        return False

def excutetext(string):
    indexa = string.find('"')
    indexb = string.rfind('"')
    if indexb > indexa:
        return string[indexa+1:indexb]
    else:
        return string[indexa + 1:]




@web.route("/android/localized/<app>")
def  androidlocalized(app):

    list = ["en","de","es","fr","id","ja","ko","pt-PT","ru","zh-Hans","zh-HK","ms","th","vi"]

    n = len(list)

    for i in range(0,n):

        string = list[i]

        iospath = os.path.join(basedir, 'static/uploads/'+app+"/"+string+".lproj", "Localizable.strings")

        if os.path.exists(iospath):
            pass
        else:
            continue


        androiddorecroty = os.path.join(basedir, 'static/downloads/'+app+"/"+string)

        mkdir(androiddorecroty)

        androidpath = os.path.join(basedir, 'static/downloads/' + app + "/" + string,"strings.xml")

        f1 = open(androidpath, "w")

        left_str = ""
        right = ""

        with open(iospath, "r") as f:
            for line in f.readlines():
                line= line.strip()
                if line.find("=")> 0 and line.startswith('"'):
                    left_str = ""
                    right = ""
                    dengindex = line.find("=")

                    left = excutetext(line[:dengindex])
                    right =  excutetext(line[dengindex + 1:])
                    left_str = left.replace(" ","_")
                else:
                    index = line.find('";')
                    if index > 0:
                        right = right + "\n" + line[:index]
                    else:
                        right = right +"\n" + line
                if line.endswith('";'):

                    androidstring = '<string name="'+left_str+'">'+right+'</string>'
                    f1.write(androidstring)
                    f1.write("\n")










    return "done"



@web.route("/android/localized/<app>/<sub>")
def  androidsublocalized(app,sub):

    list = ["en","de","es","fr","id","ja","ko","pt-PT","ru","zh-Hans","zh-HK","ms","th","vi"]

    n = len(list)

    for i in range(0,n):

        string = list[i]

        iospath = os.path.join(basedir, 'static/uploads/'+app+"/"+string+".lproj", sub+".strings")

        if os.path.exists(iospath):
            pass
        else:
            continue


        androiddorecroty = os.path.join(basedir, 'static/downloads/'+app+"/"+string)

        mkdir(androiddorecroty)

        androidpath = os.path.join(basedir, 'static/downloads/' + app + "/" + string, sub+"_strings.xml")

        f1 = open(androidpath, "w")

        left_str = ""
        right = ""

        with open(iospath, "r") as f:
            for line in f.readlines():
                line= line.strip()
                if line.find("=")> 0 and line.startswith('"'):
                    left_str = ""
                    right = ""
                    dengindex = line.find("=")

                    left = excutetext(line[:dengindex])
                    right =  excutetext(line[dengindex + 1:])
                    left_str = left.replace(" ","_")
                else:
                    index = line.find('";')
                    if index > 0:
                        right = right + "\n" + line[:index]
                    else:
                        right = right +"\n" + line
                if line.endswith('";'):

                    androidstring = '<string name="'+left_str+'">'+right+'</string>'
                    f1.write(androidstring)
                    f1.write("\n")










    return "done"






