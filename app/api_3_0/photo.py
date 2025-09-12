#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
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
from  app.Camera import Camera


@api3.route("/camera/npf")
def camaranpf():
    result = {}
    list = []

    try:
        cameras = db.session.query(Camera).all()
        for cameraobject in cameras:
            dict = cameraobject.CameraDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)

