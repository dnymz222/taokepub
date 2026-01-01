#coding=utf8
from . import web
from flask import Flask,render_template,request,redirect,url_for,session,escape
from werkzeug.utils import secure_filename
from config import basedir
import os
import sys
import json
from app.CCDMStar import CCDMStar
from app.HDStar import HDStar
from app.HRStar import HRStar
from app.HIPStar import HIPStar
from app.Tycho import Tycho
from app.Tycho2 import Tycho2
from app.TychoSuppl import TychoSuppl
from app.TychoIndex import TychoIndex
from app.SAOStar import SAOStar
from app.GCVSStar import GCVSStar
from app.NGCCStar import NGCCStar
from app.Hefengtide import Hefengtide
import re
from app import db
from app.AstroEvent import AstroEvent
import xlrd
import time
import datetime
import base64
import math
from app.Camera import Camera
from app.WanggangOrder import OrderIdkey ,OrderDayKey,OrderTeamkey,ClientManagerKey,ClientNameKey,ApplyAmountKey,LoanTypeKey,MarkKey,StatusKey,ResultDescriptionKey,StatusTypeKey ,FallbackTimesKey,FallbackReasonKey,FallbackTypeKey ,AnalysisProgressKey ,RemarkKey ,MonthKey

from app.WanggangOrder import OrderIdTitle,OrderDayTitle,OrderTeamTitle ,ClientManagerTitle ,ClientNameTitle ,ApplyAmountTitle ,LoanTypeTitle ,MarkTitle,StatusTitle ,ResultDescriptionTitle ,StatusTypeTitle ,FallbackTimesTitle ,FallbackReasonTitle ,FallbackTypeTitle ,AnalysisProgressTitle ,RemarkTitle ,MonthTitle


from app.WanggangOrder import WanggangOrder
from app.WorkingDaysConfig import WorkingDaysConfig
from app.WorkingDaysModel import WorkingDaysModel
from app.MeteorShowers import MeteorShowers
from app.Comet import Comet
from app.SurfSpot import SurfSpot
import tifffile











# @web.route('/')
# def welcome():
#     return 'hello upload'

