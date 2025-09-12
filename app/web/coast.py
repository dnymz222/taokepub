#codeing=utf8
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




@web.route("/noaa/harcon")
def harcon():
    path = os.path.join(basedir, 'static/downloads', "harconfull.json")
    driver = webdriver.Chrome()

    driver.get("https://tidesandcurrents.noaa.gov/stations.html?type=Harmonic+Constituents")
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"id": "maincontent"})
    span12s = div.select(".areaheader")
    result = []

    for span12 in span12s:
        rowfluids = span12.select(".row-fluid")
        for rowfluid in rowfluids:
            divs = rowfluid.select("div")
            for stattion in divs:
                dict = {}
                dict["id"] = stattion.attrs["id"][1:]
                a = stattion.find("a")
                dict["name"] = a.text.replace(dict["id"], "").strip()
                dict["href"] = a.attrs["href"]
                result.append(dict)





    driver.quit()

    for dict in result:
        try:

            href = "https://tidesandcurrents.noaa.gov/" + dict["href"]
            driver2 = webdriver.Chrome()

            driver2.get(href)
            time.sleep(3)
            html2 = driver2.page_source
            soup2 = BeautifulSoup(html2, 'lxml')
            table = soup2.find("table", attrs={"class": "table-striped"})
            tbodys = table.select("tbody")

            hars = []
            for tbody in tbodys:
                tds = tbody.select("td")
                list = []
                for td in tds:
                    list.append(td.text)
                hars.append(list)
            dict["hars"] = hars

        except Exception as e:
            print (e)



        finally:
            driver2.quit()
    f2 = open(path, 'w')
    f2.write(json.dumps(result))
    f2.close()

    return json.dumps(result)