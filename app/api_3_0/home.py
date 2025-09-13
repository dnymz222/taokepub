#coding=utf8
from . import api3
import time
import datetime
# from app.coupon import coupon

from app import db
from app.utils.constvalue import x_data,x_code,x_meesage
import json
from flask import request

import time
from app.banner import banner

from app.welfare import welfare

from app.column import column
from app.launchad import launchad
import random

from app.appitem import appitem
from app.downloadAd import downloadAd
from app.DownloadAdClick import downloadAdClick
from app.saleconfig import saleconfig




@api3.route('/soluanr/config')
def soluanrconfig():
    result = {}
    result[x_code] = 200
    dict = {}

    # isVip = request.args.get('isVip', '0')
    # userType = request.args.get('userType', '0')
    #
    # if isVip == "0" and userType == "1":
    #     dict["isOpen"] = True
    #     dict["isUpgrade"] = True
    # else:
    #     dict["isOpen"] = False
    #     dict["isUpgrade"] = True
    # dict["homeText"] = "过期会员升级终身会员原48元现28元"
    # dict["amount"] = "28.00"
    # dict["mineText"] = "会员过期可优惠升级终身会员"
    # dict["buttonText"] = "过期会员升级终身会员:￥28"
    # dict["tipText"] = "为回馈用户，原价48的终身会员,之前包年会员过期的可28元升级终身会员"
    # dict["orderName"] = "日出日落月相升级终身会员"
    # result[x_data] = dict
    # return json.dumps(result)


    outtime = datetime.datetime(2024,9, 6, hour=0, minute=0, second=0, microsecond=0)

    nowtime = datetime.datetime.now()

    if outtime > nowtime:
        dict["isOpen"] = True
        dict["isUpgrade"] = False
    else:
        dict["isOpen"] = False
        dict["isUpgrade"] = False

    # isVip = request.args.get('isVip', '0')
    # userType = request.args.get('userType', '0')
    # if isVip == "0" and userType != "0":
    #     dict["isOpen"] = True
    # else:
    #     dict["isOpen"] = False

    dict["homeText"] = "五周年特惠终身会员原48元现28元"
    dict["amount"] = "28.00"
    dict["mineText"] = "五周年特惠"
    dict["buttonText"] = "五周年特惠(终身会员:原￥48):￥28"
    dict["tipText"] = "为回馈用户，日出日落月相安卓版五周年推出特惠"
    dict["orderName"] = "日出日落月相五周年特惠(终身会员)"
    result[x_data] = dict
    return json.dumps(result)

@api3.route('/meteo/config')
def meteoconfig():
    result = {}
    result[x_code] = 200
    dict = {}
    outtime = datetime.datetime(2023, 11, 6, hour=0, minute=0, second=0, microsecond=0)

    nowtime = datetime.datetime.now()

    if outtime > nowtime:
        dict["isOpen"] = True
    else:
        dict["isOpen"] = False

    dict["homeText"] = "2023,2024跨年特惠:终身会员原48元现38元"
    dict["amount"] = "28.00"
    dict["mineText"] = "双11特惠"
    dict["buttonText"] = "双11特惠(终身会员:原价￥48)：￥28"
    dict["tipText"] = "双11期间推出双11特惠"
    dict["orderName"] = "日出日落月相双11特惠(终身会员)"
    result[x_data] = dict
    return json.dumps(result)

@api3.route('/fish/config')
def fishconfig():

    result = {}
    result[x_code] = 200
    dict = {}

    outtime = datetime.datetime(2024,8, 10, hour=0, minute=0, second=0, microsecond=0)

    nowtime = datetime.datetime.now()

    if outtime > nowtime:
        dict["isOpen"] = True
    else:
        dict["isOpen"] = False

    # isVip = request.args.get('isVip', '0')
    # userType = request.args.get('userType', '0')
    # if isVip == "0" and userType != "0":
    #     dict["isOpen"] = True
    # else:
    #     dict["isOpen"] = False

    dict["homeText"] = "钓鱼天气五周年特惠终身会员原98元现48元"
    dict["amount"] = "48.00"
    dict["mineText"] = "五周年特惠"
    dict["buttonText"] = "五周年特惠(终身会员:原价￥98):￥48"
    dict["tipText"] = "为回馈用户，钓鱼天气安卓版五周年推出特惠"
    dict["orderName"] = "钓鱼天气五周年特惠(终身会员)"
    result[x_data] = dict
    return json.dumps(result)



