from flask import Blueprint

solunar = Blueprint('solunar', __name__)


from . import  Search
from . import  Web
from . import Nearby