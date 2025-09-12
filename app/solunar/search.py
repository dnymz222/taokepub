#coding=utf8
import os.path

from . import solunar
from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
import json
from flask import request,session,url_for,redirect,make_response
from app import db

import urllib
import hashlib
import time
import datetime
from app.Star import Star
from app.Constellation import Constellation
from app.ConstellationDetail import ConstellationDetail
from app.Caldwell import Caldwell
from app.Messier import Messier
from app.NGCC import NGCC
from app.TychoIndex import TychoIndex
from app.CCDMStar import CCDMStar
from app.Galaxy import Galaxy
from app.GlobularClusters import GlobularClusters
from app.OpenClusters import OpenClusters
from app.DiffuseNebulae import DiffuseNebulae
from app.ProtoplanetaryNebulae import ProtoplanetaryNebulae
from app.PlanetaryNebulae import PlanetaryNebulae
from app.AstroEvent import AstroEvent
from app.Comet import Comet
from app.CometDetail import CometDetail
from app.HIPStar import HIPStar
from app.HDStar import HDStar
from app.HRStar import HRStar
from app.SAOStar import SAOStar
from app.CCDMStar import CCDMStar
from app.NGCCStar import NGCCStar
from app.GCVSStar import GCVSStar
from app.Tycho import Tycho
from app.TychoSuppl import TychoSuppl
from app.Tycho2 import Tycho2
from app.Asteroid import Asteroid
from app.MeteorShowers import MeteorShowers
from config import  basedir
from app.stardetail import stardetail
from app.DeepskyDetail import DeepskyDetail






@solunar.route("/constellation")
def constellation():
    # result = {}
    list = []

    try:
        constellations   = db.session.query(Constellation).all()
        for constellationobject in constellations:
            dict = constellationobject.constellationDict()
            list.append(dict)
        # result[x_code] = 200
        # result[x_data] = list
    except Exception as e:
        print(e)
        # result[x_meesage] = e.message
        # result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)


@solunar.route("/star")
def starlist():
    list =[]
    try:
        stars = db.session.query().all()
        for starobjcet in stars:

            if len(starobjcet.Magnitude)>0:
                dict = starobjcet.stardict()
                list.append(dict)

    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    content = json.dumps(list)
    response = make_response(content)
    response.headers["Content-Disposition"] = "p_w_upload; filename=starlist.dat"

    return response


@solunar.route("/star/fix")
def starlistfix():
    list = []
    try:
        stars = db.session.query(Star).all()
        for starobjcet in stars:

            dec = starobjcet.Declination
            dec.replace("−","-")

            starobjcet.Declination = dec
            try:
                db.session.commit()
            except:
                db.session.rollback()

    except Exception as  e:
        print (e)
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)




@solunar.route("/star/main")
def mainstarlist():
    list =[]
    try:
        stars = db.session.query(Star).filter(Star.Magnitude < 2.001).all()
        for starobjcet in stars:
            dict = starobjcet.stardict()
            list.append(dict)

    except Exception as e:
        print (e)
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)

@solunar.route("/star/<constellation>")
def mainstarlistconstealltion(constellation):
    list =[]
    try:
        stars = db.session.query(Star).filter(Star.ConsetellationName == constellation).all()
        for starobjcet in stars:
            dict = starobjcet.stardict()
            list.append(dict)
            # constellationname = starobjcet.ConsetellationName
            # newstring = constellationname.replace(" ","")
            # starobjcet.ConsetellationName = newstring
            # try:
            #     db.session.commit()
            # except:
            #     db.session.rollback()

    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)






@solunar.route("/messier/main")
def messierlistmain():
    list = []
    try:
        messiers = db.session.query(Messier).filter(Messier.Magnitude < 6.5001).all()
        for messierobject in  messiers:
            dict = messierobject.messierdict()
            list.append(dict)
    except Exception as  e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)

