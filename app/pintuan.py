#coding=utf8
from app import create_app
import os
from app import db
import datetime


class pintuan:



    @classmethod
    def juconvertdict(cls,judict):
        dict = {}
        dict['clickUrl'] =judict['wap_url']
        dict['image'] = 'https:'+judict['pic_url_for_w_l']+'_250x250'
        dict['taobaoId'] = judict['item_id']
        dict['title'] = judict['title']
        dict['oriPrice'] = judict['orig_price']
        dict['finalPrice'] = judict['act_price']
        dict['startTime'] = judict['online_start_time']
        dict['online_end_time'] = judict['online_end_time']
        dict['usp_desc_list'] = judict['usp_desc_list']
        dict['item_usp_list'] = judict['item_usp_list']
        dict['price_usp_list']= judict['price_usp_list']
        dict['cate'] = judict['category_name']
        dict['cateId'] = judict['tb_first_cat_id']
        return dict

    # @classmethod
    # def pintuanmaterialdictApi(cls, taodict):
    #     dict = {}
    #     # dict['cateId'] = taodict['category']
    #     dict['clickUrl'] = "https:" + taodict['click_url']
    #     # couponinfo = taodict['coupon_info']
    #     dict['couponDenomination'] = taodict['coupon_amount']
    #     dict['shopName'] = taodict['item_description']
    #     # dict['sellerId'] = taodict['seller_id']
    #     dict['taobaoId'] = taodict['num_iid']
    #     dict['image'] = "https:" + taodict['pict_url'] + '_250x250'
    #     # dict['endTime'] = taodict['coupon_end_time']
    #     dict['goodsName'] = taodict['title']
    #     dict['price'] = taodict['zk_final_price']
    #     dict['sellCount'] = taodict['volume']
    #     price = float(dict['price']) - int(dict['couponDenomination'])
    #     dict['finalPrice'] = "%.2f" % price
    #     return dict

