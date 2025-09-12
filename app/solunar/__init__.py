from flask import Blueprint

solunar = Blueprint('solunar', __name__)


from . import  search
from . import  web
from . import nearby