from app import create_app
import os
from app import db
import sys
import logging

class Camera(db.Model):
    __tablename__ = 'Camera'
    BrandModel = db.Column(db.String(100), primary_key=True)
    Brand = db.Column(db.String(32), unique=False)
    Model = db.Column(db.String(64), unique=False)
    MaximumPDR = db.Column(db.String(20), unique=False)
    LowLightISO = db.Column(db.String(20), unique=False)
    LowLightEV = db.Column(db.String(20), unique=False)
    ReadNoiseISO = db.Column(db.String(20), unique=False)
    SensorWidth = db.Column(db.String(20), unique=False)
    SensorHeight = db.Column(db.String(20), unique=False)
    PixelWidth = db.Column(db.String(20), unique=False)
    PixelHeight = db.Column(db.String(20), unique=False)
    Megapixels = db.Column(db.String(20), unique=False)
    PixelPitch = db.Column(db.String(20), unique=False)
    CoC = db.Column(db.String(20), unique=False)
    Diffraction = db.Column(db.String(20), unique=False)
    Mount = db.Column(db.String(20), unique=False)
    FocalLength = db.Column(db.String(20), unique=False)
    Aperture = db.Column(db.String(20), unique=False)
    Shutter = db.Column(db.String(20), unique=False)
    Exposure = db.Column(db.String(20), unique=False)


    def __init__(self,dict):
        self.BrandModel = dict["BrandModel"]
        self.Brand = dict["Brand"]
        self.Model = dict["Model"]
        self.MaximumPDR = dict["MaximumPDR"]
        self.LowLightISO = dict["LowLightISO"]
        self.LowLightEV = dict["LowLightEV"]
        self.ReadNoiseISO = dict["ReadNoiseISO"]
        self.SensorWidth = dict["SensorWidth"]
        self.SensorHeight = dict["SensorHeight"]
        self.PixelWidth = dict["PixelWidth"]
        self.PixelHeight = dict["PixelHeight"]
        self.Megapixels = dict["Megapixels"]
        self.PixelPitch = dict["PixelPitch"]
        self.CoC = dict["COC"]
        self.Diffraction = dict["Diffraction"]
        self.Mount = dict["Mount"]
        self.FocalLength = dict["FocalLength"]
        self.Aperture = dict["Aperture"]
        self.Shutter = dict["Shutter"]
        self.Exposure = dict["Exposure"]

    def CameraDict(self):
        dict = {}
        dict["Brand"] = self.Brand
        dict["Model"] = self.Model
        dict["MaximumPDR"] = self.MaximumPDR
        dict["LowLightISO"] = self.LowLightISO
        dict["LowLightEV"] = self.LowLightEV
        dict["ReadNoiseISO"] = self.ReadNoiseISO
        dict["SensorWidth"]  =self.SensorWidth
        dict["SensorHeight"] = self.SensorHeight
        dict["PixelWidth"] = self.PixelWidth
        dict["PixelHeight"] = self.PixelHeight
        dict["Megapixels"]  = self.Megapixels
        dict["PixelPitch"] = self.PixelPitch
        dict["COC"] = self.CoC
        dict["Diffraction"] = self.Diffraction
        dict["Mount"] = self.Mount
        dict["FocalLength"] = self.FocalLength
        dict["Aperture"] = self.Aperture
        dict["Shutter"]  =self.Shutter
        dict["Exposure"]  = self.Exposure

        return dict



