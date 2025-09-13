#!/usr/bin/env python
#coding=utf8
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from app import create_app,db


from app.yuanorder import yuanorder
from app.appconfig import appconfig
from app.sharecoupon import sharecoupon
from app.appuser import appuser
from app.banner import banner
from app.special import special
from app.wxuser import wxuser
from app.qianggou import qianggou
from app.welfare import welfare
from app.column import column
from app.worldTidalStation import worldTidalStation
from app.chinaTidalStation import chinaTidalStation
from app.launchad import launchad
from app.appitem import appitem
from app.downloadAd import downloadAd
from app.Star import Star
from app.NGCC import NGCC
from app.Messier import Messier
from app.Constellation import Constellation
from app.Tycho import Tycho
from app.stardetail import stardetail
from app.ConstellationDetail import ConstellationDetail
from app.Caldwell import Caldwell
from app.CCDMStar import CCDMStar
from app.HDStar import HDStar
from app.HRStar import HRStar
from app.HIPStar import HIPStar
from app.Tycho import Tycho
from app.Tycho2 import Tycho2
from app.TychoSuppl import TychoSuppl
from app.TychoIndex import TychoIndex
from app.SAOStar import SAOStar
from app.GCVSStar import GCVSStar
from app.NGCCStar import NGCCStar
from app.OpenClusters import OpenClusters
from app.GlobularClusters import GlobularClusters
from app.Galaxy import Galaxy
from app.PlanetaryNebulae import PlanetaryNebulae
from app.ProtoplanetaryNebulae import ProtoplanetaryNebulae
from app.DiffuseNebulae import DiffuseNebulae
from app.DeepskyDetail import DeepskyDetail
from app.CometDetail import CometDetail
from app.StormStation import StormStation
from app.Asteroid import Asteroid
from app.Camera import Camera
from app.Xuanpin import Xuanpin
from app.WanggangOrder import WanggangOrder
from app.Holiday import Holiday
from app.DownloadAdClick import downloadAdClick
from app.XuanpinCate import XuanpinCate
from app.YuanCustomer import YuanCustomer
from app.Hefengtide import Hefengtide
from app.TyphoonModel import TyphoonModel
from app.JiliangCert import JiliangCert


#from app.models import User, Follow, Role, Permission, Post, Comment
from flask_script import Manager, Shell,Server

from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import datetime
import  MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request,session,Blueprint,redirect,url_for
from app.MeteorShowers import MeteorShowers
from app.AstroEvent import AstroEvent
from app.VipUser import VipUser
from app.Comet import Comet
from app.ChinaCounty import ChinaCounty
from app.WorkingDaysConfig import WorkingDaysConfig
from app.WorkingDaysModel import WorkingDaysModel
from app.XuannpinShop import XuanpinShop
from app.XuanpinCoupon import XuanpinCoupon
from app.XuanpinHistory import XuanpinHistory
from app.GoodsDetailImage import GoodsDetailImage
from app.saleconfig import saleconfig
from app.SurfSpot import SurfSpot
from app.WannaSurf import WannaSurf

import time


monkey.patch_all()

#from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


manager.add_command("server", Server())















# @manager.shell
# def make_shell_context():
#     return dict(app=app, db=db, coupon=coupon)


# @manager.shell
# def make_shell_context():
#     return dict(app=app, db=db, yuanorder= yuanorder)



# @manager.shell
# def make_shell_context():
#     return dict(app=app, db=db, appconfig= appconfig)

# @manager.shell
# def make_shell_context():
#     return dict(app=app, db=db, sharecoupon= sharecoupon)
@manager.shell
def make_shell_context():
    return dict(app=app, db=db, appuser= appuser)

# @manager.shell
# def make_shell_context():
#     return dict(app=app, db=db, qianggou= qianggou)



# def make_shell_context():
#         return dict(app=app)
# manager.add_command("shell", Shell(make_context=make_shell_context))
#manager.add_command('db', MigrateCommand)




@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()
    server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


@manager.command
def deploy():
    """Run deployment tasks."""
    pass

    #from flask.ext.migrate import upgrade
    #from app.models import Role, User

    # migrate database to latest revision
    #upgrade()

    # create user roles
    #Role.insert_roles()

    # create self-follows for all users
    #User.add_self_follows()

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template("index.html")


if __name__ == '__main__':
    manager.run()


