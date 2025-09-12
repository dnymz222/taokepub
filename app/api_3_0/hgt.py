#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage,hefengfishingapikey,hefengusername
import json
from flask import request,session,url_for,redirect
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
import requests
from config import basedir
import os
import numpy as np
import shutil
from flask import send_file
import rasterio
import  tifffile
import zipfile
# from matplotlib import pyplot as plt
from selenium import webdriver
from requests.auth import HTTPBasicAuth
import requests

SAMPLES = 3601  # Change this to 3601 for SRTM1
HGTDIR = 'hgt'  # All 'hgt' files will be kept here uncompressed



@api3.route("/hgt/elevation")
def hgtelevation():
    lat = request.args.get('lat', '30.2870')
    lng = request.args.get('lng', '119.9872')
    t = request.args.get("t","100")
    s = request.args.get("s","11122")
    url = "http://www.astronomyobserver.net/api/v3.0/elevation?s=" + s + "&lat=" + lat + "&lng=" + lng + "&t="+ t +""

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        return content
    except Exception as e:

        dict = {}
        dict[x_code] =201
        dict[x_meesage] = "%s"%e
        return  json.dumps(dict)


@api3.route("/elevation")
def tifelevationfromastronomy():
    lat = request.args.get('lat', '30.2870')
    lng = request.args.get('lng', '119.9872')
    t = request.args.get("t","100")
    s = request.args.get("s","11122")
    url = "http://www.astronomyobserver.net/api/v3.0/elevation?s=" + s + "&lat=" + lat + "&lng=" + lng + "&t="+ t +""

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        content = response.read()
        return content
    except Exception as e:

        dict = {}
        dict[x_code] =201
        dict[x_meesage] = "%s"%e
        return  json.dumps(dict)


@api3.route("/tif/elevation")
def tifelevation():
    lat = request.args.get('lat', '30.2870')
    lng = request.args.get('lng', '119.9872')
    timestamp = request.args.get('time', '1585843200')
    total = request.args.get('total', '1599918717')
    result = {}


    try:
        evlation =  get_tiff_elavation(float(lng),float(lat))
        result[x_data]  =evlation
        result[x_code] = 200
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)

@api3.route("/hgt/download/clean")
def hgtdownloadclean():
   path =  os.path.join("/Volumes/KINGSTON","N51")
   try:

       for parent, _, fileNames in os.walk(path):
           for filename in fileNames:
               try:
                   if filename.find("zip") > 0:
                       if filename.find("__") > -1:
                           opath = os.path.join(path, filename)
                           os.remove(opath)
                   else:
                       opath = os.path.join(path, filename)
                       os.remove(opath)

               except Exception as e:
                   print(e)



   except Exception as e:
       print(e)

   return "done"


@api3.route("/hgt/unzip")
def hgtunzip():
   path = os.path.join("/Volumes/KINGSTON", "hgtzip")
   epath = os.path.join("/Volumes/KINGSTON","hgt")
   try:

       for parent, _, fileNames in os.walk(path):
           for filename in fileNames:
               if filename.find("zip") > 0:

                   try:
                        fpath = os.path.join(path,filename)
                        with zipfile.ZipFile(fpath) as z_file:
                            z_file.extractall(epath)
                   except Exception as e:
                       print(e)



   except Exception as e:
       print(e)

   return "done"

@api3.route("/hgt/download")
def hgtdownload():
   path =  os.path.join(basedir,"static/chinahgt")
   filename =  request.args.get('file', 'N30E120') +".SRTMGL1.hgt.zip"

   try:
       fpath = os.path.join(path, filename)
       return send_file(fpath,as_attachment=True)

   except Exception as e:
       return (e)


