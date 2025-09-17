from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask import Blueprint,session
from flask_login import UserMixin



import os


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'





def create_app(config_name):
#     app = Flask(__name__,static_folder = "./dist/static",
# template_folder = "./dist")
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/www/flask/taokepub/static/DB/eclipse1.db'
    
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:222222@localhost/xunquan'
    #

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/xuepingwang/Workspace/flask/taoke/static/DB/eclipse1.db'

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://luwan:Hyh671002@rm-bp1b6qz754yv0743fo.mysql.rds.aliyuncs.com/xunquan'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://luwan:Hyh671002@rm-bp1b6qz754yv0743f.mysql.rds.aliyuncs.com/xunquan'
    # # app.config['APNS_CERTIFICATE'] = './static/apns-dis.pem'
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify 
        sslify = SSLify(app)

    #from .main import main as main_blueprint
    #app.register_blueprint(main_blueprint)

    #from .auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint, url_prefix='/auth')

 


    from .api_3_0 import api3 as api_3_0_blueprint
    app.register_blueprint(api_3_0_blueprint,url_prefix='/api/v3.0')




    from .web import web as web_blueprint
    app.register_blueprint(web_blueprint,url_prefix="/web")

    from .h5 import h5 as h5_blueprint
    app.register_blueprint(h5_blueprint,url_prefix='/h5')






    from .tide import tide as tide_blueprint

    app.register_blueprint(tide_blueprint, url_prefix='/tide')







    from app.index import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/")


    from .yuan import yxx as yxx_blueprint

    app.register_blueprint(yxx_blueprint, url_prefix='/yxx')


    from .jiliang import jiliang as jiliang_blueprint

    app.register_blueprint(jiliang_blueprint,url_prefix='/jiliang')



    return app




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    avatar = db.Column(db.String(50), default="default.jpg")
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return self.username

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))