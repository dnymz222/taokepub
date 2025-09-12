from app import create_app
import os
from app import db
import sys
import logging


class Healthandroiduser(db.Model):
    __tablename__ = 'healthandroiduser'
    