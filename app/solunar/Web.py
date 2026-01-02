#coding=utf8
from . import solunar
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,render_template
from app import db

import urllib
import hashlib
import time
import datetime
from app.stardetail import stardetail
from app.ConstellationDetail import ConstellationDetail
from app.DeepskyDetail import DeepskyDetail
from app.CometDetail import CometDetail

headerhtml = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>Title</title><style type=\"text/css\">body{margin: 0px;background-color: #000;}p {color: #eeeeee;align-self: left;align-content: left;margin-left: 15px;}h2 {color: #fff;align-self: left;align-content: left;margin-left: 5px;}h3 {color: #fff;align-self: left;align-content: left;margin-left: 10px;} ul{align-self: left;align-content: left; margin-left: 10px;}li{color: #eeeeee;align-self: left;align-content: left;margin-left: 15px; }</style></head><body><div>"




@solunar.route("/star/detail/<combinedId>")
def stadetailweb(combinedId):
    language= request.args.get('language', "en")
    try:
        stardetailobject = db.session.query(stardetail).filter(stardetail.CombinedId == combinedId)[0]
        if language == "en":
            b  =stardetailobject.EnglishHTML
            link = stardetailobject.EnglishLink
            wiki = "Wikipedia"
            aticle = "Article"
        elif language == "zh":
            b = stardetailobject.ChineseHTML
            link = stardetailobject.ChineseLink
            wiki = "维基百科"
            aticle = "文章"
        else:
            b = stardetailobject.JapaneseHTML
            link  = stardetailobject.JapaneseLink
            wiki = "ウィキペディア"
            aticle = "記事"


        string = b.decode()

        # print  string

        # return  string


        return  headerhtml + string + "</div></body></html>"

        # return render_template("stardetail.html",html =string,wiki = link)
    except Exception as e:
        db.session.rollback()

        return render_template("error.html")


    finally:

        db.session.close()

@solunar.route("/constellation/detail/<shortname>")
def constellationdetailweb(shortname):
    language= request.args.get('language', "en")
    try:
        constellationDetailobject = db.session.query(ConstellationDetail).filter(ConstellationDetail.shortname == shortname)[0]
        if language == "en":
            b  =constellationDetailobject.EnglishHTML
            link = constellationDetailobject.EnglishLink
            wiki = "Wikipedia"
            aticle = "Article"
        elif language == "zh":
            b = constellationDetailobject.ChineseHTML
            link = constellationDetailobject.ChineseLink
            wiki = "维基百科"
            aticle = "文章"
        else:
            b = constellationDetailobject.JapaneseHTML
            link  = constellationDetailobject.JapaneseLink
            wiki = "ウィキペディア"
            aticle = "記事"


        string = b.decode()

        # print  string

        # return  string


        return  headerhtml + string +"</div></body></html>"

        # return render_template("stardetail.html",html =string,wiki = link)
    except Exception as e:
        db.session.rollback()

        return render_template("error.html")


    finally:

        db.session.close()


@solunar.route("/deepsky/detail/<Identifier>")
def deepskydetailweb(Identifier):
    language= request.args.get('language', "zh")
    try:
        constellationDetailobject = db.session.query(DeepskyDetail).filter(DeepskyDetail.Identifier == Identifier)[0]
        if language == "en":
            b  =constellationDetailobject.EnglishHTML
            link = constellationDetailobject.EnglishLink
            wiki = "Wikipedia"
            aticle = "Article"
        elif language == "zh":
            b = constellationDetailobject.ChineseHTML
            link = constellationDetailobject.ChineseLink
            wiki = "维基百科"
            aticle = "文章"
        else:
            b = constellationDetailobject.JapaneseHTML
            link  = constellationDetailobject.JapaneseLink
            wiki = "ウィキペディア"
            aticle = "記事"


        string = b.decode()

        # print  string

        # return  string


        return  headerhtml + string + "</div></body></html>"

        # return render_template("stardetail.html",html =string,wiki = link)
    except Exception as e:
        print(e)
        db.session.rollback()

        return render_template("error.html")


    finally:

        db.session.close()