@api3.route('/astro/config')
def astroconfig():
    result = {}
    result[x_code] = 200
    dict = {}

    outtime = datetime.datetime(2024,11, 1, hour=0, minute=0, second=0, microsecond=0)

    nowtime = datetime.datetime.now()

    if outtime > nowtime:
        dict["isOpen"] = True
    else:
        dict["isOpen"] = False

    # isVip = request.args.get('isVip', '0')
    # userType = request.args.get('userType', '0')
    # if isVip == "0" and userType != "0":
    #     dict["isOpen"] = True
    # else:
    #     dict["isOpen"] = False

    dict["homeText"] = "追寻彗星特惠终身会员原98元现48元"
    dict["amount"] = "48.00"
    dict["mineText"] = "追寻彗星特惠"
    dict["buttonText"] = "追寻彗星特惠(终身会员:原价￥98):￥48"
    dict["tipText"] = "C2023 A3 紫金山-阿特拉斯,可能是数十年来最亮的彗星，特提供终身会员特惠持续关注"
    dict["orderName"] = "天文观星指南追寻彗星(终身会员)"
    result[x_data] = dict
    return json.dumps(result)

@api3.route('/xunquan/config')
def newconfig():

    soure = request.args.get("source","xunquan")
    result = {}
    result[x_code] = 200
    dict = {}
    dict['opentaobao'] = 1  # 是否打开淘宝
    dict['openh5'] = 0  # 打开h5详情页
    dict['showdiscount'] = 1  # 小程序显示优惠券
    dict['showscore'] = 3  # iOS显示评分功能所需打开应用的次数
    dict['cartpath'] = 'cart.html'  # 购物车链接所含字符
    dict['showdetail'] = 1  # 打开原生详情页
    dict['showrate'] = 10  # 显示评论
    dict['showtaobao'] = 2
    # if  soure == "lunartides":
    #     dict['showtaobao'] = 1  # 钓鱼天气，日月潮汐表是否显示商城界面 0：不展示 1：安装淘宝展示 2：展示
    # else:
    #     dict['showtaobao'] =  0 #钓鱼天气，日月潮汐表是否显示商城界面 0：不展示 1：安装淘宝展示 2：展示
    # dict['guideurl'] = ''
    # "var a = st.getElementsByTagName('a')[0];" \
    # "var is = a.getAttribute('href');" \
    # "var fi = is.indexOf('shop_id=');" \
    dict['cartjs'] = "var scancart = function scan () {" \
                     "var gs = document.getElementsByClassName('bundlev2');" \
                     "var list =[];" \
                     "for (i=0;i< gs.length;i++) {" \
                     "var g_i = gs[i];" \
                     "var so = g_i.getElementsByClassName('shop')[0];" \
                     "if (so == undefined) continue;" \
                     "var sn = so.getElementsByClassName('title')[0];" \
                     "var sc = sn.textContent;" \
                     "var its = g_i.getElementsByClassName('item-info');" \
                     "for (j=0;j< its.length;j++){" \
                     "var dict = {};" \
                     "var g_i = its[j];" \
                     "var t = g_i.getElementsByClassName('title')[0];" \
                     "var gn = t.textContent;" \
                     "dict['title'] = gn;" \
                     "dict['itemId'] = sc;" \
                     "list.push(dict);" \
                     "}" \
                     "}" \
                     "return list;" \
                     "};"
    # 扫描购物车商品的js
    # print dict['cartjs']

    result[x_data] = dict

    return json.dumps(result)


