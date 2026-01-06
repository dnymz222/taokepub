from flask import Blueprint

api3 = Blueprint('api3', __name__)


from . import home
from . import hgt
from . import photo

from . import meteoblue
from  . import Tile
from . import Tide
from . import Aurora
from . import SolarEclipse
from . import Storm



@api3.route('/')
def welcome():
    return 'welcome you to xunquan api3'
