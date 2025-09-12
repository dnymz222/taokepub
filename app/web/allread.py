#coding=utf8
from . import web

import json

from app import db
import time
from flask import request,render_template
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

import random









# @web.route('/read/all/delete')
# def alldelete():
#     nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#     nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
# #    print nowTime
#
#     # deno =  int(request.args.get('deno'))
#     coupons = db.session.query(allcoupon).all()
#     for couponobject in coupons:
#
#         try:
#
#             if  couponobject.sellCount < 3000 and couponobject.couponDenomination < 100:
#
#                 db.session.delete(couponobject)
#                 db.session.commit()
#
#
#         except:
#             db.session.rollback()
#             continue
#         finally:
#             pass
#     db.session.close()
#     return "删除过期商品成功"









