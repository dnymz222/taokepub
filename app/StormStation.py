from app import create_app
import os
from app import db
import sys
import logging

class StormStation(db.Model):
    __tablename__ = 'StormStation'
    name = db.Column(db.String(100), primary_key=True)
    source = db.Column(db.String(20), unique=False)
    lat = db.Column(db.Float, unique=False)
    lng = db.Column(db.Float, unique=False)

    def __init__(self,dict):
        self.name = dict["name"]
        self.source = dict["source"]
        self.lat = dict["lat"]
        self.lng  = dict["lng"]