#coding=utf8
from flask import render_template,request,session,Blueprint,redirect,url_for

import json
from flask import request,session
from app import db

from app.appconfig import appconfig

import sys
from app.banner import banner
import urllib
from app.welfare import welfare

main = Blueprint('main', __name__)



# @main.route('/', defaults={'path': ''})
# @main.route('/<path:path>')
# def catch_all(path):
#     return render_template("index.html")



@main.route('')
def index():


    return render_template('index.html')


@main.route('app')
def homeindex():

    return render_template('index.html')

@main.route('promotion')
def promotion():

    bannerresult = db.session.query(banner).filter_by(type=1).order_by(banner.index).all()

    return render_template('promotion.html',banners = bannerresult,download = True)

@main.route('activity')
def activity():

    bannerresult = db.session.query(banner).filter_by(type=3).order_by(banner.index).all()

    return render_template('activity.html',banners = bannerresult,download = True)



@main.route('p%e5%9b%9eT%e9%80%80%e8%ae%a2')
def simpromotion():


    bannerresult = db.session.query(banner).filter_by(type=2).order_by(banner.index).all()
    appconfigobject = db.session.query(appconfig).filter(appconfig.source == 'p')[0]
    return render_template('promotion.html',banners = bannerresult,download= appconfigobject.showdiscount)


@main.route('p')
def ddsimpromotion():
    return  'hello world'

    bannerresult = db.session.query(banner).filter_by(type=2).order_by(banner.index).all()
    appconfigobject = db.session.query(appconfig).filter(appconfig.source == 'p')[0]
    return render_template('promotion.html',banners = bannerresult,download= appconfigobject.showdiscount)



@main.route("fishing")
def fishinghome():
    return render_template("fishingdownload.html")


@main.route("meteocalc")
def meteocalchome():
    return render_template("meteocalc.html")



@main.route("tide")
def tidehome():
    return render_template("tideapp.html")

@main.route("astronomy")
def astronomyhome():
    return render_template("astronomyapp.html")


@main.route("solunar")
def solunarhome():
    return render_template("solunarapp.html")



@main.route('download')
def download():
    return render_template('download.html')

@main.route('lamadownload')
def lamadownload():
    return render_template('lamadownload.html')

@main.route('index')
def indexdownload():
    #return redirect('home')
    return render_template('download.html')
    # return render_template('baidu.html')
@main.route('lamaindex')
def lamaindexdownload():
    #return redirect('home')
    return render_template('lamadownload.html')

@main.route('intru')
def intrudownload():
    #return redirect('home')
    return render_template('download.html')
    # return render_template('baidu.html')


@main.route('info')
def infodownload():
    #return redirect('home')
    return render_template('download.html')
    # return render_template('baidu.html')

@main.route('inhome')
def inhomedownload():
    #return redirect('home')
    return render_template('download.html')
    # return render_template('baidu.html')

@main.route('pinduoduo')
def pinduoduo():
    #return redirect('home')
    return render_template('pinduoduo.html')
    # return render_template('baidu.html')

@main.route("auth/redircet")
def authredirect():
    return ""



@main.route("auth/fishing/redircet")
def authfihsingredirect():
    return ""






@main.route('welfare')
def welfarehtml():
    typestr = request.args.get('type','1')
    typeint = int(typestr)

    try:
        welfarereslut = welfare.query.filter_by(type=typeint)[0]
        urlstr = welfarereslut.activeUrl

        return render_template('welfare.html',url = urlstr)
        
    except  Exception as  e:
        db.session.rollback()
        return render_template('error.html')

        
   
      



    







@main.route('aboutus')
def aboutus():
    return render_template('aboutus.html')

@main.route('contact')
def contact():
    return render_template('contact.html')




