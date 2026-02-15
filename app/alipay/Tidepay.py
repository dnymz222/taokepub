#coding=utf8
import logging
import traceback
from app.utils.constvalue import tide_alipay_publickey,tide_app_pulickey,tide_app_scretekey,tide_appid,tide_serverurl
from app.utils.constvalue import x_data,x_code,x_meesage
from . import alipay
import json
from flask import request,redirect,session,url_for
import time
import datetime
from app.VipUser import VipUser

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
tide_logger = logging.getLogger('')


tide_alipay_client_config = AlipayClientConfig()
tide_alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
tide_alipay_client_config.app_id = tide_appid
tide_alipay_client_config.app_private_key =tide_app_scretekey
tide_alipay_client_config.alipay_public_key = tide_alipay_publickey
tide_client = DefaultAlipayClient(alipay_client_config=tide_alipay_client_config, logger=tide_logger)


# @alipay.route("/tide/pay")
# def tidepay():
#     model = AlipayTradePayModel()
#     model.auth_code = "282877775259787048"
#     model.body = "Iphone6 16G"
#     goods_list = list()
#     goods1 = GoodsDetail()
#     goods1.goods_id = "apple-01"
#     goods1.goods_name = "ipad"
#     goods1.price = 10
#     goods1.quantity = 1
#     goods_list.append(goods1)
#     model.goods_detail = goods_list
#     model.operator_id = "yx_001"
#     model.out_trade_no = "20180510AB014"
#     model.product_code = "FACE_TO_FACE_PAYMENT"
#     model.scene = "bar_code"
#     model.store_id = ""
#     model.subject = "huabeitest"
#     model.timeout_express = "90m"
#     model.total_amount = 1
#     request = AlipayTradePayRequest(biz_model=model)
#     # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
#     # udf_params = dict()
#     # from alipay.aop.api.constant.ParamConstants import *
#     # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
#     # request.udf_params = udf_params
#     # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
#     response_content = None
#     try:
#         response_content = tide_client.execute(request)
#     except Exception as e:
#         print(traceback.format_exc())
#     if not response_content:
#         print("failed execute")
#     else:
#         response = AlipayTradePayResponse()
#         # 解析响应结果
#         response.parse_response_content(response_content)
#         print(response.body)
#         if response.is_success():
#             # 如果业务成功，则通过respnse属性获取需要的值
#             print("get response trade_no:" + response.trade_no)
#         else:
#             # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
#             print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
#
#
# @alipay.route("/tide/page/pay")
# def tide_page_pay():
#     model = AlipayTradePagePayModel()
#     model.out_trade_no = "pay201805020000226"
#     model.total_amount = 50
#     model.subject = "测试"
#     model.body = "支付宝测试"
#     model.product_code = "FAST_INSTANT_TRADE_PAY"
#     settle_detail_info = SettleDetailInfo()
#     settle_detail_info.amount = 50
#     settle_detail_info.trans_in_type = "userId"
#     settle_detail_info.trans_in = "2088302300165604"
#     settle_detail_infos = list()
#     settle_detail_infos.append(settle_detail_info)
#     settle_info = SettleInfo()
#     settle_info.settle_detail_infos = settle_detail_infos
#     model.settle_info = settle_info
#     sub_merchant = SubMerchant()
#     sub_merchant.merchant_id = "2088301300153242"
#     model.sub_merchant = sub_merchant
#     request = AlipayTradePagePayRequest(biz_model=model)
#     # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
#     response = tide_client.page_execute(request, http_method="GET")
#     print("alipay.trade.page.pay response:" + response)
#
#


@alipay.route("/tide/app/pay/v3")
def tide_app_pay_v3():

    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "2")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")

    if  type == "9":
        model.total_amount = "3.00"
        model.subject = '月相潮汐表包月会员'
    elif type == "3" :
        model.total_amount = "7.00"
        model.subject = '月相潮汐表包季会员'
        if amount:
            model.total_amount =amount
    elif type == "1":
        model.total_amount = "16.00"
        model.subject = '月相潮汐表包年会员'
        if amount:
            model.total_amount =amount
    elif type == "2":
        model.total_amount = "49.00"
        model.subject = '月相潮汐表终身会员'
        if amount:
            model.total_amount =amount

    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '月相潮汐表会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = tide_client.sdk_execute(request_ali)


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


@alipay.route("/tide/app/pay/v4")
def tide_app_pay_v4():

    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "2")
    type = str(type)
    userType = request.args.get('userType', '0')
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")

    if  type == "9":
        model.total_amount = "8.00"
        model.subject = '月相潮汐表包月会员'
    elif type == "3" :
        model.total_amount = "20.00"
        model.subject = '月相潮汐表包季会员'
        if amount:
            model.total_amount =amount
    elif type == "1":
        model.total_amount = "48.00"
        model.subject = '月相潮汐表包年会员'
        if amount:
            model.total_amount =amount
    elif type == "5":
        model.total_amount = "58.00"
        if amount:
            model.total_amount = amount
        if userType == "0":
            model.subject = "月相潮汐表端午特惠(终身会员)"
        else:
            model.subject = "月相潮汐表升级终身会员"
    elif type == "2":
        model.total_amount = "98.00"
        model.subject = '月相潮汐表终身会员'
        if amount:
            model.total_amount =amount

    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '月相潮汐表会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"

    response = tide_client.sdk_execute(request_ali)


    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)


