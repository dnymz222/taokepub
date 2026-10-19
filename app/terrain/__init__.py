import os

from flask import Blueprint, send_from_directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

terrain = Blueprint('terrain', __name__, template_folder='.')

from . import mountain


@terrain.route('/')
def welcome():
    return 'welcome you to terrian'


@terrain.route('/css/<path:filename>')
def css(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'css'), filename)


@terrain.route('/js/<path:filename>')
def js(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'js'), filename)


@terrain.route('/data/<path:filename>')
def data(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'data'), filename)
