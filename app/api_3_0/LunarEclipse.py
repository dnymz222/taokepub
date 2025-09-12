#coding=utf8
import os.path

from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,make_response
from app import db
import urllib
import hashlib

import time
import datetime as date_time_m
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
from config import basedir
from PIL import Image as PILImage

from urllib.request import urlopen

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade
import matplotlib.image  as mpimage
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from flask import send_file

from cartopy.io.shapereader import Reader
import paramiko
import matplotlib.gridspec as gridspec
from shapely.geometry import GeometryCollection,Point,shape

from app.SolarEclipse import SolarEclipse
from app.SolarEclipseCalculate import SolarEclipseCalculate

# import  geopandas as  gpd

# import cv2


# @api3.route("/lunar/video")
# def lunarvideo():
#
#
#     date = "2030-06-15"
#
#     path = os.path.join(basedir,"static/LunarEclipse/" + date +"/english")
#
#     imagelist = []
#
#     for i in range(0,420):
#         imagename  = "lunar_"+ date +"_" + str(i) + ".png"
#         imagepath = os.path.join(path,imagename)
#         if os.path.exists(imagepath):
#             imagelist.append(imagepath)
#
#     mp4path = os.path.join(basedir,"static/LunarEclipse", date + "_en.mp4")
#
#     frame = cv2.imread(imagelist[0])
#     height,width,layers = frame.shape
#
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#
#     video = cv2.VideoWriter(mp4path, fourcc, 12, (width, height))
#     for image in imagelist:
#         video.write(cv2.imread(image))
#
#     cv2.destroyAllWindows()
#     video.release()
#
#
#
#     return "done"