@api3.route("/hgt/download/usgs")
def hgtdownloadusgs():

   spath =  os.path.join("/Volumes/KINGSTON","hgtzip")
   n = 0
   try:
       txtpath = os.path.join(spath,"66.txt")
       tf = open(txtpath,"r")
       for line in tf.readlines():
            url =  line.strip()
            n = n + 1
            continue
            filename = url[-23:]
            fpath = os.path.join(spath, filename)
            if os.path.exists(fpath):
                continue
            print( n)

            try:
                response = requests.get(url)
                if response.history:
                    # when you try to download the request will be redirect for permorming the authentification
                    # then we should use the redirected url in a pair with basic auth
                    final_url = response.url
                else:
                    final_url = url
                r =  requests.get( final_url, stream=True, auth=HTTPBasicAuth("dbymz222", "Hyh671002"))
                if r.status_code != 200:
                    print ("faile:" + url)
                else:
                    f = open(str(fpath), "wb")
                    shutil.copyfileobj(r.raw, f, length=16 * 1024 * 1024)
            except Exception as e:
                print ("error:"  + url)


   except Exception as e:
       return "%s"%e
   print(n)
   return "done"

# @api3.route("/tiff/plot/<location>")
# def tiffplot(location):
#     path = os.path.join(basedir, "static/hgt")
#     filename = location +".tif"
#     try:
#         fpath = os.path.join(path,filename)
#         with rasterio.open(fpath) as src:
#             # Read the elevation data from the file
#             elevation_data = src.read(1)
#
#             # Set the contour levels
#
#             contour_levels = np.arange(0, elevation_data.max(), 100)
#
#             # Create a contour plot
#             C = plt.contourf(elevation_data, contour_levels, cmap='terrain')
#
#             plt.axis('off')  # 去除坐标轴
#             plt.xticks([])  # 去除刻度
#             plt.yticks([])  # 去除刻度
#             # plt.clabel(C, inline=True, fontsize=10)
#
#             imagefile = os.path.join(path,location +".png")
#
#
#             # Add a colorbar to the plot
#             # plt.colorbar()
#
#             # Show the plot
#             plt.show()
#             plt.close()
#
#             src.close()
#
#     except Exception,e:
#         print e.message
#     return "done"




@api3.route("/hgt/download/count")
def hgtdownloadcount():
   path =  os.path.join("/Users/xueping/Downloads/chrome","hgt")
   path = os.path.join("/Volumes/KINGSTON", "chinahgt")
   n = 0
   s = 0
   try:

       for parent, _, fileNames in os.walk(path):
           for filename in fileNames:
               s =  s + 1
               if filename.find(".zip") > 0:
                   n = n + 1
                   hgtfilename = filename[:7] +".hgt"
                   hgtpath = os.path.join(path,hgtfilename)
                   if not os.path.exists(hgtpath):
                       print (filename)





   except Exception as e:
       print(e)

   print (n)
   print (s)
   return "done"



@api3.route("/hgt/move")
def hgtmove():
    cpath = os.path.join("/Volumes/KINGSTON", "90metertif")
    path = os.path.join("/Volumes/KINGSTON","90meterother")
    list = ["N6","N7","N8","N9","S6","S7","S8","S9"]

    try:
        for parent, _, fileNames in os.walk(cpath):
            for filename in fileNames:
                fprefix = filename[:2]
                if fprefix in list:
                     opath = os.path.join(cpath,filename)
                     wpath = os.path.join(path,filename)
                     shutil.move(opath,wpath)


    except Exception as e:
        print(e)


    return "done"


@api3.route("/hgt/convert")
def hgtconvert():

    path = os.path.join("/Volumes/KINGSTON","hgt")
    tifpath = os.path.join("/Volumes/KINGSTON", "tif")
    n = 0

    try:

        for parent, _, fileNames in os.walk(path):
            for filename in fileNames:
                if filename.find(".hgt") > 0:
                    n = n + 1
                    print (n)
                    try:
                        hgtpath = os.path.join(path,filename)
                        with rasterio.open(hgtpath) as src:
                            # Get the metadata of the source file
                            meta = src.meta.copy()

                            # Update the metadata for the output GeoTIFF file
                            meta.update(driver='GTiff', compress='lzw')
                            name = filename[:7] +".tif"
                            # Set the output file name and path
                            output_file = os.path.join(tifpath,name)

                            # Create the output GeoTIFF file
                            with rasterio.open(output_file, 'w', **meta) as dst:
                                # Read the data from the source file
                                data = src.read(1)

                                # Write the data to the output file
                                dst.write(data, 1)
                                dst.close()
                            src.close()
                    except Exception as e:
                        print(e)




    except Exception as e:
        print(e)


    return "done"


