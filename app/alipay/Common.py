#coding=utf8
from app.utils.constvalue import x_data,x_code,x_meesage


from . import alipay
import json
from flask import request,redirect,session,url_for
import time
import datetime
from app.VipUser import VipUser
from app import db


@alipay.route("/app/pay/notify",methods =["GET","POST"])
def apppaynotify():
    if request.method == "GET":
        out_trade_no = request.args.get("out_trade_no")
        trade_status = request.args.get("trade_status")
        trade_no = request.args.get("trade_no")
        out_trade_no = str(out_trade_no)
        # print ("trade_status:"+trade_status)
        phone = out_trade_no[:11]
        timestring = out_trade_no[11:19]
        type = out_trade_no[19:20]
        app = out_trade_no[20:]
        if app == "1":
            phoneapp = phone + "fish"
        elif app == "2":
            phoneapp  = phone + "tide"
        elif app == "3":
            phoneapp = phone + "solunar"
        elif app == "4":
            phoneapp = phone + "astronomy"
        elif app == "5":
            phoneapp = phone + "meteo"
        else:
            phoneapp = phone + "default"

        nowTime = datetime.datetime.strptime(timestring, "%Y%m%d")
        if trade_status == "TRADE_SUCCESS":
            try:
                phoneapp = db.session.query(VipUser).filter(VipUser.PhoneNumberApp==phoneapp)[0]
                phoneapp.isvip = True
                phoneapp.startdate = nowTime
                phoneapp.type = int(type)
                phoneapp.trade_no = trade_no
                db.session.commit()



            except Exception as e:
                db.session.rollback()

        else:
            pass
        return "done"
    else:
        out_trade_no = request.form["out_trade_no"]
        trade_status = request.form["trade_status"]
        trade_no = request.form["trade_no"]
        out_trade_no = str(out_trade_no)
        # print "trade_status:" + trade_status
        phone = out_trade_no[:11]
        timestring = out_trade_no[11:19]
        type = out_trade_no[19:20]
        app = out_trade_no[20:]
        if app == "1":
            phoneapp = phone + "fish"
        elif app == "2":
            phoneapp = phone + "tide"
        elif app == "3":
            phoneapp = phone + "solunar"
        elif app == "4":
            phoneapp = phone + "astronomy"
        elif app == "5":
            phoneapp = phone + "meteo"
        else:
            phoneapp = phone + "default"

        nowTime = datetime.datetime.strptime(timestring, "%Y%m%d")
        if trade_status == "TRADE_SUCCESS":
            try:
                phoneapp = db.session.query(VipUser).filter(VipUser.PhoneNumberApp == phoneapp)[0]

                phoneapp.isvip = True
                phoneapp.startdate = nowTime
                phoneapp.type = int(type)
                phoneapp.trade_no = trade_no
                db.session.commit()


            except Exception as e:
                db.session.rollback()

        else:
            pass
        return "done"



@alipay.route("/app/pay/notify/v2",methods =["GET","POST"])
def apppaynotify_v2():
    if request.method == "GET":
        out_trade_no = request.args.get("out_trade_no")
        trade_status = request.args.get("trade_status")
        trade_no = request.args.get("trade_no")
        out_trade_no = str(out_trade_no)
        # print ("trade_status:"+trade_status)
        phone = out_trade_no[:11]
        timestring = out_trade_no[11:19]
        type = out_trade_no[19:20]
        app = out_trade_no[20:]
        if app == "1":
            phoneapp = phone + "fish"
        elif app == "2":
            phoneapp  = phone + "tide"
        elif app == "3":
            phoneapp = phone + "solunar"
        elif app == "4":
            phoneapp = phone + "astronomy"
        elif app == "5":
            phoneapp = phone + "meteo"
        else:
            phoneapp = phone + "default"

        nowTime = datetime.datetime.strptime(timestring, "%Y%m%d")
        if trade_status == "TRADE_SUCCESS":
            try:
                phoneapp = db.session.query(VipUser).filter(VipUser.PhoneNumberApp==phoneapp)[0]
                phoneapp.isvip = True
                phoneapp.startdate = nowTime
                phoneapp.type = int(type)
                phoneapp.trade_no = trade_no
                db.session.commit()



            except Exception as e:
                db.session.rollback()

        else:
            pass
        return "done"
    else:
        out_trade_no = request.form["out_trade_no"]
        trade_status = request.form["trade_status"]
        trade_no = request.form["trade_no"]
        out_trade_no = str(out_trade_no)
        # print "trade_status:" + trade_status
        phone = out_trade_no[:11]
        timestring = out_trade_no[11:19]
        type = out_trade_no[19:20]
        app = out_trade_no[20:]
        if app == "1":
            phoneapp = phone + "fish"
        elif app == "2":
            phoneapp = phone + "tide"
        elif app == "3":
            phoneapp = phone + "solunar"
        elif app == "4":
            phoneapp = phone + "astronomy"
        elif app == "5":
            phoneapp = phone + "meteo"
        else:
            phoneapp = phone + "default"

        nowTime = datetime.datetime.strptime(timestring, "%Y%m%d")
        if trade_status == "TRADE_SUCCESS":
            try:
                phoneapp = db.session.query(VipUser).filter(VipUser.PhoneNumberApp == phoneapp)[0]

                phoneapp.isvip = True
                phoneapp.startdate = nowTime
                phoneapp.type = int(type)
                phoneapp.trade_no = trade_no
                db.session.commit()


            except Exception as e:
                db.session.rollback()

        else:
            pass
        return "done"

@alipay.route("/fish/pay/amount")
def fishpayamount():
    pass
