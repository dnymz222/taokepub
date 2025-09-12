#coding=utf8
from app import create_app
import os
from app import db
import base64



class XuanpinCoupon(db.Model):
    __tablename__ = 'xuanpincoupon'
    item_id = db.Column(db.String(32), primary_key=True)
    category_id = db.Column(db.String(32), unique=False)
    seller_id = db.Column(db.String(32))
    title = db.Column(db.String(160), unique=False)
    shop_title = db.Column(db.String(64), unique=False)
    price = db.Column(db.String(32), unique=False)  #excel里的价格 ￥120
    reserve_price = db.Column(db.String(32), unique=False) #原价
    zk_final_price = db.Column(db.String(32), unique=False)  #折扣价
    final_price =db.Column(db.Float, unique=False)  #最低到手价 (price -coupon_amount)*(1-kudian_rate) 比较标准
    image_url =  db.Column(db.String(320), unique=False)  #image
    coupon_share_url = db.Column(db.String(640), unique=False)  #旗舰店url
    coupon_amount = db.Column(db.Integer, unique=False)
    coupon_end_time = db.Column(db.String(32), unique=False)
    coupon_start_fee = db.Column(db.String(32), unique=False)
    volume_str = db.Column(db.String(32), unique=False)
    volume = db.Column(db.Integer, unique=False)
    update_day = db.Column(db.String(32), unique=False) #价格更新时间
    last_update_day = db.Column(db.String(32), unique=False) #上一次价格更新时间
    last_price =   db.Column(db.Float, unique=False)  #上一次价格
    last_low_price = db.Column(db.Float, unique=False) #上一次低价格
    last_low_day = db.Column(db.String(32), unique=False)  #上一次低价格时间
    lowest_price = db.Column(db.Float, unique=False)  #价格最低值
    lowest_day = db.Column(db.String(32), unique=False) #价格最低时间
    highest_price = db.Column(db.Float, unique=False)  # 价格最高值
    highest_day = db.Column(db.String(32), unique=False)  # 价格最高时间
    prcie_rate = db.Column(db.Float, unique=False) #与上一次价格相比变化比率
    prcie_delta = db.Column(db.Float, unique=False) #与上一次介格相比变化数目
    is_lowest =  db.Column(db.Boolean, unique=False) #本次是否是最低
    is_lower = db.Column(db.Boolean, unique=False)  #本次是否是更对
    price_score = db.Column(db.Float,unique = False) #价格评分 0-100
    is_taoke = db.Column(db.Boolean, unique=False)  # 店铺是否参加淘客
    kuadian_promotion_info = db.Column(db.String(32), unique=False) #跨店满减
    kudian_rate = db.Column(db.Float, unique=False) #跨店rate
    create_time = db.Column(db.Integer, unique=False) #上线时间



    def __init__(self,dict,is_taoke,create_time,update_day):
        self.item_id = dict["item_id"]
        self.seller_id = dict["seller_id"]
        self.category_id = ""
        self.title = dict["title"]
        self.shop_title = dict["shop_title"]
        self.price =  dict["price"]
        self.reserve_price = self.price[2:]
        self.zk_final_price = self.reserve_price
        self.final_price = float(self.zk_final_price)
        self.image_url = dict["image_url"]
        self.coupon_share_url = ""
        self.coupon_amount = 0
        self.coupon_end_time = ""
        self.coupon_start_fee = ""

        self.volume_str = dict["volume_str"]
        volume_str = self.volume_str
        index_jiao = volume_str.find("交")
        index_jia = volume_str.find("+")

        if index_jia > -1:
            volume = volume_str[index_jiao+3:index_jia]
        else:
            index_bi = volume_str.find("笔")
            if index_bi > -1:
                volume = volume_str[index_jiao+3:index_bi]
            else:
                index_jian = volume_str.find("件")
                volume = volume_str[index_jiao + 3:index_jian]


        self.volume = int(volume)
        self.update_day = update_day
        self.last_update_day = ""
        self.last_price = 0
        self.last_low_day =update_day
        self.last_low_price = self.final_price
        self.lowest_price = self.final_price
        self.lowest_day =update_day
        self.highest_price = self.final_price
        self.highest_day = update_day
        self.prcie_rate = 0
        self.prcie_delta = 0
        self.is_lowest = False
        self.is_lower = False
        self.price_score = 50
        self.is_taoke = is_taoke
        self.kuadian_promotion_info = ""
        self.kudian_rate = 0
        self.create_time = create_time

    # def __init__(self,dict,seller_id,updateDay):
    #     self.item_id  =dict["item_id"]
    #     self.seller_id = seller_id
    #     self.category_id = ""
    #     self.title = dict["title"]
    #     self.shop_title = dict["shop_title"]
    #     self.zk_final_price = dict["zk_final_price"]
    #     self.picture_url = dict["picture_url"]
    #     self.coupon_share_url = dict["coupon_share_url"]
    #     self.coupon_amount = dict["coupon_amount"]
    #     self.volume = dict["volume"]
    #     self.endTime = dict["endTime"]
    #     self.cateId = dict["cateId"]
    #     self.updateDay = updateDay
    #     self.lastUpdateDay = updateDay
    #     self.last_price = self.zk_final_price-self.coupon_amount
    #     self.last_low_day = updateDay
    #     self.lowest_price = self.zk_final_price-self.coupon_amount
    #     self.lowest_day = updateDay
    #     self.highest_price = self.zk_final_price-self.coupon_amount
    #     self.highest_day = updateDay
    #     self.prcie_rate = 0
    #     self.prcie_delta = 0
    #     self.is_lowest = True
    #     self.is_lower = True
    #     self.price_score = 0


    def xuanpincoupon2dict(self):
        dict = {}
        dict["item_id"] = self.item_id
        dict["title"] = self.title
        dict["shop_title"] =self.shop_title
        dict["zk_final_price"] = self.zk_final_price
        dict["final_price"] = self.final_price
        dict["price"] = self.price
        dict["image_url"] = self.image_url
        dict["volume"] = self.volume
        dict["volume_str"] = self.volume_str
        dict["seller_id"] = self.seller_id
        dict["is_taoke"] = self.is_taoke
        dict["price_score"] = self.price_score
        dict["is_lower"] = self.is_lower
        dict["is_lowest"] = self.is_lowest
        dict["coupon_share_url"] = self.coupon_share_url
        dict["coupon_amount"] = self.coupon_amount
        dict["coupon_end_time"] = self.coupon_end_time
        dict["coupon_start_fee"] = self.coupon_start_fee
        dict["kuadian_promotion_info"] = self.kuadian_promotion_info
        dict["kudian_rate"] = self.kudian_rate
        dict["update_day"] = self.update_day



        return  dict