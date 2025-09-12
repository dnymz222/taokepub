from flask import Blueprint

alipay = Blueprint('alipay', __name__)

from . import fishweatherpay
from . import tidepay
from . import common
from . import solunarpay
from . import astronomypay
from . import Meteopay



@alipay.route("/")
def alipayroute():
    return "wecome to alipay"