@solunar.route("/messier")
def messierlist():
    list = []
    try:
        messiers = db.session.query(Messier).all()
        for messierobject in  messiers:
            dict = messierobject.messierdict()
            list.append(dict)
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)


@solunar.route("/caldwell")
def caldwelllist():
    result  ={}
    list = []
    try:
        messiers = db.session.query(Caldwell).all()
        for messierobject in  messiers:
            dict = messierobject.caldwellDict()
            list.append(dict)
        result[x_code]=200
        result[x_data] = list
    except Exception as e:
        result[x_code]=201
        result[x_meesage] = "%s"%e
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)

@solunar.route("/NGCC")
def ngcclist():
    list = []
    try:
        ngccs = db.session.query(NGCC).all()
        for ngccobject in  ngccs:

            dict = ngccobject.NGCCDict()
            list.append(dict)
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)

@solunar.route("/globular")
def goloubularlist():
    result = {}
    list = []
    try:
        golobulars = db.session.query(GlobularClusters).all()

        for golobularobject in  golobulars:

            try:
                db.session.commit()
            except :
                db.session.rollback()
            dict = golobularobject.gloubarclusterDict()
            list.append(dict)
        result[x_data] = list
        result[x_code] = 200
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)


@solunar.route("/opencluster")
def OpenClusterlist():
    result = {}
    list = []
    try:
        openclusters = db.session.query(OpenClusters).all()

        for openclusteobject in  openclusters:

            dict = openclusteobject.openclusterDict()
            list.append(dict)
        result[x_code]  =200
        result[x_data] =list
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)

@solunar.route("/galaxy")
def galaxylist():
    result = {}
    list = []
    try:
        galaxys = db.session.query(Galaxy).all()

        for galaxyobject in  galaxys:

            try:
                db.session.commit()
            except :
                db.session.rollback()
            dict = galaxyobject.galaxydict()
            list.append(dict)
        result[x_code]  = 200
        result[x_data] = list
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)

@solunar.route("/diffuse")
def diffuselist():
    result = {}
    list = []
    try:
        diffuses = db.session.query(DiffuseNebulae).all()
        for diffuseobject in  diffuses:

            dict = diffuseobject.diffuseDict()
            list.append(dict)
        result[x_code] =200
        result[x_data] = list
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)


@solunar.route("/planetarynebulae")
def planetarynebulaelist():
    result = {}
    list = []
    try:
        planetarynebulaes = db.session.query(PlanetaryNebulae).all()
        for planetarynebulaeobject in planetarynebulaes:

            dict = planetarynebulaeobject.planetarynebulaeDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)

@solunar.route("/protoplanetarynebulae")
def protoplanetarynebulaelist():
    result = {}
    list = []
    try:
        protoplanetarynebulaes = db.session.query(ProtoplanetaryNebulae).all()
        for protoplanetarynebulaeobject in protoplanetarynebulaes:

            dict = protoplanetarynebulaeobject.protoplanetarynebulaeDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)



@solunar.route("/tycho/index")
def tychoindex():
    list =[]
    try:
        tyindexs = db.session.query(TychoIndex).all()
        for tychoindexobjcet in tyindexs:
            dict = tychoindexobjcet.props_dict()

            list.append(json.load(dict))

    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(list)


@solunar.route("/event")
def astroevent():
    language = request.args.get("language","zh")
    year = request.args.get("year","2021")
    time = ""
    if language == "zh":
        time = "8"
    elif language =="jp":
        time= "9"
    else:
        time = "GMT"
    result = {}
    list = []
    try:
        events = db.session.query(AstroEvent).filter(AstroEvent.language == language,AstroEvent.year == year,AstroEvent.timezone == time).order_by(AstroEvent.recordIndex).all()
        for event in  events:
            dict = event.astroeventdict()
            list.append(dict)
        result[x_data] = list
        result[x_code] =200
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e


    return json.dumps(result)


