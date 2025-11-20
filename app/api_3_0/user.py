#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage
from flask import request
from app import db


import time
import datetime

import json

import math
from app.utils.constvalue import aliyun_euler_accesskey,aliyun_euler_secret
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from app.VipUser import VipUser
import random

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models

from app.SMSCode import SMSCode



# sms_client = AcsClient(aliyun_accesskey, aliyun_secret, 'cn-hangzhou')


sms_client_2 = AcsClient(aliyun_euler_accesskey, aliyun_euler_secret, 'cn-hangzhou')


def create_client() -> Dysmsapi20170525Client:
    """
    使用AK&SK初始化账号Client
    @return: Client
    @throws Exception
    """
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
    # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
    config = open_api_models.Config(
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
        access_key_id=aliyun_euler_accesskey,
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
        access_key_secret=aliyun_euler_secret
    )
    # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
    config.endpoint = f'dysmsapi.aliyuncs.com'
    return Dysmsapi20170525Client(config)


# @api3.route("/user/requestcode/v2")
# def requestcodev2new():
#     client = create_client()
#     app = request.args.get('app',"fish")
#     phone = request.args.get("phone","19805815923")
#
#
#     lat = request.args.get('lat', '37.513')
#     lng = request.args.get('lng', '122.12')
#     timestamp = request.args.get('time', '1705466471')
#     total = request.args.get('total', '1599918717')
#
#     sms_code = random.randint(1000,9999)
#
#     code = userchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
#     result = {}
#     SignName = "杭州欧拉公式科技"
#     # if app == "fish":
#     #     SignName = "钓鱼天气"
#     # elif app == "tide":
#     #     SignName = "月相潮汐表"
#     # elif app == "solunar":
#     #    SignName =  "日出日落月相"
#
#     dict = {"code": str(sms_code)}
#
#
#     batch_send_message_request = dysmsapi_20170525_models.SendSmsRequest(
#         phone_numbers=phone,
#         sign_name=SignName,
#         template_code="SMS_232161590",
#         template_param=json.dumps(dict)
#     )
#     try:
#         # 复制代码运行请自行打印 API 的返回值
#         client.send_sms_with_options(batch_send_message_request,util_models.RuntimeOptions())
#         result[x_code] = 200
#         result[x_meesage] = "发送成功"
#         dict = {}
#         dict["sms_code"] = sms_code
#         result[x_data] = dict
#     except Exception as error:
#         # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
#         # 错误 message
#         print(error)
#         result[x_code] = 201
#         result[x_meesage] = "%s"%error
#         # 诊断地址
#
#     return json.dumps(result)





@api3.route("/user/requestcode/v2")
def requsetzcodev2():
    app = request.args.get('app',"fish")
    phone = request.args.get("phone","15167140620")

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1705466471')
    total = request.args.get('total', '1599918717')

    sms_code = random.randint(1000,9999)

    code = userchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    result = {}
    if 200 == code:
        pass
    elif 201 == code:
        result[x_meesage] = "发送成功"
        dict = {}
        dict["sms_code"] = sms_code

        return json.dumps(result)
    elif 202 == code:
        result[x_meesage] = "发送成功"
        dict = {}
        dict["sms_code"] = sms_code
        return json.dumps(result)

    # time.sleep(10)
    # result[x_code] = 200
    # dict = {}
    # dict["sms_code"] = sms_code
    # result[x_data] = dict
    # return json.dumps(result)



    s_request = CommonRequest()
    s_request.set_accept_format('json')
    s_request.set_domain('dysmsapi.aliyuncs.com')
    s_request.set_method('POST')
    s_request.set_protocol_type('https')  # https | http
    s_request.set_version('2017-05-25')
    s_request.set_action_name('SendSms')

    s_request.add_query_param('RegionId', "cn-hangzhou")
    s_request.add_query_param('PhoneNumbers', phone)
    s_request.add_query_param('SignName', "杭州欧拉公式科技")
    if app == "fish":
        s_request.add_query_param('SignName', "钓鱼天气")
    elif app == "tide":
        s_request.add_query_param('SignName', "月相潮汐表")
    elif app == "solunar":
        s_request.add_query_param('SignName', "日出日落月相")
        # writesmscode(phone=phone, code=str(sms_code), app=timestamp)

    s_request.add_query_param('TemplateCode', "SMS_232161590")


    dict = {"code":str(sms_code)}


    s_request.add_query_param('TemplateParam', json.dumps(dict))





    try:
        response = sms_client_2.do_action_with_exception(s_request)

        result[x_code] =200
        result[x_meesage] = "发送成功"
        dict = {}
        dict["sms_code"] = sms_code
        result[x_data] = dict
    except Exception as e:
        writesmscode(phone=phone, code=str(sms_code), app=timestamp)
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)




