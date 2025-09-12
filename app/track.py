#coding=utf8

from app import create_app
import os
from app import db

class track(db.Model):
    __tablename__ = 'track'
    trackId = db.Column(db.String(32), primary_key=True)
    trackName = db.Column(db.String(64), unique=False) 
    clickCount = db.Column(db.BigInteger,unique=False)
    today =   db.Column(db.String(32), unique=False)
    yesterday =  db.Column(db.String(32), unique=False)
    todayClick = db.Column(db.Integer,unique=False)
    yesterdayClick = db.Column(db.Integer,unique=False)




    def trackresult(self):
        result = {}
        result['clickCount'] = self.clickCount
        result['trackId'] = self.trackId
        result['trackName'] = self.trackName
        result['todayClick'] = self.todayClick
        result['yesterdayClick'] = self.yesterdayClick
        result['today'] = self.today
        result['yesterday'] = self.yesterday
        return result

        

    