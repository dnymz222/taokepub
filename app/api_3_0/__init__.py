from flask import Blueprint

api3 = Blueprint('api3', __name__)


from . import Weather
from . import home
from . import Tide
from . import user
from . import Storm

from . import Hefeng

from . import hgt
from . import photo
from . import xinzhi

from . import openweathermap

from . import Lishu

from . import accuweather
from . import meteoblue

from . import appleweather
from . import  tianmap
from  . import Tile
from . import openmeteo
from . import noaa
from . import Aurora
from . import Astronomy
from . import Zhongkexingtu




@api3.route('/')
def welcome():
    return 'welcome you to xunquan api3'