@api3.route("/launch/ad")
def getlaunuchad():
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    osstring = request.args.get('os','iOS')
    result = {}

    statusvalue =1
    source = request.args.get("source","xunquan")
    if source == "solunar":
        statusvalue = 2
    try:
        launchadobject= db.session.query(launchad).filter(launchad.endTime > nowTime).filter_by(
            status=statusvalue,os = osstring).all()
        size = len(launchadobject)
        if size >0:
            index = random.randint(0,size-1)
            launchaditem = launchadobject[index]
            result[x_data] = launchaditem.launchadDict()
            result[x_code] = 200
        else:
            result[x_code]=201
            result[x_meesage] = 'nodata'

    except Exception as e:
        db.session.rollback()
        result[x_code] = 201
        result[x_meesage] = "%s"%e
    finally:
        db.session.close()

    return json.dumps(result)




@api3.route('/xunquan/banner')
def xunquanbanner():
    result = {}
    bannnerList = []


    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    try:
        bannerresult = db.session.query(banner).filter(banner.endTime > nowTime).filter_by(plat=0).order_by(
            banner.index).all()

        for banneritem in bannerresult:
            bannerdict = banneritem.promotiondict()
            bannnerList.append(bannerdict)
        result[x_code] = 200
        result[x_data] = bannnerList
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()
    return json.dumps(result)


@api3.route('/fish/banner')
def fishbanner():
    result = {}
    bannnerList = []


    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    try:
        bannerresult = db.session.query(banner).filter(banner.endTime > nowTime).filter_by(plat =2).order_by(
            banner.index).all()

        for banneritem in bannerresult:
            bannerdict = banneritem.promotiondict()
            bannnerList.append(bannerdict)
        result[x_code] = 200
        result[x_data] = bannnerList
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()
    return json.dumps(result)





@api3.route('/solunar/banner')
def solunarbanner():
    result = {}
    bannnerList = []


    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    try:
        bannerresult = db.session.query(banner).filter(banner.endTime > nowTime).filter_by(plat =3).order_by(
            banner.index).all()

        for banneritem in bannerresult:
            bannerdict = banneritem.promotiondict()
            bannnerList.append(bannerdict)
        result[x_code] = 200
        result[x_data] = bannnerList
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()
    return json.dumps(result)



@api3.route('/ad/banner')
def adbanner():
    result = {}
    bannnerList = []

    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    platString = request.args.get("plat","2")
    platvalue = int(platString)
    

    try:
        bannerresult = db.session.query(banner).filter(banner.endTime > nowTime).filter_by(plat =platvalue).order_by(
            banner.index).all()

        for banneritem in bannerresult:
            bannerdict = banneritem.promotiondict()
            bannnerList.append(bannerdict)
        result[x_code] = 200
        result[x_data] = bannnerList

    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()
    return json.dumps(result)


@api3.route('/ad/download')
def addownload():
    dict = {}

    result = {}

    result[x_meesage] =201
    result[x_data] ="no data"

    return json.dumps(result)



    # platvalue = request.args.get("plat", "1")
    # channelvalue = request.args.get("channel", "0")
    #
    # try:
    #     download_ads = db.session.query(downloadAd).filter_by(plat=platvalue, status=1, channel=channelvalue).order_by(
    #         downloadAd.index).all()
    #
    #     size = len(download_ads)
    #     if size > 0:
    #         index = random.randint(0, size - 1)
    #         downloadaditem = download_ads[index]
    #         result[x_data] = downloadaditem.downloaddict()
    #         result[x_code] = 200
    #     else:
    #         result[x_code] = 201
    #         result[x_meesage] = 'nodata'
    #
    # except Exception, e:
    #     result[x_meesage] = e.message
    #     result[x_code] = 201
    #     db.session.rollback()
    #
    # finally:
    #     db.session.close()
    # return json.dumps(result)