@solunar.route("/event/modify")
def astroeventmodify():
    language = request.args.get("language","jp")
    year = request.args.get("year","2021")
    result = {}
    list = []
    try:
        events = db.session.query(AstroEvent).filter(AstroEvent.language == language,AstroEvent.year == year).order_by(AstroEvent.recordIndex).all()
        for event in  events:
            timezone = event.timezone

            if  timezone.find("+")>0:
                try:
                    event.timezone =timezone[4:]
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()

        result[x_data] = list
        result[x_code] =200
    except Exception as e:
        result[x_code] = 201
        result[x_meesage] = "%s"%e


    return json.dumps(result)


@solunar.route("/event/new")
def astroeventnew():
    language = request.args.get("language","zh")
    year = request.args.get("year","2022")
    time =  request.args.get("time","8")
    result = {}
    list = []
    try:
        events = db.session.query(AstroEvent).filter(AstroEvent.language == language,AstroEvent.year == year,AstroEvent.timezone== time).order_by(AstroEvent.recordIndex).all()
        for event in  events:
            dict = event.astroeventdict()
            list.append(dict)
        result[x_data] = list
        result[x_code] =200
    except Exception as e:

        result[x_code] = 201
        result[x_meesage] = "%s"%e


    return json.dumps(result)



@solunar.route("/comet")
def cometlist():
    result = {}
    list = []
    # type  =request.args.get("type","1")

    try:
        # if type == "1":
        #     comets = db.session.query(Comet).filter_by(Comet.MotionType == 1).all()
        # else:
        comets = db.session.query(Comet).all()
        for cometobject in  comets:

            dict = cometobject.cometDict()
            list.append(dict)
        result[x_code] =200
        result[x_data] = list
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)


@solunar.route("/asteroid")
def asteroidlist():
    result = {}
    list = []
    # type  =request.args.get("type","1")

    try:
        # if type == "1":
        #     comets = db.session.query(Comet).filter_by(Comet.MotionType == 1).all()
        # else:
        comets = db.session.query(Asteroid).all()
        for cometobject in  comets:

            dict = cometobject.asteroidDict()
            list.append(dict)
        result[x_code] =200
        result[x_data] = list
    except Exception as e:
        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)




@solunar.route("/ccdm/page")
def CCDMStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        ccdmpagi = db.session.query(CCDMStar).order_by(CCDMStar.CCDM).paginate(page=int(page), per_page=100)
        ccdms = ccdmpagi.items
        for ccdmobject in ccdms:
            dict = ccdmobject.ccdmDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)

@solunar.route("/ccdm/read")
def CCDMStarread():

    result = {}
    list = []
    try:
        ccdms = db.session.query(CCDMStar).filter(CCDMStar.HIP >0).all()

        for ccdmobject in ccdms:
            hip = ccdmobject.HIP

            try:
                    hipobject = db.session.query(HIPStar).filter(HIPStar.HIP == hip)[0]

                    ccdmobject.RA199125 = hipobject.RA199125
                    ccdmobject.DE199125 = hipobject.DE199125
                    db.session.commit()


            except:
                    db.session.rollback()





    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e

    return json.dumps(result)


@solunar.route("/ccdm/read/add")
def CCDMStarreadadd():

    result = {}
    list = []
    try:
        ccdms = db.session.query(CCDMStar).filter(CCDMStar.HIP == "").all()

        for ccdmobject in ccdms:
            ra = ccdmobject.RA199125
            if ra is None:
                number = ccdmobject.CCDM
                prefix = number[:-4]
                try:
                    hipobject = db.session.query(CCDMStar).filter(CCDMStar.CCDM.like("%"+prefix+"%") ,CCDMStar.HIP >0)[0]

                    ccdmobject.RA199125 = hipobject.RA199125
                    ccdmobject.DE199125 = hipobject.DE199125

                    db.session.commit()


                except Exception as e:
                    print(e)
                    db.session.rollback()
            else:
                continue



    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e

    return json.dumps(result)


