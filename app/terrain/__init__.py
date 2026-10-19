from flask import Blueprint

terrain= Blueprint('terrain', __name__)

from . import mountain


@terrain.route('/')
def welcome():
    return 'welcome you to terrian'