@alipay.route("/tide/app/price")
def tide_app_pay_price():
    result = {}
    result[x_code] = 200
    dict = {}
    dict["1"] = "68.00"
    dict["2"] = "198.0"
    dict["3"] = "24.00"
    result[x_data] = dict
    return json.dumps(result)


@alipay.route("/tide/app/pay/price")
def tideapppayprice():
    result = {}
    list = []
    quater = {}
    quater["type"] = "3"
    quater["amount"] = "15.00"
    list.append(quater)
    year = {}
    year["type"] = "1"
    year["amount"] = "36.00"
    list.append(year)
    life = {}
    life["type"] = "2"
    life["amount"] = "98.00"
    list.append(life)
    result[x_code]= 200
    result[x_data] = list
    return json.dumps(result)


@alipay.route("/tide/app/pay/v5")
def tide_app_pay_v5():

    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "2")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")

    if  type == "9":
        model.total_amount = "6.00"
        model.subject = '月相潮汐表包月会员'
        if amount:
            model.total_amount =amount
    elif type == "3" :
        model.total_amount = "9.00"
        model.subject = '月相潮汐表包季会员'
        if amount:
            model.total_amount =amount
    elif type == "1":
        model.total_amount = "24.00"
        model.subject = '月相潮汐表包年会员'
        if amount:
            model.total_amount =amount
    elif type == "2":
        model.total_amount = "68.00"
        model.subject = '月相潮汐表终身会员'
        if amount:
            model.total_amount = amount

    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '月相潮汐表会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"

    response = tide_client.sdk_execute(request_ali)


    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)


@alipay.route("/tide/app/pay/v6")
def tide_app_pay_v6():

    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "2")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")

    if  type == "9":
        model.total_amount = "12.00"
        model.subject = '月相潮汐表包月会员'
        if amount:
            model.total_amount =amount
    elif type == "3" :
        model.total_amount = "30.00"
        model.subject = '月相潮汐表包季会员'
        if amount:
            model.total_amount =amount
    elif type == "1":
        model.total_amount = "78.00"
        model.subject = '月相潮汐表包年会员'
        if amount:
            model.total_amount =amount
    elif type == "5":
        model.total_amount = "98.00"
        if amount:
            model.total_amount = amount

        model.subject = "月相潮汐表新春特惠(终身会员)"

    elif type == "2":
        model.total_amount = "198.00"
        model.subject = '月相潮汐表终身会员'
        if amount:
            model.total_amount = amount

    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '月相潮汐表会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"

    response = tide_client.sdk_execute(request_ali)


    result = {}
    result[x_code]  =200
    dict = {}
    dict["trade_info"]  =response
    result[x_data]  = dict

    return json.dumps(result)




@alipay.route("/tide/app/pay/v2")
def tide_app_pay_v2():

    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "2")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)
    amount = request.args.get("amount")
    if  type == "9":
        model.total_amount = "3.00"
        if amount:
            model.total_amount =amount
        model.subject = '月相潮汐表包月会员'
    elif type == "3":
        model.total_amount = "6.00"
        if amount:
            model.total_amount =amount
        model.subject = '月相潮汐表包季会员'
    elif type == "1":
        model.total_amount = "15.00"
        if amount:
            model.total_amount =amount
        model.subject = '月相潮汐表包年会员'
    elif type == "2":
        model.total_amount = "45.00"
        if amount:
            model.total_amount =amount
        model.subject = '月相潮汐表终身会员'

    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '月相潮汐表会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = tide_client.sdk_execute(request_ali)


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




@alipay.route("/tide/app/pay")
def tide_app_pay():

    model = AlipayTradeAppPayModel()
    type = request.args.get("type", "2")
    type = str(type)
    out_trade_no = request.args.get("out_trade_no","151671406202020031011")
    out_trade_no = str(out_trade_no)

    if  type == "1":
        model.total_amount = "12.00"
        model.subject = '月相潮汐表包年会员'
    elif type == "2":
        model.total_amount = "30.00"
        model.subject = '月相潮汐表终身会员'
    elif type == "3":
        model.total_amount = "40.00"
        model.subject = '月相潮汐表终身会员'
    elif type == "4":
        model.total_amount = "300.00"
        model.subject = '月相潮汐表终身会员'

    elif type == "5":
        model.total_amount = "720"
        model.subject = "月相潮汐表终身会员"
    elif type == "6":
        model.total_amount = "800"
        model.subject = "月相潮汐表终身会员"
    elif type =="7":
        model.total_amount = "820"
        model.subject = "月相潮汐表终身会员"
    elif type =="8":
        model.total_amount = "1600"
        model.subject = "月相潮汐表终身会员"

    else:
        model.total_amount = "40.00"
        model.subject = '月相潮汐表终身会员'
    model.seller_id = "2088131645470041"
    model.timeout_express = "90m"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = '月相潮汐表会员'

    model.out_trade_no = out_trade_no
    request_ali = AlipayTradeAppPayRequest(biz_model=model)
    request_ali.notify_url = "https://www.oulagongshi.com/api/v3.0/alipay/app/pay/notify"


    response = tide_client.sdk_execute(request_ali)


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