@api3.route('/help/promote')
def helppromote():
    dict = {}

    result = {}

    platvalue = request.args.get("plat", "1")
    channelvalue = request.args.get("channel", "0")

    try:
        download_ads = db.session.query(downloadAd).filter_by(plat=platvalue, status=1, channel=channelvalue).order_by(
            downloadAd.index).all()

        size = len(download_ads)
        if size > 0:
            index = random.randint(0, size - 1)
            downloadaditem = download_ads[index]
            result[x_data] = downloadaditem.downloaddict()
            result[x_code] = 200
        else:
            result[x_code] = 201
            result[x_meesage] = 'nodata'

    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()
    return json.dumps(result)




@api3.route('/app/promote')
def helpownload():
    result = {}

    platvalue = request.args.get("plat","1")
    channelvalue =  request.args.get("channel","0")
    appversion = request.args.get("appversion","3.0")
    source = request.args.get("source","fish")



    try:
        # download_ads= db.session.query(downloadAd).filter_by(plat=platvalue,status=1,channel =channelvalue).order_by(
        #     downloadAd.index).all()

        # size = len(download_ads)
        if source == "solunar"  and (appversion.startswith("2") or appversion.startswith("1")):
            dict = {}
            dict["haha"] = "hh"

            result[x_data] =  dict
            result[x_code] = 200
        else:
            result[x_code] = 201
            result[x_meesage] = 'nodata'

    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()

    finally:
        db.session.close()
    return json.dumps(result)


@api3.route("/help/promote/click")
def helpdownloadclick():

    app = request.args.get("source","unkown")
    adId = request.args.get("adId","100")
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    try:
        downloadclick =  downloadAdClick(day=nowTimeSting,adId=adId,app=app)
        db.session.add(downloadclick)
        db.session.commit()

    except Exception as e:
        db.session.rollback()

    finally:
        db.session.close()

    dict  = {}



    dict[x_meesage] = "nothing"
    dict[x_code] = 201

    return json.dumps(dict)


@api3.route("/app/promote/click")
def adddownloadclick():

    app = request.args.get("source","unkown")
    adId = request.args.get("adId","100")
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    try:
        downloadclick =  downloadAdClick(day=nowTimeSting,adId=adId,app=app)
        db.session.add(downloadclick)
        db.session.commit()

    except Exception as e:
        db.session.rollback()

    finally:
        db.session.close()

    dict  = {}



    dict[x_meesage] = "nothing"
    dict[x_code] = 201

    return json.dumps(dict)


@api3.route("/app/download/static")
def adddownloadstatic():

    result = {}
    list =[]

    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    day = request.args.get("day",nowTimeSting)

    try:
        download_adclicks = db.session.query(downloadAdClick).filter_by(day=day).all()
        for clickitem in download_adclicks:
            dict = clickitem.downloadclickdict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list
        result["count"] = len(download_adclicks)

    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        db.session.rollback()

    finally:
        db.session.close()



    return json.dumps(result)


@api3.route('/xunquan/column')
def xunquancolumn():
    result = {}
    bannnerList = []
    itemlist = []
    datadict = {}
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    try:
        bannerresult = db.session.query(banner).filter(banner.endTime > nowTime).filter_by(plat=0).order_by(
            banner.index).all()

        for banneritem in bannerresult:
            bannerdict = banneritem.promotiondict()
            bannnerList.append(bannerdict)
    except:
        db.session.rollback()


    try:

        columnresult = db.session.query(column).filter_by(plat=1).order_by(
            column.index).all()

        for columnitem in columnresult:
            columndict = columnitem.columndict()
            itemlist.append(columndict)
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()

    if  len(bannnerList) or len(itemlist):
        result[x_code] = 200
        datadict['itemList'] = itemlist
        datadict['bannerList'] = bannnerList
        result[x_data]  =datadict
    else:
        result[x_code] = 201

        result[x_meesage] = 'no data'

    return json.dumps(result)






