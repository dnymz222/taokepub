from flask import Blueprint

h5= Blueprint('h5', __name__)

from . import detailh5


@h5.route('/')
def welcome():
    return 'welcome you to xunquan h5'
