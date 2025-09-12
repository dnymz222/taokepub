#coding=utf8
from app import create_app
import os
from app import db
import time
import datetime

class WorkingDaysModel(db.Model):
    __tablename__ = 'workingdaysmodel'
    recordId = db.Column(db.String(80), primary_key=True)  #
    date = db.Column(db.String(32), unique=False)
    day = db.Column(db.String(16), unique=False)
    year = db.Column(db.String(16), unique=False)
    month = db.Column(db.String(16), unique=False)
    code =  db.Column(db.String(16), unique=False)
    configuration = db.Column(db.String(64), unique=False)  #

    working_day = db.Column(db.String(16), unique=False)
    work_hours = db.Column(db.String(16), unique=False)

    morning_start = db.Column(db.String(16), unique=False)
    morning_end = db.Column(db.String(16), unique=False)
    afternoon_start = db.Column(db.String(16), unique=False)
    afternoon_end = db.Column(db.String(16), unique=False)



    public_holiday = db.Column(db.String(16), unique=False)

    public_holiday_description = db.Column(db.String(160), unique=False)
    weekend_day = db.Column(db.String(16), unique=False)





    def __init__(self,dict):
        self.day = dict["day"]
        self.year = dict["year"]
        self.month = dict["month"]
        self.code = dict["code"]
        self.configuration = dict["configuration"]
        self.work_hours = dict["work_hours"]
        self.working_day = dict["working_day"]
        self.public_holiday = dict["public_holiday"]
        self.public_holiday_description = dict["public_holiday_description"]
        self.weekend_day = dict["weekend_day"]

        self.morning_start = dict["morning_start"]
        self.morning_end = dict["morning_end"]
        self.afternoon_start = dict["afternoon_start"]
        self.afternoon_end = dict["afternoon_end"]

        self.date = self.year+"-"+self.month+"-"+self.day

        self.recordId  = self.code+"_"+self.date+"_"+self.configuration

    # def __init__(self, year,month,day,code,config,working_day,weekend):
    #     self.day = day
    #     self.year = year
    #     self.month = month
    #     self.code = code
    #     self.configuration = config
    #     self.work_hours = "8"
    #     self.working_day = working_day
    #     self.public_holiday = "0"
    #     self.public_holiday_description = ""
    #     self.weekend_day =weekend
    #
    #     self.morning_start = ""
    #     self.morning_end = ""
    #     self.afternoon_start = ""
    #     self.afternoon_end = ""
    #
    #     self.date = self.year + "-" + self.month + "-" + self.day
    #
    #     self.recordId = self.code + "_" + self.date + "_" + self.configuration

    def  woringdaysdict(self):
        dict = {}
        dict["work_hours"] = self.work_hours
        dict["day"] = self.day
        dict["month"] = self.month
        dict["date"]  = self.date
        dict["year"] = self.year
        dict["working_day"] = self.working_day
        dict["public_holiday"] = self.public_holiday
        dict["public_holiday_description"] = self.public_holiday_description
        dict["weekend_day"] = self.weekend_day
        dict["work_hours"] = self.work_hours
        dict["configuration"] = self.configuration
        dict["code"] = self.code

        return dict
