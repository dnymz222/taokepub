#codeing=utf8
# -*- coding: utf-8 -*-
from . import web

from selenium import webdriver
from bs4 import BeautifulSoup
import time

import os
import json
from  config import basedir

from timezonefinder import TimezoneFinder

tf = TimezoneFinder()




@web.route("/buoy/station/list")
def buoystationlist():
    driver = webdriver.Chrome()
    list = []
    try:
        url = "https://www.ndbc.noaa.gov/to_station.shtml"
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        maindiv = soup.find("main", attrs={"id": "contents"})
        stattionlist = maindiv.select(".station-list")
        for stattion in stattionlist:
            links = stattion.select("a")
            for link in links:
                dict= {}
                dict["id"] = link.text
                dict["href"] = link.attrs["href"]
                list.append(dict)

    except Exception as e:
        print(e)

    driver.quit()

    image_path = os.path.join(basedir, 'static/noaa', "buoystation.json")
    f = open(image_path, "w")
    f.write(json.dumps(list))
    f.close()

    return json.dumps(list)

@web.route("/buoy/station/locations")
def buoystationlocations():
    driver = webdriver.Chrome()
    list = []
    image_path = os.path.join(basedir, 'static/noaa', "buoystation.json")
    f = open(image_path, "r")
    slist = json.loads(f.read())
    for sdict in slist:
        url = "https://www.ndbc.noaa.gov/" + sdict["href"]
        try:
            driver.get(url)
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            maindiv = soup.find("main", attrs={"id": "contents"})
            div = maindiv.find("div",attrs={"id":"stn_metadata"})
            p = div.find("p")
            sdict["p"] = p.text
            list.append(sdict)


        except Exception as e:
            print (e)
    driver.quit()

    image_path = os.path.join(basedir, 'static/noaa', "buoystationlocations.json")
    f = open(image_path, "w")
    f.write(json.dumps(list))
    f.close()

    return json.dumps(list)