@api3.route("/user/requestcode")
def requsetzcode():
    app = request.args.get('app',"fish")
    phone = request.args.get("phone","15167140620")

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time')
    total = request.args.get('total', '1599918717')

    if timestamp is None:
        local_time = int(time.time())
        timestamp =  str(local_time)


    # code = userchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    result = {}
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)

    sms_code = random.randint(1000,9999)
    timestamp_i = int(timestamp)
    local_i = int(time.time())
    deta = abs(timestamp_i - local_i)

    if deta > 360 :

        result[x_code] = 200
        dict = {}
        result[x_meesage] = "发送成功1"
        dict["sms_code"] = sms_code
        result[x_data] = dict
        return json.dumps(result)

    s_request = CommonRequest()
    s_request.set_accept_format('json')
    s_request.set_domain('dysmsapi.aliyuncs.com')
    s_request.set_method('POST')
    s_request.set_protocol_type('https')  # https | http
    s_request.set_version('2017-05-25')
    s_request.set_action_name('SendSms')

    s_request.add_query_param('RegionId', "cn-hangzhou")
    s_request.add_query_param('PhoneNumbers', phone)
    if app == "fish":
        s_request.add_query_param('SignName', "钓鱼天气")
    elif app == "tide":
        s_request.add_query_param('SignName', "月相潮汐表")
    elif app == "solunar":
        s_request.add_query_param('SignName', "日出日落月相")

    s_request.add_query_param('TemplateCode', "SMS_232161590")


    dict = {"code":str(sms_code)}


    s_request.add_query_param('TemplateParam', json.dumps(dict))



    try:
        response = sms_client_2.do_action_with_exception(s_request)
        result[x_code] =200
        result[x_meesage] = "发送成功"
        dict = {}
        dict["sms_code"] = sms_code
        result[x_data] = dict
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)


@api3.route("/user/eluer/requestcode")
def eluerrequsetzcode():
    app = request.args.get('app', "astronomy")
    phone = request.args.get("phone", "15167140620")

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    sms_code = random.randint(1000, 9999)

    code = userchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    result = {}
    if 200 == code:
        pass
    elif 201 == code:
        result[x_meesage] = "发送成功"
        dict = {}
        dict["sms_code"] = sms_code
        result[x_data] = dict
        return json.dumps(result)
    elif 202 == code:
        if app == "meteo":
            pass
        else:
            result[x_meesage] = "发送成功"
            dict = {}
            dict["sms_code"] = sms_code
            result[x_data] = dict
            return json.dumps(result)

    s_request = CommonRequest()
    s_request.set_accept_format('json')
    s_request.set_domain('dysmsapi.aliyuncs.com')
    s_request.set_method('POST')
    s_request.set_protocol_type('https')  # https | http
    s_request.set_version('2017-05-25')
    s_request.set_action_name('SendSms')

    s_request.add_query_param('RegionId', "cn-hangzhou")
    s_request.add_query_param('PhoneNumbers', phone)
    s_request.add_query_param('SignName', "杭州欧拉公式科技")
    if app == "fish":
        s_request.add_query_param('SignName', "钓鱼天气")
    elif app == "tide":
        s_request.add_query_param('SignName', "月相潮汐表")
    elif app == "solunar":
        s_request.add_query_param('SignName', "日出日落月相")
    elif app == "astronomy":
        s_request.add_query_param('SignName', "天文观星指南")

    elif app == "meteo":
        s_request.add_query_param('SignName', "气象计算")
    # else:
    #      s_request.add_query_param('SignName', "杭州欧拉公式科技")

    s_request.add_query_param('TemplateCode', "SMS_232161590")


    dict = {"code": str(sms_code)}

    s_request.add_query_param('TemplateParam', json.dumps(dict))



    try:
        response = sms_client_2.do_action_with_exception(s_request)
        result[x_code] = 200
        result[x_meesage] = "发送成功"
        dict = {}
        dict["sms_code"] = sms_code
        result[x_data] = dict
    except Exception as e:
        writesmscode(phone=phone, code=str(sms_code), app=timestamp)
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)



