from app import create_app
import os
from app import db
import sys
import logging


class Healthiosuser(db.Model):
    __tablename__ = 'healthiosuser'


