from flask import Blueprint

api3 = Blueprint('api3', __name__)


from . import Home
from . import Hgt
from . import Photo

from . import Meteoblue
from  . import Tile
from . import Tide
from . import Aurora
from . import SolarEclipse
from . import Storm
from . import Lishu



@api3.route('/')
def welcome():
    return 'welcome you to xunquan api3'
