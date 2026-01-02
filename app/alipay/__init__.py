from flask import Blueprint

alipay = Blueprint('alipay', __name__)

from . import Fishweatherpay
from . import Tidepay
from . import Common
from . import Solunarpay
from . import Astronomypay
from . import Meteopay



@alipay.route("/")
def alipayroute():
    return "wecome to alipay"