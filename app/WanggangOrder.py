#coding=utf8
from app import create_app
import os
from app import db
import sys
import logging
import time
import datetime


OrderIdkey = "OrderId"
OrderDayKey  ="OrderDay"
OrderTeamkey  ="OrderTeam"
ClientManagerKey = "ClientManager"
ClientNameKey  = "ClientName"
ApplyAmountKey = "ApplyAmount"
LoanTypeKey = "LoanType"
MarkKey = "Mark"
StatusKey = "Status"
ResultDescriptionKey = "ResultDescription"
StatusTypeKey = "StatusType"
FallbackTimesKey = "FallbackTimes"
FallbackReasonKey = "FallbackReason"
FallbackTypeKey = "FallbackType"
AnalysisProgressKey = "AnalysisProgress"
RemarkKey = "Remark"
MonthKey = "Month"


OrderIdTitle = "投保单号码"
OrderDayTitle  ="交单日"
OrderTeamTitle  ="组别"
ClientManagerTitle = "客户经理"
ClientNameTitle  = "客户姓名"
ApplyAmountTitle = "申请金额"
LoanTypeTitle = "贷款类型"
MarkTitle = "标记"
StatusTitle = "状态"
ResultDescriptionTitle = "审批结果描述（通过/拒绝填写）"
StatusTypeTitle = "状态类别（通过/拒绝填写）"
FallbackTimesTitle = "回退次数"
FallbackReasonTitle = "回退原因描述"
FallbackTypeTitle = "回退类别"
AnalysisProgressTitle = "分析进度"
RemarkTitle = "备注"
MonthTitle = "所属月份"




class WanggangOrder(db.Model):
    __tablename__ = 'wanggangorder'
    OrderId = db.Column(db.String(64), primary_key=True)
    OrderDay = db.Column(db.String(32),unique=False)
    OrderTeam = db.Column(db.String(32),unique=False)
    ClientManager = db.Column(db.String(32),unique=False)
    ClientName = db.Column(db.String(32),unique=False)
    ApplyAmount  = db.Column(db.String(32),unique=False)
    LoanType = db.Column(db.String(32),unique=False)
    Mark = db.Column(db.String(32),unique=False)
    Status = db.Column(db.String(32),unique=False)
    ResultDescription = db.Column(db.String(320),unique=False)
    StatusType = db.Column(db.String(32),unique=False)
    FallbackTimes  =db.Column(db.String(32),unique=False)
    FallbackReason = db.Column(db.String(320),unique=False)
    FallbackType = db.Column(db.String(32),unique=False)
    AnalysisProgress = db.Column(db.String(32),unique=False)
    Remark = db.Column(db.String(32),unique=False)
    Month = db.Column(db.String(32),unique=False)
    Sheet  = db.Column(db.String(32),unique=False)


    def __init__(self,sheetName):
        self.Sheet = sheetName


    def orderdict(self):
        dict = {}
        dict[OrderIdkey] = self.OrderId
        dict[OrderDayKey] = self.OrderDay
        dict[OrderTeamkey] = self.OrderTeam
        dict[ClientManagerKey] = self.ClientManager
        dict[ClientNameKey] = self.ClientName
        dict[ApplyAmountKey] = self.ApplyAmount
        dict[LoanTypeKey] = self.LoanType
        dict[MarkKey] = self.Mark
        dict[ResultDescriptionKey] = self.ResultDescription
        dict[StatusKey] = self.Status
        dict[FallbackTimesKey]  = self.FallbackTimes
        dict[FallbackReasonKey] = self.FallbackReason
        dict[FallbackTypeKey] = self.FallbackType
        dict[AnalysisProgressKey] = self.AnalysisProgress
        dict[RemarkKey] = self.Remark
        dict[MonthKey] = self.Month
        dict["Sheet"]  = self.Sheet
        return dict

    def updatevalue(self,newobject):
        self.Mark = newobject.Mark
        self.ResultDescription = newobject.ResultDescription
        self.Status = newobject.Status
        self.FallbackTimes = newobject.FallbackTimes
        self.FallbackReason = newobject.FallbackReason
        self.FallbackType = newobject.FallbackType
        self.AnalysisProgress = newobject.AnalysisProgress
        self.Remark  = newobject.Remark
        self.Month = newobject.Month
        self.Sheet = newobject.Sheet