def get_elavation(lon,lat):
    filename = get_file_name(lon, lat)
    file_path = os.path.join(basedir, 'static/hgt', filename)
    evlation = 0
    try:
        evlation = read_elevation_from_file(file_path, lon, lat)
    except Exception as e:
        print(e)
        pass
    return evlation

def get_tiff_elavation(lon,lat):
    filename = get_tiff_file_name(lon, lat)
    file_path = os.path.join(basedir, 'static/chinatif', filename)
    evlation = 0
    try:
        evlation = read_elevation_from_file(file_path, lon, lat)
    except Exception as e:
        print ("error")
        print (e)
        pass
    return evlation


def get_tiff_file_name(lon, lat):
    """
    Returns filename such as N27E086.hgt, concatenated
    with HGTDIR where these 'hgt' files are kept
    """

    if lat >= 0:
        ns = 'N'
    elif lat < 0:
        ns = 'S'

    if lon >= 0:
        ew = 'E'
    elif lon < 0:
        ew = 'W'

    tif_file = "%(ns)s%(lat)02d%(ew)s%(lon)03d.tif" % {'lat': abs(lat), 'lon': abs(lon), 'ns': ns, 'ew': ew}
    return tif_file


def get_file_name(lon, lat):
    """
    Returns filename such as N27E086.hgt, concatenated
    with HGTDIR where these 'hgt' files are kept
    """

    if lat >= 0:
        ns = 'N'
    elif lat < 0:
        ns = 'S'

    if lon >= 0:
        ew = 'E'
    elif lon < 0:
        ew = 'W'

    hgt_file = "%(ns)s%(lat)02d%(ew)s%(lon)03d.hgt" % {'lat': abs(lat), 'lon': abs(lon), 'ns': ns, 'ew': ew}
    return hgt_file



def read_elevation_from_file(hgt_file, lon, lat):
        src = rasterio.open(hgt_file)
        # Read the elevation data from the file
        elevation_data = src.read(1)



        # Get the row and column indices for the given latitude and longitude
        row, col = src.index(lon, lat)


        # Get the elevation at the given location
        elevation = elevation_data[int(row), int(col)].astype(int)
        src.close()
        return elevation



@api3.route("/check/hgt")
def checkhgtsize():
    file_path = os.path.join(basedir, 'static/hgt')
    for root, dirs, files in os.walk(file_path):
        for file  in files:
            file_name_pth = os.path.join(basedir, 'static/hgt', file)
            n = checkhgt(file_name_pth)
            print (n)

    return  "done"

@api3.route("/vnl10/move")
def vnl10move():
    download_path = os.path.join(basedir, 'static/vnl2014')
    wepb_path = os.path.join(basedir, 'static/vnl201410')
    emptydict = {}
    for z in range(10, 11):
        for x in range(0, int(pow(2, z) + 0.1)):
            for y in range(0, int(pow(2, z) + 0.1)):
                try:


                    wname = str(z) + "_" + str(x) + "_" + str(y) + ".webp"

                    fPath = os.path.join(download_path, wname)

                    wPath = os.path.join(wepb_path, wname)

                    if os.path.exists(fPath):
                        shutil.move(fPath,wPath)



                except Exception as e:
                    print(e)

    return "done"


def checkhgt(hgt_file):

    with open(hgt_file, 'rb') as hgt_data:
        pass