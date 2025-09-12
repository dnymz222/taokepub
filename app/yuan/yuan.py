# coding=utf8
from . import yxx
from flask import Flask, redirect, render_template, request, url_for, session, escape
import xlrd
import os
import json
from config import basedir
# from coupon import coupon
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.yuanorder import yuanorder
import urllib
import datetime
import time
import logging
import sys
import random


from werkzeug.utils import secure_filename
from config import basedir
import base64
from app.utils.constvalue import yxx_appkey, yxx_secret,yxx_siteid, x_code, x_meesage, x_data, appkey, secret, site_id, adzone_id, \
    yxx_adzonid

import re
from app.YuanCustomer import YuanCustomer
import hashlib
from hashlib import md5
import base64




@yxx.route('/list')
def yuanlist():
    page = int(request.args.get('page', '1'))
    orderpagi = db.session.query(yuanorder).order_by(yuanorder.onTime.desc()).paginate(page=int(page), per_page=100)
    orderlist = orderpagi.items
    db.session.close()

    return render_template('yuanlist.html', orderlist=orderlist)

@yxx.route('/customer/list')
def yuancustomerlist():
    page = int(request.args.get('page', '1'))
    result = {}
    try:
        orderpagi = db.session.query(YuanCustomer).order_by(YuanCustomer.index.desc()).paginate(page=int(page), per_page=100)
        orderlist = orderpagi.items
        list=[]
        for customeobject  in orderlist:
            dict = customeobject.YuanCustomerDict()
            list.append(dict)

        result[x_code]   =200

        result[x_data] =  list


    except Exception as e:
        result[x_code]  =201
        result[x_meesage] = "%s"%e

    finally:
        db.session.close()

    return json.dumps(result)



@yxx.route('/search')
def search():
    q = request.args.get('q')

    # q = q.decode('utf8')
    # print(q)

    page = int(request.args.get('page', '1'))
    orders = db.session.query(yuanorder).filter_by(name=q).order_by(yuanorder.onTime.desc()).paginate(page=int(page),
                                                                                                      per_page=100)
    orderlist = orders.items
    db.session.close()

    return render_template('yuansearch.html', orderlist=orderlist)


@yxx.route('/customer/search')
def customersearch():
    page = int(request.args.get('page', '1'))
    q = request.args.get('q')

    # q = q.decode('utf8')
    # print(q)
    result = {}

    list = []


    try:
        orderpagi = db.session.query(YuanCustomer).filter(YuanCustomer.note.like("%"+q+"%")|YuanCustomer.wechat_name.like("%"+q+"%")|YuanCustomer.shop_name.like("%"+q+"%")|YuanCustomer.company_name.like("%"+q+"%")|YuanCustomer.wangwang_num.like("%"+q+"%")|YuanCustomer.wechat_number.like("%"+q+"%")).order_by(YuanCustomer.index.desc()).paginate(page=int(page), per_page=100)
        orderlist = orderpagi.items
        list=[]
        for customeobject  in orderlist:
            dict = customeobject.YuanCustomerDict()
            list.append(dict)



        result[x_code]   =200

        result[x_data] =  list


    except Exception as e:
        result[x_code]  =201
        result[x_meesage] = "%s" % e

    finally:
        db.session.close()

    return json.dumps(result)



    return render_template('yuansearch.html', orderlist=orderlist)


@yxx.route('/customer/action')
def customeraction():
    action = request.args.get('action') #1.添加，2.修改 3.删除

    index = request.args.get("index")
    date = request.args.get("date","")
    wechat_name = request.args.get("wechat_name","")
    wechat_special = request.args.get("wechat_number","")
    wangwang_num = request.args.get("wangwang_num","")
    wechat_number = request.args.get("wechat_number","")
    company_name = request.args.get("company_name","")
    shop_name = request.args.get("shop_name","")
    detect_company = request.args.get("detect_company","")
    note  = request.args.get("note","")
    from_excel =  request.args.get("from_excel",0)

    result = {}

    if action == "1":

        dict = {}
        dict["index"] = index
        dict['date'] = date
        dict["wechat_name"] = wechat_name
        dict["wechat_number"] = wechat_number
        dict["wechat_special"] = wechat_special
        dict["wangwang_num"] = wangwang_num
        dict["company_name"] = company_name
        dict["shop_name"] = shop_name
        dict["detect_company"] = detect_company
        dict["note"] = note
        dict["from_excel"] =  from_excel



        try:
            yuancustomerobeject = YuanCustomer(dict=dict)
            db.session.add(yuancustomerobeject)
            db.session.commit()

            result[x_code] = 200
            result[x_data] = "ok"
        except Exception as e:
            result[x_code] = 201
            result[x_meesage] = "%s"%e


    elif action == "2":

        dict = {}

        dict['date'] = date
        dict["wechat_name"] = wechat_name
        dict["wechat_number"] = wechat_number
        dict["wechat_special"] = wechat_special
        dict["wangwang_num"] = wangwang_num
        dict["company_name"] = company_name
        dict["shop_name"] = shop_name
        dict["detect_company"] = detect_company
        dict["note"] = note
        dict["from_excel"] = from_excel

        try:
            db.session.query(YuanCustomer).filter_by(index=index).update(dict)
            db.session.commit()
            result[x_code] = 200
            result[x_data] = "ok"

        except Exception as e:
            result[x_code] = 201
            result[x_meesage] = "%s" % e

            db.session.rollback()

    else:
        try:
            db.session.query(YuanCustomer).filter_by(index=index).delete()
            db.session.commit()
            result[x_code] = 200
            result[x_data] = "ok"
        except Exception as e:
            result[x_code] = 201
            result[x_meesage] = "%s" % e
            db.session.rollback()


    db.session.close()
    return json.dumps(result)






