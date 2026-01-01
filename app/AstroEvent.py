#coding=utf8
from app import create_app
import os
from app import db
class AstroEvent(db.Model):
    __tablename__ = 'AstroEvent'
    timelanguage = db.Column(db.String(32),primary_key=True)
    language = db.Column(db.String(16),unique=False)
    year = db.Column(db.String(16),unique=False)
    month = db.Column(db.String(16), unique=False)
    day = db.Column(db.String(16), unique=False)
    time = db.Column(db.String(16), unique=False)
    event = db.Column(db.String(320), unique=False)
    recordIndex = db.Column(db.Integer, unique=False)
    timezone = db.Column(db.String(16), unique=False)


#en
    # def __init__(self,Line,Year,Month,Timezone,Lanuage ,RecordIndex):
    #     self.year = Year
    #     self.month = Month
    #     self.timezone  = Timezone
    #     self.language = Lanuage
    #     self.recordIndex = RecordIndex
    #     self.day = Line[4:6]
    #     self.time = Line[8:13].strip()
    #     self.event= Line[15:]
    #     self.timelanguage = self.year+"-"+self.month+"-"+self.day+"-"+self.time+"-"+self.language+"-"+self.timezone

#日语
#     def __init__(self,year,month,day,time,RecodIndex,Event):
#         self.year = year
#         self.month = month
#         self.day = day
#         self.time = time
#         self.recordIndex = RecodIndex
#         self.event = Event
#         self.timezone = "9"
#         self.language = "jp"
#         idx = Event.find("：")
#         print "idx" + str(idx)
#         if idx > -1 and idx <3:
#             self.event = Event[idx+1:]
#         self.timelanguage = self.year + "-" + self.month + "-" + self.day + "-" + self.time + "-" + self.language + "-" + self.timezone

#中文
    def __init__(self,Line ,RecordIndex):
        self.year = Line[0:4]
        self.month = Line[5:7]
        self.day = Line[8:10]
        self.timezone  = "8"
        self.language = "zh"
        self.recordIndex = RecordIndex
        self.time = Line[11:16].strip()
        if len(self.time) < 2:
            self.time = ""
            self.event = Line[15:].strip()
        else:
            self.event = Line[16:].strip()
        # print ("event" + self.event)
        self.timelanguage = self.year+"-"+self.month+"-"+self.day+"-"+str(RecordIndex)+"-"+self.language+"-"+self.timezone

    def  astroeventdict(self):
        dict = {}
        dict["language"] = self.language
        dict["year"] = self.year
        dict["month"] = self.month
        dict["day"] = self.day
        dict["time"] = self.time
        dict["timezone"]  =self.timezone
        dict["event"] = self.event
        return dict






    # def __init__(self,Language,Dict):
    #     self.language = Language
    #     self.year = dict["year"]
    #     self.month = dict["month"]
    #     self.day = dict["day"]
    #     self.time = dict["time"]
    #     self.event = dict["event"]
    #     self.recordIndex = dict["recordIndex"]
    #     self.timelanguage = self.year +"-"+self.month +"-"+ self.day +"-"+ self.language