@api3.route('/xunquan/welfare')
def xunquanwelfareget():
    result = {}
    list = []
    try:
        welfarereslut = db.session.query(welfare).filter_by(status=1).all()
        for welfareitem in welfarereslut:
            welfaredict = welfareitem.welfareDict()
            list.append(welfaredict)
        if(len(list)):
            result[x_data] = list
            result[x_code] = 200
        else:
            result[x_code] =201
            result[x_meesage]= 'no message'

    except  Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 203

    finally:
        db.session.close()
    return json.dumps(result)

@api3.route('/lunitidalsite')
def getlunitidalsite():
    result = {}
    list = []
    try:
        sitereslut = db.session.query(lunitidalsite).filter_by(status=1).order_by(lunitidalsite.index).all()
        for siteitem in sitereslut:
            sitedict = siteitem.lunitidalsiteDict()
            list.append(sitedict)
        if (len(list)):
            result[x_data] = list
            result[x_code] = 200
        else:
            result[x_code] = 201
            result[x_meesage] = 'no message'

    except  Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 203

    finally:
        db.session.close()
    return json.dumps(result)



@api3.route('/setwelfare', methods=['POST'])
def setwelfare():
    result = {}

    status = request.form.get('status', '0')
    url = request.form.get('url')
    typestr = request.form.get('type', '1')
    typeint = int(typestr)
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    welfareUrlStr = 'https://www.xunquan.shop/welfare?day=' + nowTimeSting + '&type=' + typestr

    try:
        welfarereslut = welfare.query.filter_by(type=typeint)[0]
        try:
            welfarereslut.welfareUrl = welfareUrlStr
            welfarereslut.activeUrl = url
            welfarereslut.status = int(status)
            db.session.commit()
            result[x_code] = 200

        except Exception as e:
            db.session.rollback()
            result[x_code] = 201
    except  Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 203

    finally:
        db.session.close()
    return json.dumps(result)


@api3.route("/app/items")
def appitems():
    result = {}
    list = []
    plat  = request.args.get("plat",0)

    source = request.args.get("source", "xunquan")
    if source == "solunar":
        plat = 4
    # result[x_code] = 201
    # result[x_meesage] = "no way"
    # return json.dumps(result)

    try:
        items  = db.session.query(appitem).filter_by(plat =plat).order_by(appitem.index).all()
        for item in items:
            itemdict = item.appitemDict()
            list.append(itemdict)
        result[x_code] = 200
        result[x_data] = list


    except  Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 203
    finally:
        db.session.close()

    return json.dumps(result)



@api3.route("/sale/config")
def getsaleconfig():
    result = {}


    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")

    is_vip =  request.args.get("isvip","1")

    source = request.args.get("source", "fishing")

    if is_vip == 1:
        result[x_code] = 201
        result[x_meesage] = "nodata"
        return json.dumps(result)

    try:
        saleresult = db.session.query(saleconfig).filter(saleconfig.endTime > nowTime,saleconfig.status >0).filter_by(source=source).all()
        if len(saleresult)>0:
            saleconfig0 = saleresult[0]
            result[x_code] = 200
            result[x_data] = saleconfig0.saleconfigdict()
        else:
            result[x_code] = 201
            result[x_meesage] = "nodata"


    except Exception as e:
        result[x_meesage] = "%s" % e
        result[x_code] = 201
        db.session.rollback()

    return json.dumps(result)


@api3.route("/7timerinfo/image")
def timerinfoimage():
    lat = request.args.get("lat","30")
    lon  = request.args.get("lon","120")
    lang = request.args.get("lang","zh-CN")
    unit = request.args.get("unit","metric")
    ac = request.args.get("ac","0")
    tzshift = request.args.get("tzshift","0")
    time = request.args.get("time","1000")

    result = {}
    result[x_code] = 200

    #167.99.8.254
    url = "https://www.7timer.info/bin/astro.php?lon="+lon+"&lat=" + lat +"&lang=" + lang + "&ac="+ ac + "&unit="+ unit +"&tzshift=" + tzshift +"&t=" + time

    result[x_data] = url

    return json.dumps(result)









