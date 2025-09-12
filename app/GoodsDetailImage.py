#coding=utf8
from app import create_app
import os
from app import db
import base64
import json



class GoodsDetailImage(db.Model):
    __tablename__ = 'goodsdetailimage'
    item_id = db.Column(db.String(32), primary_key=True)
    item_url = db.Column(db.String(160),unique=False)
    seller_id = db.Column(db.String(32),unique=False)
    title = db.Column(db.String(160), unique=False)
    small_images = db.Column(db.String(1000), unique=False)
    description_images = db.Column(db.String(5000), unique=False)
    has_update = db.Column(db.Boolean,unique=False)


    def __init__(self,item_id,title,item_url,seller_id):
        self.item_id   = item_id
        self.title = title
        self.small_images = ""
        self.description_images = ""
        self.item_url = item_url
        self.seller_id = seller_id
        self.has_update = False

    def GoodsDetailImageDict(self):
        dict ={}
        dict["title"] = self.title
        dict["item_url"] = self.item_url
        try:
            dict["small_images"] = json.loads(self.small_images)

        except Exception as e:
            dict["small_images"] = []


        try:
            dict["description_images"] = json.loads(self.description_images)
        except Exception as e:
            dict["description_images"] = []



        return dict