@api3.route("/user/verifycode/login")
def verifycodelogin():
    app = request.args.get('app')
    phone = request.args.get("phone")


    usercode = request.args.get("usercode")
    code = request.args.get("code")
    result  ={}
    if code == usercode:
        pass
    else:
        result[x_code] = 202
        result[x_meesage] = "验证码错误"
        return json.dumps(result)

    try:
        phone = phone[:11]
    except:
        result[x_code] = 202
        result[x_meesage] = "手机号码错误"
        return json.dumps(result)

    phoneapp = phone + app

    try:
        users = db.session.query(VipUser).filter(VipUser.PhoneNumberApp==phoneapp).all()
        if len(users) > 0:
            userobject = users[0]
            result[x_code] = 200
            result[x_meesage] = "登陆成功"
            result[x_data] = userobject.vipDict()
        else:
            newuser = VipUser(Phone=phone,App= app)
            db.session.add(newuser)
            db.session.commit()
            result[x_code] = 200
            result[x_meesage] = "登陆成功"
            result[x_data] = newuser.vipDict()



    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)





@api3.route("/user/password/longin")
def passwordlogin():
    app = request.args.get('app')
    phone = request.args.get("phone")
    phoneapp = phone+app
    result = {}
    password = request.args.get("password")
    try:
        users = db.session.query(VipUser).filter(VipUser.PhoneNumberApp == phoneapp).all()
        if len(users) >0:
            userobeject = users[0]
            dbpassword = userobeject.password
            if password == dbpassword:
                result[x_code] = 200
                result[x_meesage] = "登陆成功"
                result[x_data] = userobeject.vipDict()
            else:
                result[x_code]  =203
                result[x_meesage] = "密码错误或未设置密码"
        else:
            result[x_code] = 202
            result[x_meesage]  ="用户未注册"

    except Exception as e:
        db.session.rollback()
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)


@api3.route("/user/setpassword")
def setpassword():
    app = request.args.get('app')
    phone = request.args.get("phone")
    phoneapp = phone + app
    password = request.args.get("password")
    result = {}
    try:
        phoneapp = db.session.query(VipUser).filter(VipUser.PhoneNumberApp == phoneapp)[0]
        phoneapp.password =  password
        db.session.commit()
        result[x_code] = 200
        dict = {}
        result[x_data]  = dict
        result[x_meesage] ="密码设置成功"


    except Exception as e:
        db.session.rollback()
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)




@api3.route("/user/userinfo")
def userinfo():
    app = request.args.get('source')

    if app ==  "solunar":
        pass
    else:
        app  =request.args.get("app")


    phone = request.args.get("phone")
    phoneapp = phone + app
    result = {}
    try:
        users = db.session.query(VipUser).filter(VipUser.PhoneNumberApp == phoneapp).all()
        if len(users) > 0:
            userobeject = users[0]
            result[x_code] = 200
            result[x_data] = userobeject.vipDict()

        else:
            result[x_code] = 202
            result[x_meesage] = "用户未注册"

    except Exception as  e:

        db.session.rollback()
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return json.dumps(result)



@api3.route("/user/buyvip")
def buyvip():
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    app = request.args.get('app')
    phone = request.args.get("phone")
    phoneapp = phone + app
    viptype = request.args.get("type","5")

    result  = {}

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    # code = userchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)

    try:
        phoneapp = db.session.query(VipUser).filter(VipUser.PhoneNumberApp==phoneapp)[0]
        if phoneapp.type == "0":
            phoneapp.startdate  = nowTime
            db.session.commit()
        elif phoneapp.type == "1":
            oldstardate = phoneapp.startdate
            newstardate = oldstardate + datetime.timedelta(days=366)
            phoneapp.startdate = newstardate
            db.session.commit()
        result[x_code] = 200
        result[x_meesage] = "购买成功"

    except Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)



