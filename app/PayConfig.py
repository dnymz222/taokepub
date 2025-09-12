from app import create_app
import os
from app import db
import sys
import logging

class PayConfig(db.Model):
    __tablename__ = 'PayConfig'
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    app = db.Column(db.String(36), unique=True)
    type= db.Column(db.String(36), unique=False)

    amount = db.Column(db.String(36), unique=False)
    activity_amount = db.Column(db.String(36), unique=False)
    activity_name = db.Column(db.String(64), unique=False)

    # JapaneseName = db.Column(db.String(32), unique=False)
    # Image = db.Column(db.String(256), unique=False)
    # RightAscension = db.Column(db.String(32), unique=False)
    # Declination = db.Column(db.String(32), unique=False)
    # Constellation = db.Column(db.String(32), unique=False)
    # Distance = db.Column(db.String(16), unique=False)
    # Age = db.Column(db.String(16), unique=False)



    def  payconfigdict(self):
        dict ={}

        dict["type"] = self.type
        dict["amount"] = self.amount
        dict["activity_name"] = self.activity_name
        dict["activity_amount"] = self.activity_amount
        dict["app"] = self.app
        return dict