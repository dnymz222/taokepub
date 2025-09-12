#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging
import json

class Holiday(db.Model):
    __tablename__ = 'CalendarHoliday'
    HolidayId = db.Column(db.String(64), primary_key=True)
    CalendarType = db.Column(db.String(32), unique=False)
    startDate = db.Column(db.String(32), unique=False)
    endDate = db.Column(db.String(32), unique=False)
    localName = db.Column(db.String(320), unique=False)
    name = db.Column(db.String(320), unique=False)
    type =  db.Column(db.String(64), unique=False)
    startDay= db.Column(db.Integer, unique=False)
    endDay  = db.Column(db.Integer, unique=False)
    year = db.Column(db.Integer, unique=False)
