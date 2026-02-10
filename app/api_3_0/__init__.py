from flask import Blueprint

api3 = Blueprint('api3', __name__)


from . import Weather
from . import Home
from . import Tide
from . import User
from . import Storm

from . import Hefeng

from . import Hgt
from . import Photo
from . import Xinzhi

from . import Openweathermap

from . import Lishu

from . import Accuweather
from . import Meteoblue

from . import Appleweather
from . import  Tianmap
from  . import Tile
from . import Openmeteo
from . import Noaa
from . import Aurora
from . import Astronomy
from . import Zhongkexingtu
from . import CommetEdit
from . import CAMS




@api3.route('/')
def welcome():
    return 'welcome you to xunquan api3'
