#coding=utf8
import logging
import traceback
from app.utils.constvalue import meteo_appid,meteo_app_publickey,meteo_app_secretkey,meteo_alipay_publickey
from app.utils.constvalue import x_data,x_code,x_meesage


from . import alipay
import json
from flask import request,redirect,session,url_for
import time
import datetime
from app.VipUser import VipUser
from app import db


from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse
import sys



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


meteo_alipay_client_config = AlipayClientConfig()
meteo_alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
meteo_alipay_client_config.app_id = meteo_appid
meteo_alipay_client_config.app_private_key = meteo_app_secretkey
meteo_alipay_client_config.alipay_public_key = meteo_alipay_publickey

meteo_client = DefaultAlipayClient(alipay_client_config=meteo_alipay_client_config, logger=logger)


@alipay.route("/meteo/pay")
def meteoopay():
    model = AlipayTradePayModel()
    model.out_trade_no = "20150320010101001";
    model.total_amount = "88.88";
    model.subject = "Iphone6 16G";
    model.buyer_id = "2088102177846880";


    request_ali = AlipayTradePayRequest(biz_model=model)
    # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
    # udf_params = dict()
    # from alipay.aop.api.constant.ParamConstants import *
    # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
    # request.udf_params = udf_params
    # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    response_content = None

    result = {}
    try:
        response_content = meteo_client.execute(request_ali)
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        print(traceback.format_exc())

    if not response_content:
        result[x_code] = 202
        result[x_meesage] = "failed execute"
        print("failed execute")

    else:
        response = AlipayTradePayResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        print(response.body)
        if response.is_success():
            # 如果业务成功，则通过respnse属性获取需要的值
            print("get response trade_no:" + response.trade_no)
            result[x_code] = 200
            dict ={}
            dict["trade_no"] = response.trade_no
            result[x_data] = dict
        else:
            # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
            result[x_meesage] = response.msg
            result[x_code] = response.code


    return json.dumps(result)




@alipay.route("/meteo/page/pay")
def meteo_page_pay():
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088301300153242"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = meteo_client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)


@alipay.route("/meteo/app/pay")
def meteo_app_pay():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "1")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202021031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")
    if  type == "1":
        model.total_amount = "36.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包年会员'
    elif type == "9":
        model.total_amount = "6.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包月会员'
    elif type == "3" :
        model.total_amount = "15.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算包季会员'
    else:
        model.total_amount = "98.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '气象计算会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = meteo_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)

@alipay.route("/meteo/app/pay/v2")
def meteo_app_pay_v2():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "1")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202021031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")
    if  type == "1":
        model.total_amount = "48.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包年会员'
    elif type == "9":
        model.total_amount = "12.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包月会员'
    elif type == "3" :
        model.total_amount = "20.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算包季会员'
    else:
        model.total_amount = "98.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '气象计算会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = meteo_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)


@alipay.route("/meteo/app/pay/v3")
def meteo_app_pay_v3():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "1")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202021031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")
    if  type == "1":
        model.total_amount = "48.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包年会员'
    elif type == "9":
        model.total_amount = "10.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包月会员'
    elif type == "3" :
        model.total_amount = "20.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算包季会员'
    else:
        model.total_amount = "98.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '气象计算会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = meteo_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)

@alipay.route("/meteo/app/pay/v4")
def meteo_app_pay_v4():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "1")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202021031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")
    if  type == "1":
        model.total_amount = "78.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包年会员'
    elif type == "9":
        model.total_amount = "12.00"
        if amount:
            model.total_amount = amount
        model.subject = '气象计算包月会员'
    elif type == "3" :
        model.total_amount = "30.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算包季会员'
    else:
        model.total_amount = "198.00"
        if amount:
            model.total_amount =amount
        model.subject = '气象计算终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '气象计算会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = meteo_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)