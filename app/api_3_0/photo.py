#coding=utf8
from . import api3
from app.utils.constvalue import x_code,x_data,x_meesage
from app import db
import json
from  app.Camera import Camera


@api3.route("/camera/npf")
def camaranpf():
    result = {}
    list = []

    try:
        cameras = db.session.query(Camera).all()
        for cameraobject in cameras:
            dict = cameraobject.CameraDict()
            list.append(dict)
        result[x_code] = 200
        result[x_data] = list
    except Exception as e:

        result[x_meesage] = "%s"%e
        result[x_code] = 201
        db.session.rollback()
    finally:
        db.session.close()

    return json.dumps(result)