@yxx.route('/upload', methods=['POST', 'GET'])
def yuanupload():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        session['filename'] = secure_filename(f.filename)
        return redirect(url_for('yxx.yuanread'))
    return '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@yxx.route('/customer/upload', methods=['POST', 'GET'])
def yuancustomupload():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        session['filename'] = secure_filename(f.filename)
        return redirect(url_for('yxx.yuancustomerread'))
    return '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''


@yxx.route('/read')
def yuanread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")
        nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
        for sheet in bk.sheets():
            sheet_name = sheet.name
            nrows = sheet.nrows
            for i in range(1, nrows):
                dict = {}
                row_value = sheet.row_values(i)


                # dict['sheet'] = sheet_name
                # num = row_value[2]
                # if isinstance(num, str):
                #     numstr = num
                # elif isinstance(num, float):
                #     numstr = str(int(num))
                # else:
                #     numstr = str(num)
                #
                # numstr = numstr.strip()
                # name = row_value[1].strip()

                #
                # dict['nameNum'] = base64.encodestring(name).replace('\n', '') + numstr
                # dict['name'] = name
                # dict['num'] = numstr
                # dict['date'] = row_value[0]
                # dict['price'] = row_value[3]
                # dict['status'] = row_value[4]
                # dict['chatnum'] = row_value[5]
                # dict['goodsname'] = row_value[6]
                # dict['note'] = row_value[7]
                # dict['onTime'] = nowTime

                # insert = yuanorder(dict=dict)

                # try:
                #     db.session.add(insert)
                #     db.session.commit()
                # except:
                #     db.session.rollback()
                #     try:
                #         orderold = yuanorder.query.filter_by(nameNum=insert.nameNum)[0]
                #         if orderold:
                #             orderold.sheet = insert.sheet
                #             orderold.date = insert.date
                #             orderold.price = insert.price
                #             orderold.status = insert.status
                #             orderold.chatnum = insert.chatnum
                #             orderold.goodsname = insert.goodsname
                #             orderold.note = insert.note
                #             db.session.commit()
                #     except:
                #         db.session.rollback()
                # finally:
                #     db.session.flush()

            # session.clear()
            # db.session.close()

        os.remove(xlspath)
    return '读取成功'


@yxx.route('/customer/read')
def yuancustomerread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")
        nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")

        t = int( time.time())

        try:
            db.session.query(YuanCustomer).filter_by(from_excel =1).delete()
            db.session.commit()



        except Exception as e:
            db.session.rollback()






        for sheet in bk.sheets():

            nrows = sheet.nrows
            for i in range(1, nrows):
                dict = {}
                row_value = sheet.row_values(i)

                dict['date'] = str(row_value[0])
                dict["wechat_name"] = str( row_value[1])
                dict["wechat_number"] = str( row_value[2])
                dict["wechat_special"] = str( row_value[6])
                dict["wangwang_num"] =str( row_value[3])
                dict["company_name"] = str( row_value[4])
                dict["shop_name"] = str( row_value[5])
                dict["detect_company"] = str( row_value[7])
                dict["note"] = str( row_value[8])
                dict["from_excel"] = 1
                string =dict["date"]+"_"+ dict["wechat_number"]+"_"+ dict["wechat_name"]+"_"+dict["wangwang_num"]+"_"+dict["company_name"]+"_"+dict["note"]

                dict["index"] = computeMD5hash(string)




                # dict['sheet'] = sheet_name
                # num = row_value[2]
                # if isinstance(num, str):
                #     numstr = num
                # elif isinstance(num, float):
                #     numstr = str(int(num))
                # else:
                #     numstr = str(num)
                #
                # numstr = numstr.strip()
                # name = row_value[1].strip()

                #
                # dict['nameNum'] = base64.encodestring(name).replace('\n', '') + numstr
                # dict['name'] = name
                # dict['num'] = numstr
                # dict['date'] = row_value[0]
                # dict['price'] = row_value[3]
                # dict['status'] = row_value[4]
                # dict['chatnum'] = row_value[5]
                # dict['goodsname'] = row_value[6]
                # dict['note'] = row_value[7]
                # dict['onTime'] = nowTime

                insert = YuanCustomer(dict=dict)

                try:
                    db.session.add(insert)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()

                finally:
                    pass

            # session.clear()
            db.session.close()

        os.remove(xlspath)
    return '读取成功'


# @yxx.route('/search')
# def yuansearch():
#     pass






def computeMD5hash(string):

    m = hashlib.md5()
    m.update(memoryview(string))
    md5string=m.digest()
    return base64.encodestring(md5string).strip()
