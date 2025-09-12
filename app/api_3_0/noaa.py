
#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,make_response
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
from app.water import water
from app.worldTidalStation import worldTidalStation
from app.chinaTidalStation import chinaTidalStation
import gzip
from app.utils.constvalue import acuuappkey,xinzhi_prinvate_key,xinzhi_public_key,openweather_key,meteobule_apikey
import metpy.calc as mpcalc
from metpy.units import units
import gzip
from io import StringIO
import requests
import pytz

tz = pytz.timezone("GMT")







@api3.route("/aurora/color")
def auroraColor():
    list = []
    for i in range(0,101):
        color = hex(aururo_to_rgb(i))
        list.append(color)
    print(list)
    return json.dumps(list)





def aururo_to_rgb(elevation):

    if elevation < 1:
        return 0

    normalized_value = elevation

    breakpoints = [

        (0,(126,161,140)),
        (10,(1,228,0)),
        (30,(58,255,5)),
        (50, (255,251,0)),
        (70, (255,166,2)),
        (90, (250,1,0)),
        (101, (177,32,0))


    ]



    # Find the two neighboring breakpoints for the normalized value
    prev_breakpoint, prev_color = breakpoints[0]
    for next_breakpoint, next_color in breakpoints[1:]:
        if normalized_value < next_breakpoint:
            break
        prev_breakpoint, prev_color = next_breakpoint, next_color

    # Interpolate between the neighboring colors
    prev_normalized, prev_rgb = prev_breakpoint, prev_color
    next_normalized, next_rgb = next_breakpoint, next_color
    t = (normalized_value - prev_normalized) / (next_normalized - prev_normalized)

    r = prev_rgb[0] + int((next_rgb[0] - prev_rgb[0]) * t)
    g = prev_rgb[1] + int((next_rgb[1] - prev_rgb[1]) * t)
    b = prev_rgb[2] + int((next_rgb[2] - prev_rgb[2]) * t)

    # Clamp the RGB values to the valid range (0-255)
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    return b + g * 256 + r * 256 * 256 + 255 * 256 * 256 * 256


