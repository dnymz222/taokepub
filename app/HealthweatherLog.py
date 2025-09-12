from app import create_app
import os
from app import db
import sys
import logging

class HealthweatherLog(db.Model):
    __tablename__ = 'HealthweatherLog'
    log_id= db.Column(db.String(100), primary_key=True)
    uuid = db.Column(db.String(100), unique=False)
    user_id = db.Column(db.String(16), unique=False)
    type = db.Column(db.SmallInteger, unique=False)
    grade = db.Column(db.SmallInteger, unique=False)
    day = db.Column(db.String(16), unique=False)
    hour = db.Column(db.String(16), unique=False)
    event_timestemp = db.Column(db.BigInteger, unique=False)
    hour_data = db.Column(db.BLOB, unique=False)
    compare_data = db.Column(db.BLOB, unique=False)
    log_timestemp = db.Column(db.BigInteger, unique=False)
    location = db.Column(db.BLOB, unique=False)