@web.route('/upload',methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.read'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''




@web.route('/shop/upload',methods=['POST', 'GET'])
def shopupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.shopread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''


@web.route('/xunpin/upload',methods=['POST', 'GET'])
def xuanpinupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.xuanpinread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''


@web.route('/tide/upload',methods=['POST', 'GET'])
def tideupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.tideread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''



@web.route('/surf/upload',methods=['POST', 'GET'])
def surfupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.surfread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route('/uploadcate',methods=['POST', 'GET'])
def uploadcate():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.cateread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route('/pintuan/upload',methods=['POST', 'GET'])
def uploadpintuan():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.pintuanread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''



@web.route('/lintie_upload',methods=['POST', 'GET'])
def lintie_upload():
    if request.method == 'POST':
       f = request.files['file']
       cate_id = request.form.get('cate_id')
       if not cate_id:
           return "no cate id"
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.lintie_read', cate_id=cate_id))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="text" name="cate_id", value="">
           <input type="submit" value="上传">
         </form>
        '''

@web.route('/upload/hipindex',methods=['POST', 'GET'])
def uploadhipindex():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readhipindex'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/hipindex")
def readhipindex():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        for lines in file_test.readlines():
            # print  lines[0:9]
            line = lines.strip('\n')
            try:
                tycindex = TychoIndex(Line=line)
                db.session.add(tycindex)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :
                db.session.rollback()
                print(e)

        return  "done"

@web.route('/upload/tycho2',methods=['POST', 'GET'])
def uploadtycho2():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readtycho2'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/tycho2")
def readtycho2():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 1
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1
            if i< 254000:
                continue
            if i >255001:
                break

            try:
                tycho2 = Tycho2(Line=line,RecordeId=i)

                # print tycho2.HIP+"\n"
                # print tycho2.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(tycho2)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"

@web.route('/upload/tycho2supplemet',methods=['POST', 'GET'])
def uploadtycho2supplemet():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readtycho2supplement'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/tycho2supplemet")
def readtycho2supplement():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 3:
            #     break


            try:
                tycho2 = TychoSuppl(Line=line,Catalog="2")

                # print tycho2.HIP+"\n"
                # print tycho2.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(tycho2)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"

@web.route('/upload/tycho',methods=['POST', 'GET'])
def uploadtycho():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readtycho'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/tycho")
def readtycho():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1
            if i < 478823:
                continue


            try:
                tycho= Tycho(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(tycho)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"




@web.route('/upload/sao',methods=['POST', 'GET'])
def uploadsao():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readsao'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/sao")
def readsao():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 239675:
            #     continue


            try:
                sao= SAOStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(sao)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"

@web.route('/upload/HR',methods=['POST', 'GET'])
def uploadHR():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readHR'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/HR")
def readHR():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 239675:
            #     continue


            try:
                sao= HRStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(sao)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"


@web.route('/upload/HD',methods=['POST', 'GET'])
def uploadHD():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readHD'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/HD")
def readHD():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break




            try:
                sao= HDStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(sao)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"

@web.route('/upload/HIP',methods=['POST', 'GET'])
def uploadHIP():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readHIP'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/HIP")
def readHIP():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 207177:
            #     continue


            try:
                hip= HIPStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(hip)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"


@web.route('/upload/CCDM',methods=['POST', 'GET'])
def uploadCCDM():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readCCDM'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/CCDM")
def readCCDM():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 207177:
            #     continue


            try:
                ccdm= CCDMStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(ccdm)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"


@web.route('/upload/GCVS',methods=['POST', 'GET'])
def uploadGCVS():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readGCVS'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/GCVS")
def readGCVS():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 207177:
            #     continue


            try:
                ccdm= GCVSStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(ccdm)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"

@web.route('/upload/NGCC',methods=['POST', 'GET'])
def uploadNGCC():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readNGCC'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/NGCC")
def readNGCC():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        # list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 207177:
            #     continue


            try:
                ccdm= NGCCStar(Line=line)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"

                db.session.add(ccdm)
                db.session.commit()
                # dict = tycindex.indexDict()
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"


@web.route('/upload/NGCC/name',methods=['POST', 'GET'])
def uploadNGCCname():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readNGCCname'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/NGCC/name")
def readNGCCname():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        list = []
        i = 0
        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines
            line = lines.strip('\n')
            i = i +1

            # if i > 10:
            #     break

            # if i < 207177:
            #     continue


            try:

                Object = line[0:35]
                Name = line[36:41]
                Comment = line[42:70]

                try:
                    ngccobejct = db.session.query(NGCCStar).filter(NGCCStar.Name == Name)[0]
                    ngccobejct.Object = Object
                    ngccobejct.Comment = Comment
                    db.session.commit()
                except Exception as e:

                    db.session.rollback()





            except Exception as e :

                db.session.rollback()


        return  "done"



@web.route('/upload/event',methods=['POST', 'GET'])
def uploadEvent():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readEvent'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''



@web.route("/read/event")
def readEvent():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        list = []
        i = 0
        month = ""


        for lines in file_test.readlines():
            # print  lines[0:9]


            line = lines.strip('\n')
            i = i +1

            month_new = line[0:3].replace(" ", "")

            if len(month_new) > 2:

                month = month_new
                continue

            if len(month) < 2:
                 continue

            line_trip = line.replace(" ","")
            if len(line_trip) < 5:
                continue


            # if i > 10:
            #     break

            # if i < 207177:
            #     continue


            try:
                event= AstroEvent(Line=line,Year="2023",Month=month,Timezone = "11",Lanuage="en",RecordIndex=i)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"
                # print i
                db.session.add(event)
                db.session.commit()

                dict = event.astroeventdict()

                list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  json.dumps(list)

@web.route("/event/en/file")
def eventenfile():
    filePath = os.path.join(basedir, 'static/astroevent')


    for parent, _, fileNames in os.walk(filePath):
        for filename in fileNames:
            if filename.find("2023_en") > -1:
                path = os.path.join(filePath,filename)
                file_test = open(path,"r")
                month = ""

                name = filename[:-4]
                splis = name.split("_")
                times = splis[2]
                timezone = ""
                if times.find("+")>-1:
                    timezone = times[1:]
                else:
                    timezone = times

                i = 0
                for lines in file_test.readlines():
                    # print  lines[0:9]


                    line = lines.strip('\n')
                    i = i + 1

                    month_new = line[0:3].replace(" ", "")

                    if len(month_new) > 2:

                        month = month_new
                        continue

                    if len(month) < 2:
                        continue

                    line_trip = line.replace(" ", "")
                    if len(line_trip) < 5:
                        continue



                    try:
                        event = AstroEvent(Line=line, Year="2023", Month=month, Timezone=timezone, Lanuage="en",
                                           RecordIndex=i)

                        db.session.add(event)
                        db.session.commit()


                    except Exception as  e:

                        db.session.rollback()


    return "done"

@web.route('/upload/event/zh',methods=['POST', 'GET'])
def uploadEvent_zh():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.readEvent_zh'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''


@web.route("/delete/zh")
def deletezh():
    try:
        events = db.session.query(AstroEvent).filter(AstroEvent.language == "zh", AstroEvent.year == "2025").all()
        for event in events:
            db.session.delete(event)
            db.session.commit()
    except Exception as e:

        db.session.rollback()
    finally:
        db.session.close()
    return "done"

@web.route("/read/event/zh")
def readEvent_zh():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, session['filename'])
        file_test = open(xlspath, 'r')
        list = []
        i = 0
        month = ""


        for lines in file_test.readlines():
            # print  lines[0:9]
            # print lines

            line = lines.strip('\n')
            line = line.replace("&nbsp;","")


            i = i +1

            header = line[0:7]
            # print "header:"+ header
            if header.find(":") > -1:
                month = line[0:2]

                continue




            # if i > 10:
            #     break



            # if i < 207177:
            #     continue


            try:
                event= AstroEvent(Line=line,Year="2026",Month=month,Timezone = "8",Lanuage="zh",RecordIndex=i)

                # print tycho2.HIP+"\n"
                # print tycho.RAdeg+"\n"
                # print tycho2.TYCId +"\n"
                # print i
                db.session.add(event)
                db.session.commit()
                #
                # dict = event.astroeventdict()
                # print dict
                # list.append(dict)
            except Exception as e :

                db.session.rollback()


        return  "done"




@web.route('/upload/camera',methods=['POST', 'GET'])
def uploadcamera():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.cameraread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/camera")
def cameraread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        result = {}

        list =[]

        for sheet in bk.sheets():
            sheet_name = sheet.name

            nrows = sheet.nrows
            for i in range(1,260):
                dict = {}
                row_value = sheet.row_values(i)

                dict["Brand"] = row_value[0]
                dict["Model"] = row_value[1]
                dict["BrandModel"] = row_value[0]+"-" + row_value[1]
                dict["MaximumPDR"] = str(row_value[2])
                dict["LowLightISO"] = str(row_value[3])
                dict["LowLightEV"] =str(row_value[4])
                dict["ReadNoiseISO"] =str(row_value[5])
                dict["SensorWidth"] =str(row_value[6])
                dict["SensorHeight"] =str(row_value[7])
                dict["PixelWidth"] = str(row_value[8])
                dict["PixelHeight"] =str( row_value[9])
                dict["Megapixels"] =str(row_value[10])
                dict["PixelPitch"] = str(row_value[11])
                dict["COC"] =str( row_value[12])
                dict["Diffraction"] = str(row_value[13])
                dict["Mount"] = str(row_value[14])
                dict["FocalLength"] =str( row_value[15])
                dict["Aperture"] =str( row_value[16])
                dict["Shutter"] = str( row_value[17])
                dict["Exposure"] =str( row_value[18])

                list.append(dict)

                insert = Camera(dict=dict)

                try:
                    db.session.add(insert)
                    db.session.commit()
                except:
                    db.session.rollback()




            db.session.close()



        return json.dumps(list)


@web.route('/lishu/upload',methods=['POST', 'GET'])
def lishuupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.lishuread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/lishu")
def lishuread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        for sheet in bk.sheets():
            sheet_name = sheet.name

            # print sheet_name

            nrows = sheet.nrows
            ncols = sheet.ncols

            row0 = sheet.row_values(0)

            Map = {}

            for i in range(1,nrows):
                row_value = sheet.row_values(i)

                code = row_value[0]
                year = row_value[1]
                month = row_value[2]
                day = row_value[3]
                holiday_description = row_value[4]
                holiday ="%d"%(row_value[5])

                if year == 2025:
                    pass
                else:
                    continue

                date ="%d-%02d-%02d"%(year, month, day)
                if "1" == holiday:
                    try:
                        db.session.query(WorkingDaysModel).filter_by(date=date, code=code).update(
                            {'public_holiday_description': holiday_description,"public_holiday":"1","working_day":"0"})
                        db.session.commit()
                    except Exception as e:

                        db.session.rollback()
                else:
                    try:
                        db.session.query(WorkingDaysModel).filter_by(date=date,code=code).update({"working_day":"1"})
                        db.session.commit()
                    except Exception as e:

                        db.session.rollback()


                print (code,year,month,day,holiday_description,holiday)
    return "done"

@web.route('/upload/comet',methods=['POST', 'GET'])
def commetupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.cometread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/comet")
def cometread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        result = []

        try:
            comets = db.session.query(Comet).all()
            for cometobject in comets:
                db.session.delete(cometobject)
                db.session.commit()
        except Exception as e:
            db.session.rollback()


        for sheet in bk.sheets():
            sheet_name = sheet.name

            # print sheet_name

            nrows = sheet.nrows
            ncols = sheet.ncols

            row0 = sheet.row_values(0)

            Map = {}

            list=[]



            for i in range(0,nrows):
                row_value = sheet.row_values(i)
                if 2 == i:
                    for j in  range(0,ncols):
                        list.append(row_value[j])
                elif i < 2:
                    pass
                else:
                    dict = {}
                    for j in range(0, ncols):
                        dict[list[j]] = row_value[j]

                    try:
                        cometobeject  = Comet(dict)
                        db.session.add(cometobeject)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()


                    result.append(dict)

    return  json.dumps(result)


@web.route('/metershower/upload',methods=['POST', 'GET'])
def metershowerupload():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.metershowerread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/metershower")
def metershowerread():
    result = []
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        for sheet in bk.sheets():
            sheet_name = sheet.name

            # print sheet_name

            nrows = sheet.nrows
            ncols = sheet.ncols

            row0 = sheet.row_values(0)

            Map = {}

            list=[]



            for i in range(0,nrows):
                row_value = sheet.row_values(i)
                if 0 == i:
                    for j in  range(0,ncols):
                        list.append(row_value[j])
                else:
                    dict = {}
                    for j in range(0, ncols):
                        dict[list[j]] = row_value[j]

                    try:
                        metershowerobeject  = MeteorShowers(dict)
                        db.session.add(metershowerobeject)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                    result.append(dict)

    return json.dumps(result)





@web.route("/read/surf")
def surfread():
    result = []
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        for sheet in bk.sheets():
            sheet_name = sheet.name

            # print sheet_name

            nrows = sheet.nrows
            ncols = sheet.ncols

            row0 = sheet.row_values(0)

            Map = {}

            list=[]

            # try:
            #     db.session.query(SurfSpot).filter(SurfSpot.spot_id>99999).delete()
            #     db.session.commit()
            #
            #
            #
            # except Exception, e:
            #     db.session.rollback()

            for i in range(1,nrows):
                row_value = sheet.row_values(i)

                try:
                    spot_id = int(row_value[0])
                    if spot_id > 100020:
                        surfspotlocation = SurfSpot(spot_id=int(row_value[0]),spot_name=row_value[1],lat=row_value[2],lng=row_value[3])
                    else:
                        surfspotlocation = SurfSpot(spot_id=int(row_value[0]), spot_name=row_value[1], lat=row_value[3],
                                                    lng=row_value[2])
                    db.session.add(surfspotlocation)
                    db.session.commit()
                except Exception as e:

                    db.session.rllback()

    return json.dumps(result)



@web.route("/read/tif/2")
def readtif_2():
    upload_path = os.path.join(basedir, 'static/uploads', "ETOPO1_Ice_g_geotiff.tif")
    image  = tifffile.imread(upload_path)

    height =  image.shape[0]/60
    width   =image.shape[1]/60

    filename = "world_ge_0" + ".json"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')





    list = []
    f.write("{\n")
    count = 0
    for i in  range(0,height):

        for j in range(0,width):
            # if i==0 and j ==0 :
            #     pass
            # else:
                # f.write(",")
            # f.write("{\n")
            # f.write('{')

            # count = 0
            for m in  range(0,5):
                for n  in range(0,5):
                    v_t = 0
                    v_list = []
                    v_a = 0
                    for x in  range(0,6):
                        imagerow = image[i*60+m*6+x*3+1]

                        # print  imagerow

                        for y in range(0,6):
                            v = imagerow[j*60+n*6+y*3+1]


                            if v  < 0 and v > -200:
                               v_a = v_a + 1
                               # print v
                               # print v
                            # if v> 0.02:
                            #     v_a = v_a +2
                            # elif v > 0.01:
                            #     v_a = v_a +1
                            #
                            v_list.append(toptvtype(v))

                    if v_a>2:
                        if count > 0 :
                            f.write(",")
                        count = count + 1
                        # f.write("{\n")
                        f.write('"%s":%s\n' %(str((i*360+j)*36+m*6+n), str(v_list)))
                        # f.write("}\n")



            # f.write("}\n")




    f.write("}\n")





    return "done"



@web.route("/read/tif")
def readtif():
    upload_path = os.path.join(basedir, 'static/uploads', "ETOPO1_Ice_g_geotiff.tif")
    image  = tifffile.imread(upload_path)

    height =  image.shape[0]/60
    width  =  image.shape[1]/60

    filename = "world_tpxo" + ".json"

    txt_path = os.path.join(basedir, 'static/uploads', filename)
    f = open(txt_path, 'w')


    list = []
    f.write("[")
    # count = 0
    for i in  range(0,height):

        for j in range(0,width):
            if i==0 and j ==0 :
                pass
            else:
                f.write(",")
            # f.write("{\n")
            f.write('{')

            count = 0
            for m in  range(0,5):
                for n  in range(0,5):
                    v_t = 0
                    v_list = []
                    v_a = 0
                    for x in  range(0,6):
                        imagerow = image[i*60+m*12+x*2+0]
                        imagerow1 = image[i * 60 + m * 12 + x * 2 + 1]

                        for y in range(0,6):
                            v1 = imagerow[j*60+n*12+y*2+0]
                            v2 = imagerow[j * 60 + n * 12 + y * 2 + 1]
                            v3 = imagerow1[j * 60 + n * 12 + y * 2 + 0]
                            v4 = imagerow1[j * 60 + n * 12 + y * 2 + 1]


                            v= (v1 + v2 + v3 + v4)/4


                            if v < 0 and v > -200:
                                v_a = v_a + 1

                            v_list.append(toptvtype(v))

                    if v_a>0:
                        if count > 0:
                            f.write(",")
                        count = count + 1
                        # f.write("{\n")
                        f.write('"%s":%s\n' %(str(m*5+n), str(v_list)))
                        # f.write("}\n")



            f.write("}\n")




    f.write("]\n")





    return "done"


# @web.route("/read/vnl/tif")
# def readvnltif():
#     upload_path = os.path.join(basedir, 'static/uploads', "VNL_v2_npp_2020_global_vcmslcfg_c202101211500.average.tif")
#     image  = tifffile.imread(upload_path)
#     print  image.shape
#     height =  image.shape[0]/240
#     width   =image.shape[1]/240
#     print height
#     print width
#     print image[50*height][30*width]
#     # for i in  range(49*height,51*height):
#     #     for j in  range(299*width,301*width):
#     #         print  image[i][j]
#
#
#
#
def tiflat(i):
    return  85 - i/17406.0*145.05
def tiflong(j):
    return -180 + j/43200.0*360


def tifvtype(v):
    if v < 0.01:
        return 0
    n = v/0.01;
    a = math.log(n,2)
    b = int(a+1)
    if b > 13:
        b = 13
    return b


def toptvtype(v):
    if v > 0:
        return 0

    elif v > -10:
        return 1
    elif v > -20:
        return 2
    elif v > -40:
        return 3
    elif v > -60:
        return 4
    elif v > -80:
        return  5
    elif v > -100:
        return 6
    elif v > -200:
        return 7
    else:
        return 8



@web.route('/upload/wannasurf',methods=['POST', 'GET'])
def uploadwannasurf():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.wannasurfread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''

@web.route("/read/wannasurf")
def wannasurfread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))
        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        result = {}

        list =[]

        for sheet in bk.sheets():
            sheet_name = sheet.name

            # print sheet_name

            nrows = sheet.nrows
            ncols = sheet.ncols

            row0 = sheet.row_values(0)

            Map = {}

            keylist=[]
            header = sheet.row_values(0)
            for k in range(0,ncols):
                keylist.append(header[k])




            for i in range(1,nrows):
                row_value = sheet.row_values(i)
                dict = {}
                for k in range(0, ncols):
                    key = keylist[k]
                    dict[key] = row_value[k]
                lat = dict["lat"]
                if len(lat) > 0:
                    list.append(dict)
                else:
                    print (row_value[0])


        jpath = os.path.join(uploadath,"surfchina.json")
        f = open(jpath,"w")
        f.write(json.dumps(list))
        f.close()




    return "done"


@web.route('/upload/hefeng',methods=['POST', 'GET'])
def uploadhefeng():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.hefengread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''


@web.route('/hefeng/read')
def hefengread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))

        # bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")
        # sh = bk.sheets()[0]
        # nrows = sh.nrows
        # ncols = sh.ncols
        list = []
        #
        #
        f = open(xlspath,"r")

        lines = f.readlines()

        i = 0
        for line in lines:
            if i > 1:
                try:
                    dict = {}


                    row_data = line.decode('utf-8', 'ignore').split(",")
                    dict['locationId'] = row_data[0]
                    dict['localName'] = row_data[1]
                    dict['englishName'] = row_data[2]
                    dict['chineseName'] = row_data[3]
                    dict["latitude"] = row_data[4]
                    dict["longitude"] = row_data[5]
                    dict["code"] = row_data[7].strip()
                    if dict["code"].find("CN")> -1 or dict["code"].find("HK")>-1 or dict["code"].find("MO")>-1:
                        list.append(dict)
                        try:
                            insert = Hefengtide(dict)
                            db.session.add(insert)
                            db.session.commit()
                        except Exception as e:

                            db.session.rollback()

                except Exception as e:
                    print ("error")
                    print (e)

            i = i +1

        return json.dumps(list)

@web.route('/upload/chaoxibiao',methods=['POST', 'GET'])
def uploadchaoxibiao():
    if request.method == 'POST':
       f = request.files['file']
       upload_path = os.path.join(basedir, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
       f.save(upload_path)
       session['filename'] = secure_filename(f.filename)
       return redirect(url_for('web.chaoxibiaoread'))
    return  '''
         <form action="" enctype='multipart/form-data' method='POST'>
           <input type="file" name="file">
           <input type="submit" value="上传">
         </form>
        '''
@web.route('/chaoxibiao/read')
def chaoxibiaoread():
    if 'filename' in session:
        uploadath = os.path.join(basedir, 'static/uploads')
        xlspath = os.path.join(uploadath, escape(session['filename']))

        bk = xlrd.open_workbook(xlspath, encoding_override="utf-8")

        sh = bk.sheets()[0]
        nrows = sh.nrows
        ncols = sh.ncols
        list = []
        portlist = []
        mainportlist= []
        for i in range(1, nrows):
            row_value = sh.row_values(i)
            dict = {}
            dict["number"] =namevalue(row_value[0])
            dict["name"] = row_value[1]
            dict["longitude"] = locationvalue(str(row_value[3]))
            dict["latitude"] = locationvalue(str(row_value[4]))
            dict["area"] = row_value[2]
            dict["mainport"] = row_value[5]
            if row_value[5] not in portlist:
                portlist.append(row_value[5])

            dict["type"] = 1 #1.半日 2.全日
            vlist = []
            vlist.append(timevalue(str(row_value[6])))
            vlist.append(timevalue(str(row_value[7])))
            vlist.append(str(row_value[8]))
            vlist.append(str(row_value[9]))
            vlist.append(timevalue(str(row_value[10])))
            vlist.append(timevalue(str(row_value[11])))
            vlist.append(str(row_value[12]))
            vlist.append(str(row_value[13]))
            vlist.append(str(row_value[14]))
            vlist.append(str(row_value[15]))
            vlist.append(str(row_value[17]))
            dict["value"] = vlist
            dict["datum"] = namevalue(row_value[16])
            if dict["mainport"].find("主港")<0:
                list.append(dict)
            else:
                mainportlist.append(dict)
        sh1 = bk.sheets()[1]
        nrows2 = sh1.nrows

        for i in range(2, nrows2):
            row_value = sh1.row_values(i)
            dict = {}
            dict["number"] = namevalue(row_value[0])
            dict["name"] = row_value[1]
            dict["longitude"] = locationvalue(str(row_value[3]))
            dict["latitude"] = locationvalue(str(row_value[4]))
            dict["area"] = row_value[2]
            dict["mainport"] = row_value[5]
            if row_value[5] not in portlist:
                portlist.append(row_value[5])
            dict["type"] = 2 #1.半日 2.全日
            vlist = []
            vlist.append(timevalue(str(row_value[6])))
            vlist.append(timevalue(str(row_value[7])))
            vlist.append(str(row_value[8]))
            vlist.append(str(row_value[9]))
            vlist.append(timevalue(str(row_value[10])))
            vlist.append(str(row_value[11]))
            vlist.append(timevalue(str(row_value[12])))
            vlist.append(str(row_value[13]))
            vlist.append(timevalue(str(row_value[14])))
            vlist.append(timevalue(str(row_value[15])))

            vlist.append(str(row_value[16]))
            vlist.append(str(row_value[17]))
            vlist.append(str(row_value[18]))
            vlist.append(str(row_value[19]))
            vlist.append(str(row_value[21]))
            dict["datum"] =  namevalue(row_value[20])
            dict["value"] = vlist
            if dict["mainport"].find("主港")<0:
                list.append(dict)
            else:
                mainportlist.append(dict)


        path = os.path.join(basedir, "static/hefengtide", "chaoxibiao.json")
        f = open(path,"w")
        f.write(json.dumps(list))
        f.close()

        mpath = os.path.join(basedir, "static/hefengtide", "chaoxibia01.json")
        mf = open(mpath, "w")
        mf.write(json.dumps(mainportlist))
        mf.close()

        print ("\n")
        print ("{")
        sh2 = bk.sheets()[2]
        nrows3 = sh2.nrows
        for i in range(1,nrows3):
            row_value = sh2.row_values(i)
            string = ""
            for j in range(0,14):
                string = string + str(int(row_value[j]))
                string  = string +","
            print (string)
        print ("}")

        print ("\n")
        print ("hmm4")
        print ("{")
        sh3 = bk.sheets()[3]
        nrows4 = sh3.nrows
        for i in range(2, nrows4):
            row_value = sh3.row_values(i)
            string = ""
            for j in range(1, 20):
                string = string + str(int(row_value[j]))
                string = string + ","
            print (string)
        print ("}")

        return json.dumps(list)


def namevalue(name):
    try:
        return str(int(name))
    except Exception as e:
        return name

def locationvalue(location):
    if location.strip().find(" ")> -1:
        list = location.strip().split(" ")
        value = int(list[0]) + int(list[1]) / 60.0

        return str(value)
    else:
        return location

def timevalue(time):
    if time.strip().find(" ")> -1:
        list = time.strip().split(" ")
        value = int(list[0]) * 60 + int(list[1])
        return str(value)
    else:
        return time

