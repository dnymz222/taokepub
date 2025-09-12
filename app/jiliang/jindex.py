
from flask import request,render_template
import urllib
import json
from . import jiliang
from bs4 import BeautifulSoup
from app.utils.constvalue import iplist
from app import db
import pandas as pd
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from config import basedir
from app.JiliangCert import JiliangCert
import re
from openpyxl import load_workbook
import datetime


@jiliang.route("/search", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        cert_id = request.form.get("cert_id")
        cert = JiliangCert.query.filter_by(cert_id=cert_id).first()
        if cert:
            result = cert.to_dict()
        else:
            pass
    return render_template("jiliangsearch.html", result=result)


@jiliang.route("/check/none")
def checknone():
    checkietms = db.session.query(JiliangCert).all()
    for checkietm in checkietms:
        if checkietm.serial_number is None:
            try:
                db.session.delete(checkietm)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
    return "done"

def excel_date_to_datetime(excel_number, datemode=0):
    """将 Excel 数字型日期转成 datetime"""
    return datetime.datetime(1899, 12, 30) + datetime.timedelta(days=excel_number + (1462 if datemode==1 else 0))


def parse_date_column(series: pd.Series) -> pd.Series:
    """
    通用日期解析函数：兼容多种日期格式（包括中文）
    输入：pandas Series（日期列，可能混杂字符串/日期/NaN）
    输出：统一为 pandas datetime（无效的返回 NaT）
    """

    def parse_date(x):
        if pd.isna(x):
            return pd.NaT

        if isinstance(x, (int, float)):
            try:
                return excel_date_to_datetime(x, 0)
            except:
                return x # 解析失败就保留原始值

        if isinstance(x, pd.Timestamp):
            return x
        if isinstance(x, str):
            s = x.strip()
            # 处理中文日期，例如 "2025年8月30日"
            if re.search(r"\d+年\d+月\d+日", s):
                s = re.sub("年", "-", s)
                s = re.sub("月", "-", s)
                s = re.sub("日", "", s)
            elif  re.search(r"\d+月\d+日\d+年", s):
                s = re.sub("年", "", s)
                s = re.sub("月", "/", s)
                s = re.sub("日", "/", s)
            try:
                return pd.to_datetime(s, errors="raise", infer_datetime_format=True)
            except:
                return pd.NaT
        return pd.NaT

    return series.apply(parse_date)

@jiliang.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("没有文件")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("没有选择文件")
            return redirect(request.url)
        if file and file.filename.endswith((".xlsx", ".xls")):
            filepath = os.path.join(basedir,"static/jiliang", file.filename)
            file.save(filepath)

            wb = load_workbook(filepath, data_only=True)
            sheet = wb.active

            data = []
            for row in sheet.iter_rows(values_only=True):
                data.append(row)

            df = pd.DataFrame(data[1:], columns=data[0])

            # 读取Excel
            # df = pd.read_excel(filepath,dtype=str)
            # print(df)

            # Excel 列名中文 -> 英文 映射
            col_map = {
                "证书编号": "cert_id",
                "送检单位": "company",
                "计量器具名称": "instrument_name",
                "型号/规格": "model",
                "型号规格": "model",   # 兼容情况
                "出厂编号": "serial_number",
                "管理编号": "manage_id",
                "管理编码": "manage_id",# 兼容情况
                "批准人": "approver",
                "核验员": "inspector",
                "检定员": "verifier",
                 "校准员":"verifier",# 兼容情况
                "检校日期": "check_date",
            }

            df = df.rename(columns=col_map)
            # print(df)
            df["check_date"] = parse_date_column(df["check_date"])
            # print(df)




            # 清空旧数据
            # db.session.query(jiliang).delete()

            # 插入新数据
            for _, row in df.iterrows():
                try:
                    print(row)
                    cert = JiliangCert(
                        cert_id=str(row.get("cert_id")),
                        company=row.get("company"),
                        instrument_name=row.get("instrument_name"),
                        model=row.get("model"),
                        serial_number=row.get("serial_number"),
                        manage_id=row.get("manage_id"),
                        approver=row.get("approver"),
                        inspector=row.get("inspector"),
                        verifier=row.get("verifier"),
                        check_date=str(row.get("check_date")),
                    )
                    cert0 = JiliangCert.query.filter_by(cert_id=cert.cert_id).first()
                    if cert0:
                        cert0.company = cert.company
                        cert0.instrument_name = cert.instrument_name
                        cert0.model = cert.model
                        cert0.serial_number = cert.serial_number
                        cert0.manage_id = cert.manage_id
                        cert0.approver = cert.approver
                        cert0.inspector = cert.inspector
                        cert0.verifier = cert.verifier
                        cert0.check_date = cert.check_date
                    else:
                        db.session.add(cert)
                    db.session.commit()
                except Exception as e:
                    # print(e)
                    db.session.rollback()
            flash("文件上传并导入数据库成功！")
            return redirect(url_for("jiliang.index"))

    return render_template("jiliangupload.html")