@solunar.route("/hd/page")
def hdStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        hdpagi = db.session.query(HDStar).order_by(HDStar.HD).paginate(page=int(page), per_page=100)
        hds = hdpagi.items
        for hdobject in hds:
            dict = hdobject.HDStarDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)

@solunar.route("/hip/page")
def hipStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        hippagi = db.session.query(HIPStar).order_by(HIPStar.HIP).paginate(page=int(page), per_page=100)
        hips = hippagi.items
        for hipobject in hips:
            dict = hipobject.HIPStarDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)


@solunar.route("/hr/page")
def hrStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        hrpagi = db.session.query(HRStar).order_by(HRStar.HR).paginate(page=int(page), per_page=100)
        hrs = hrpagi.items
        for hrobject in hrs:
            dict = hrobject.HRStarDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)


@solunar.route("/sao/page")
def saoStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        saopagi = db.session.query(SAOStar).order_by(SAOStar.SAO).paginate(page=int(page), per_page=100)
        saos = saopagi.items
        for saoobject in saos:
            dict = saoobject.SAOStarDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)


@solunar.route("/gcvs/page")
def gcvsStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        gcvspagi = db.session.query(GCVSStar).order_by(GCVSStar.GCVS).paginate(page=int(page), per_page=100)
        gcvss = gcvspagi.items
        for gcvsobject in gcvss:
            dict = gcvsobject.GVVStrarDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)


@solunar.route("/tycho/page")
def tychoStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        tychopagi = db.session.query(Tycho).order_by(Tycho.TYC).paginate(page=int(page), per_page=100)
        tychos = tychopagi.items
        for tychoobject in tychos:
            dict = tychoobject.tychodict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)

@solunar.route("/tycho2/page")
def tycho2StarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        tycho2pagi = db.session.query(Tycho2).order_by(Tycho2.TYCId).paginate(page=int(page), per_page=100)
        tycho2s = tycho2pagi.items
        for tycho2object in tycho2s:
            dict = tycho2object.Tycho2Dict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)

@solunar.route("/tychosp/page")
def tychospStarPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        tychosppagi = db.session.query(TychoSuppl).order_by(TychoSuppl.TYCId).paginate(page=int(page), per_page=100)
        tychosps = tychosppagi.items
        for tychospobject in tychosps:
            dict = tychospobject.tychosupplDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)

@solunar.route("/ngc/page")
def ngccPage():
    page = request.args.get("page","1")
    result = {}
    list = []
    try:
        ngcpagi = db.session.query(NGCCStar).order_by(NGCCStar.Name).paginate(page=int(page), per_page=100)
        ngcs = ngcpagi.items
        for ngcobject in ngcs:
            dict = ngcobject.NGCCStarDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)

@solunar.route("/metershower")
def metershower():
    year = request.args.get("year","2021")
    os = request.args.get("os","iOS")
    result = {}
    list = []

    try:
        metershowers = db.session.query(MeteorShowers).filter(MeteorShowers.year == year).order_by(MeteorShowers.index).all()

        for metershowerobject in metershowers:
            dict = metershowerobject.meteoshowersDict()
            if dict["shortname"] == "QUA":
                if os == "android":
                    dict["year"] = str(int(year)-1)
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list

    except Exception as e:
        db.session.rollback()
        result[x_meesage]  = "%s"%e
        result[x_code]  = 201

    return json.dumps(result)


@solunar.route("/constellation/detail/json")
def constellationdetailjson():

    list = []

    # path = os.path.join(basedir,"static/astronomy/json")
    try:
        metershowers = db.session.query(Constellation).all()

        for metershowerobject in metershowers:
            dict = metershowerobject.constellationDict()
            list.append(dict)


    except Exception as e:
        db.session.rollback()
    #
    # jpath = os.path.join(path,"deepskydetail.json")
    # jf = open(jpath,"w")
    # jf.write(json.dumps(list))
    return json.dumps(list)

