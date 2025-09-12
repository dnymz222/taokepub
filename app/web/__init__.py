from flask import Blueprint

web = Blueprint('web', __name__)

from . import upload
from . import read
from . import allread

from . import location

from . import translate
from . import lish
from . import download
from . import coast

from . import  tide
from . import buoy
from . import mountain
