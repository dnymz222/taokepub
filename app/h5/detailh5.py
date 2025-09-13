from flask import request,render_template
import urllib
import json
from . import h5
from bs4 import BeautifulSoup

from app import db





@h5.route('/privacy')
def privacy():
    return render_template('privacy.html')

@h5.route('/user')
def user():
    return render_template('user.html')

@h5.route('/lama/privacy')
def lamaprivacy():
    return render_template('lamaprivacy.html')


@h5.route('/fishinghelper/privacy')
def fishinghelper():
    return  render_template('fishinghelper.html')

@h5.route('/fishing/privacy')
def fishingprivacy():
    return  render_template('fishinghelper.html')

@h5.route('/solunar/privacy')
def solunarprivacy():
    return render_template('solunar.html')

@h5.route('/solunar/privacy/2')
def solunarprivacy_vivo():
    return render_template('solunarprivacy_vivo.html')


@h5.route('/solunar/user')
def solunaruser():
    return render_template('solunaruser.html')


@h5.route('/solunar/user/vip')
def solunaruservip():
    return  render_template('solunarvip.html')




@h5.route('/fishshopping/privacy')
def fishshopping_privacy():
    return  render_template('fishshopping_privacy.html')

@h5.route('/fishingshoping/user')
def fishshopping_user_itemservice():
    return  render_template('fishshopping_user.html')


# @h5.route('/fishing/user')
# def fishinguser():
#     return  render_template('fishinguser.html')



@h5.route('/weatherlive/privacy')
def weatherliveprivacy():
    return  render_template('weatherlive.html')

@h5.route('/weatherlive/privacy/en')
def weatherliveprivacy_en():
    return render_template("weatherlive_en.html")

@h5.route('/fishinghelper/privacy/en')
def fishinghelper_en():
    return  render_template('fishinghelper_en.html')

@h5.route('/fishinghelper/privacy/jp')
def fishinghelper_jp():
    return  render_template('fishinghelper_en.html')

@h5.route('/fishinghelper/privacy/hk')
def fishinghelper_hk():
    return  render_template('fishinghelper_en.html')


@h5.route('/fishing/user')
def fishinguser():
    return  render_template('fishinguser.html')

@h5.route('/fishing/user/vip')
def fishinguservip():
    return  render_template('fishingvip.html')

@h5.route('/fishing/user/en')
def fishinguser_en():
    return  render_template('fishinguser_en.html')

@h5.route('/fishing/user/jp')
def fishinguser_jp():
    return  render_template('fishinguser_en.html')

@h5.route('/fishing/user/hk')
def fishinguser_hk():
    return  render_template('fishinguser_en.html')

@h5.route('/solunartides/privacy')
def solunartidesprivicy():
    return  render_template('solunartides.html')

@h5.route('/solunartides/analysis')
def solunartidesanalysis():
    return  render_template('tideanalysis.html')

@h5.route('/solunartides/user')
def solunartidesuser():
    return  render_template('solunartidesuser.html')

@h5.route('/solunartides/privacy/us')
def solunartidesprivicy_us():
    return  render_template('solunartides_us.html')

@h5.route('/solunartides/analysis/us')
def solunartidesanalysis_us():
    return  render_template('tideanalysis_us.html')

@h5.route('/solunartides/user/us')
def solunartidesuser_us():
    return  render_template('solunartidesuser_us.html')

@h5.route('/solunartides/privacy/hk')
def solunartidesprivicy_hk():
    return  render_template('solunartides_us.html')

@h5.route('/solunartides/analysis/hk')
def solunartidesanalysis_hk():
    return  render_template('tideanalysis_us.html')

@h5.route('/solunartides/user/hk')
def solunartidesuser_hk():
    return  render_template('solunartidesuser_us.html')


@h5.route('/solunartides/privacy/jp')
def solunartidesprivicy_jp():
    return  render_template('solunartides_us.html')

@h5.route('/solunartides/analysis/jp')
def solunartidesanalysis_jp():
    return  render_template('tideanalysis_us.html')

@h5.route('/solunartides/user/jp')
def solunartidesuser_jp():
    return  render_template('solunartidesuser_us.html')


@h5.route('/solunartides/privacy/kr')
def solunartidesprivicy_kr():
    return  render_template('solunartides_us.html')

@h5.route('/solunartides/analysis/kr')
def solunartidesanalysis_kr():
    return  render_template('tideanalysis_us.html')

@h5.route('/solunartides/user/kr')
def solunartidesuser_kr():
    return  render_template('solunartidesuser_us.html')


@h5.route("/fishing/solunartheory")
def fishingsolunartheory():
    return render_template("solunartheory.html")



@h5.route("/fishing/download")
def fishingdownload():
    return render_template("fishingdownload.html")

@h5.route("/xunquan/download")
def xunquandownload():
    return render_template("download.html")

@h5.route("/fishingweather/download")
def fishingweatherdownload():
    return render_template("download_fish.html")

@h5.route("/solunar/download")
def solunardownload():
    return render_template("download_solunar.html")

@h5.route("/tide/download")
def tidedownload():
    return render_template("download_tide.html")



@h5.route("/astronomy/user")
def astronomyuser():

    return render_template("atronomyuser.html")



@h5.route("/astronomy/privacy")
def astronomyprivacy():

    return render_template("astronomyprivacy.html")



@h5.route("/meteocalc/user")
def metecalcouser():

    return render_template("weatherpocket_user_zh.html")



@h5.route("/meteocalc/privacy")
def meteocalcprivacy():

    return render_template("weatherpocket_privacy_zh.html")


@h5.route("/tian/static/terrain/<lat>/<lng>")
def tianstaticterrian(lat,lng):

    url = "http://api.tianditu.gov.cn/staticimage?center="+ lng + "," + lat + "&width=1024&height=1024&zoom=13&layers=ter_c,cta_c&tk=2783727892f62604956e3248c0d622ca"


    return render_template("tianstaticimage.html",url = url)


@h5.route("/tian/static/street/<lat>/<lng>")
def tianstaticstreet(lat,lng):
    location = lng + "," + lat
    url = "http://api.tianditu.gov.cn/staticimage?center="+ location +  "&markers=" + location + "&width=512&height=512&zoom=13&layers=vec_c,cva_c&tk=2783727892f62604956e3248c0d622ca"

    return render_template("tianstaticimage.html",url = url)




@h5.route('/chinalunitidal')
def chinalunitidal():
    try:
        bannerresult = db.session.query(chinaLunitidal).order_by(chinaLunitidal.index).all()


        return render_template('chinalunitidal.html', banners=bannerresult)

    except:
        db.session.rollback()
        return render_template('error.html')
    finally:
        db.session.close()