@api3.route("/user/resetvip")
def resetvip():
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")
    app = request.args.get('app')
    phone = request.args.get("phone")
    phoneapp = phone + app
    viptype = int(request.args.get("type","5"))

    result  = {}

    lat = request.args.get('lat', '37.513')
    lng = request.args.get('lng', '122.12')
    timestamp = request.args.get('time', '1550069439')
    total = request.args.get('total', '1599918717')

    # code = userchecklatandlon(lat=lat, lng=lng, timestamp=timestamp, total=total)
    # if 200 == code:
    #     pass
    # elif 201 == code:
    #     result[x_code] = 201
    #     result[x_meesage] = "time out ,no data"
    #     return json.dumps(result)
    # elif 202 == code:
    #     result[x_code] = 202
    #     result[x_meesage] = "error,no data!"
    #     return json.dumps(result)

    try:
        phoneuser = db.session.query(VipUser).filter(VipUser.PhoneNumberApp==phoneapp)[0]
        if phoneuser.type == 0 or phoneuser.type > 2:
            phoneuser.startdate  = nowTime
            phoneuser.type = viptype
            phoneuser.isvip  = True
            db.session.commit()
        elif phoneuser.type == 1 :
            oldstardate = phoneapp.startdate
            newstardate = oldstardate + datetime.timedelta(days=366)
            phoneuser.startdate = newstardate
            phoneuser.type = viptype
            phoneuser.isvip = True
            db.session.commit()
        result[x_code] = 200
        result[x_meesage] = "购买成功"

    except Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)

@api3.route("/user/delete")
def userdelete():
    app = request.args.get('app',"fish")
    phone = request.args.get("phone","15167140620")
    phoneapp = phone + app
    result = {}
    try:
        phoneappobject = db.session.query(VipUser).filter(VipUser.PhoneNumberApp == phoneapp)[0]
        try:
            db.session.delete(phoneappobject)
            db.session.commit()
            result[x_code] = 200
            result[x_meesage] = "注销成功"
        except Exception as e:
            result[x_meesage] = "%s"%e
            result[x_code] = 201
            db.session.rollback()

    except Exception as  e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 201
    return json.dumps(result)


@api3.route("/user/viptodday")
def viptoday():
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))


    result  = {}

    list = []

    try:
        vips= db.session.query(VipUser).filter(VipUser.isvip == True,VipUser.startdate ==nowTimeSting).all()

        for vipobject in vips:
            dict = vipobject.vipDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)


@api3.route("/user/registertodday")
def registertoday():
    nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))


    result  = {}

    list = []

    try:
        vips= db.session.query(VipUser).filter(VipUser.registerdate =="2025-03-04").all()

        for vipobject in vips:
            dict = vipobject.vipDict()
            list.append(dict)

        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage] = "%s"%e
        result[x_code] = 201

    return json.dumps(result)


def writesmscode(phone,code,app):

    try:
        smscode = SMSCode(phone=phone,code=code,app=app)
        db.session.add(smscode)
        db.session.commit()

    except Exception as e:
        db.session.rollback()

@api3.route("/smscode/fetch")
def fetchsmsunsendcode():
    result = {}
    try:
        codes = db.session.query(SMSCode).filter(SMSCode.status == 0).all()
        list = []
        for smscode in codes:
            try:
                smscode.status = 1
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            list.append(smscode.codedict())
        result[x_code] = 200
        result[x_data] = list


    except Exception as e:
        db.session.rollback()
        result[x_code] = 201
        result[x_meesage] = "%s"%e

    return  json.dumps(result)





def userchecklatandlon(lat,lng,timestamp,total):
    latng_i = int(float(lat) * 100 * float(lng) * 100)
    timestamp_i = int(timestamp)
    local_i = int(time.time())
    deta = abs(timestamp_i - local_i)
    if deta > 360:
        return 201
    e = 2.71828
    pi = 3.14159
    c = 0.68619
    lat_fs = abs(float(lat))
    lng_fs = abs(float(lng))
    he = math.pow(lat_fs, e) + math.pow(lng_fs, pi)
    he_in = int(he)
    token_i = int(total)
    t_i = int(math.pow(timestamp_i, c))

    if abs(t_i + latng_i + he_in - token_i) < 1000:
        return 200
    else:
        return 202







