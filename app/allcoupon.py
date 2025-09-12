from app import db
import time
import datetime
from app.utils.constvalue import allcatelist,couponUrl

# nowTimeSting = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# nowTime = datetime.datetime.strptime(nowTimeSting, "%Y-%m-%d")


class allcoupon(db.Model):
    __tablename__ = 'thirdcoupon'
    taobaoId = db.Column(db.BigInteger, primary_key=True)
    goodsName = db.Column(db.String(200),unique=False)
    couponId = db.Column(db.String(60), unique=False)
    detail = db.Column(db.String(100),unique=False)
    image = db.Column(db.String(160),unique=False)
    cate = db.Column(db.String(100),unique=False)
    cateId = db.Column(db.String(32),unique=False)
    price = db.Column(db.String(32),unique=False)
    sellCount = db.Column(db.Integer,unique=False)
    check = db.Column(db.BOOLEAN,unique=False)
    jinpai = db.Column(db.BOOLEAN, unique=False)
    incomeRate = db.Column(db.String(32), unique=False)
    #incomeRate = db.Column(db.String(32),unique=False)
    shopId = db.Column(db.String(32),unique=False)
    shopName = db.Column(db.String(60),unique=False)
    #couponAmount = db.Column(db.Integer,unique=False)
    #couponLeft = db.Column(db.Integer,unique=False)
    couponDenomination = db.Column(db.Integer,unique=False)
    endTime = db.Column(db.Date,unique=False,index=True)
    onTime = db.Column(db.Date,unique=False,index=True)
    #couponUrl = db.Column(db.String(160),unique=False)
    couponPromotUrl = db.Column(db.String(320),unique=False)
    dsr = db.Column(db.String(16),unique=False)


    def __init__(self,dict,ontime):

        self.taobaoId = int(dict['goods_id'])
        self.goodsName= dict['goods_title']
        self.detail = 'http://item.taobao.com/item.htm?id=' + str(dict['goods_id'])
        self.image = dict['goods_pic']
        self.cateId= dict['goods_cate_id']
        self.cate =allcatelist[self.cateId-1]
        self.couponId =  dict['coupon_id']
        self.dsr = str(dict['dsr'])
        self.incomeRate = dict['commission_rate']
        self.jinpai= bool(dict['jinpai'])
        self.price = dict['goods_price']
        self.sellCount =dict['goods_sale_num']
        self.check = False
        self.shopId = dict['seller_id']
        self.shopName = ''
        self.couponDenomination = int(float(dict['coupon_amount']))
        endtimestring = dict['coupon_end_time']
        if isinstance(endtimestring,basestring):
            self.endTime = datetime.datetime.strptime(endtimestring[0:10],"%Y-%m-%d")
        self.couponPromotUrl = couponUrl + self.couponId +'&itemId='+str(dict['goods_id'])
        self.onTime = ontime

    def allcoupondict(self):
        dict ={}
        dict['cateId'] = self.cateId
        dict['couponUrl'] = self.couponPromotUrl
        dict['couponDenomination'] = self.couponDenomination
        dict['shopName'] = self.shopName
        dict['taobaoId'] = str(self.taobaoId)
        dict['image'] = self.image + '_250x250'
        dict['endTime'] = self.endTime.strftime('%Y-%m-%d')
        dict['goodsName'] = self.goodsName
        dict['price'] = self.price
        dict['sellCount'] = str(self.sellCount)
        return dict
