from app import create_app
import os
from app import db
import sys
import logging

class TyphoonModel(db.Model):
    __tablename__ = 'TyphoonModel'
    id = db.Column(db.String(64), primary_key=True)
    year = db.Column(db.String(16), unique=False)
    basin = db.Column(db.String(16), unique=False)
    englishname = db.Column(db.String(64), unique=False)
    name = db.Column(db.String(64), unique=False)
    isActive = db.Column(db.String(16), unique=False)

