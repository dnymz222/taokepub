#coding=utf8
import logging
import traceback
from app.utils.constvalue import solunaralipay_publickey,soluar_app_secretkey,solunar_appid,fish_serverurl
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



# reload(sys)
# sys.setdefaultencoding('utf-8')

# if sys.getdefaultencoding() != 'gbk':
#     reload(sys)
#     sys.setdefaultencoding('gbk')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


solunar_alipay_client_config = AlipayClientConfig()
solunar_alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
solunar_alipay_client_config.app_id = solunar_appid
solunar_alipay_client_config.app_private_key =soluar_app_secretkey
solunar_alipay_client_config.alipay_public_key = solunaralipay_publickey

solunar_client = DefaultAlipayClient(alipay_client_config=solunar_alipay_client_config, logger=logger)


@alipay.route("/solunar/pay")
def soluanrpay():
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
        response_content = solunar_client.execute(request_ali)
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




@alipay.route("/solunar/page/pay")
def solunar_page_pay():
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
    response = solunar_client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)






@alipay.route("/solunar/app/pay")
def solunar_app_pay():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "3")
    amount  = request.args.get("amount")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    if  type == "1":
        model.total_amount = "12.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包年会员'
    else:
        model.total_amount = "40.00"
        if  amount:
            model.total_amount = amount
        model.subject = '日出日落月相终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '日出日落月相会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = solunar_client.sdk_execute(request_ali)


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

@alipay.route("/solunar/app/pay/v2")
def solunar_app_pay_v2():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "3")
    amount  = request.args.get("amount")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    if  type == "1":
        model.total_amount = "18.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包年会员'
    elif  type == "3":
        model.total_amount = "8.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包季会员'
    else:
        model.total_amount = "50.00"
        if  amount:
            model.total_amount = amount
        model.subject = '日出日落月相终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '日出日落月相会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = solunar_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  = 200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)


@alipay.route("/solunar/app/pay/v3")
def solunar_app_pay_v3():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "3")
    userType = request.args.get('userType', '0')
    amount  = request.args.get("amount")
    ordername = request.args.get("ordername","日出日落月相阳春三月特惠(终身会员)")

    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    if  type == "1":
        model.total_amount = "20.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包年会员'
    elif  type == "5":
        if userType == "0":
            model.subject = "日出日落月相月全食特惠终身会员"
            model.total_amount = "28.00"
        else:
            model.subject = "日出日落月相升级终身会员"
            model.total_amount = "28.00"
    else:
        model.total_amount = "48.00"
        if  amount:
            model.total_amount = amount
        model.subject = '日出日落月相终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '日出日落月相会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = solunar_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  = 200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)

@alipay.route("/solunar/app/pay/v4")
def solunar_app_pay_v4():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "3")
    userType = request.args.get('userType', '0')
    amount  = request.args.get("amount")
    ordername = request.args.get("ordername","日出日落月相阳春三月特惠(终身会员)")

    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    if  type == "1":
        model.total_amount = "20.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包年会员'
    elif type == "3":
        model.total_amount = "12.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包季会员'
    elif  type == "5":
        model.total_amount = "36.00"
        if amount:
            model.total_amount = amount
        if userType == "0":
            model.subject = "日出日落月相月全食特惠终身会员"
        else:
            model.subject = "日出日落月相升级终身会员"
    else:
        model.total_amount = "48.00"
        if  amount:
            model.total_amount = amount
        model.subject = '日出日落月相终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '日出日落月相会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = solunar_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  = 200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)

@alipay.route("/solunar/app/pay/v5")
def solunar_app_pay_v5():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "3")
    userType = request.args.get('userType', '0')
    amount  = request.args.get("amount")
    ordername = request.args.get("ordername","日出日落月相阳春三月特惠(终身会员)")

    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    if  type == "9":
        model.total_amount = "5.00"
        model.subject = '日出日落月相包月会员'
        if amount:
            model.total_amount =amount
    elif  type == "1":
        model.total_amount = "28.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包年会员'
    elif type == "3":
        model.total_amount = "12.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包季会员'
    elif  type == "5":
        model.total_amount = "36.00"
        if amount:
            model.total_amount = amount
        if userType == "0":
            model.subject = "日出日落月相开春特惠终身会员"
        else:
            model.subject = "日出日落月相升级终身会员"
    else:
        model.total_amount = "68.00"
        if  amount:
            model.total_amount = amount
        model.subject = '日出日落月相终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '日出日落月相会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = solunar_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  = 200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)


@alipay.route("/solunar/app/pay/v6")
def solunar_app_pay_v6():
    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "3")
    userType = request.args.get('userType', '0')
    amount  = request.args.get("amount")
    ordername = request.args.get("ordername","日出日落月相阳春三月特惠(终身会员)")

    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    if  type == "9":
        model.total_amount = "6.00"
        model.subject = '日出日落月相包月会员'
        if amount:
            model.total_amount =amount
    elif  type == "1":
        model.total_amount = "36.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包年会员'
    elif type == "3":
        model.total_amount = "18.00"
        if amount:
            model.total_amount = amount
        model.subject = '日出日落月相包季会员'
    elif  type == "5":
        model.total_amount = "48.00"
        if amount:
            model.total_amount = amount
        if userType == "0":
            model.subject = "日出日落月相五一特惠终身会员"
        else:
            model.subject = "日出日落月相升级终身会员"
    else:
        model.total_amount = "98.00"
        if  amount:
            model.total_amount = amount
        model.subject = '日出日落月相终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '日出日落月相会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = solunar_client.sdk_execute(request_ali)


    # print response
    #
    # return response

    # return response
    #

    result = {}
    result[x_code]  = 200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)


