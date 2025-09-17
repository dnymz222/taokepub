#  #coding=utf8
# import os.path
# from . import api3
# from app.utils.constvalue import x_code,x_data,x_hasnext,x_meesage
#
# from flask import request
#
# import datetime
# import urllib
#
#
# import json
#
# import math
#
#
# import pytz
# from pymeeus.Epoch import Epoch
# from pymeeus.Sun import Sun
# from pymeeus.Moon import Moon
#
# import pymeeus.Coordinates
#
# from datetime import datetime, timezone
# import time
# from config import basedir
# from PIL import Image as PILImage
#
# from urllib.request import urlopen
#
# from matplotlib.colors import LinearSegmentedColormap
# import matplotlib.pyplot as plt
# import numpy as np
#
# import cartopy.crs as ccrs
#
# from cartopy.feature.nightshade import Nightshade
#
# from flask import send_file
#
# from cartopy.io.shapereader import Reader
# import paramiko
# import matplotlib.gridspec as gridspec
#
# import geopandas as gpd
# from app.utils.constvalue import astronomyobserver_ip, astronomyobserver_password
#
# tz = pytz.timezone("GMT")
#
# @api3.route('/aurora/minutes/old')
# def auroraminutesold():
#
#      result = {}
#
#      url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          dict = json.loads(content)
#          coordinates = dict["coordinates"]
#          ftime = dict["Forecast Time"]
#
#
#
#          date = datetime.strptime(ftime, "%Y-%m-%dT%H:%M:%SZ")
#
#
#          tz_offset = timezonfoffset()
#
#          forecast_time = int(date.timestamp()) + tz_offset
#          dict["forecast_time"] = forecast_time
#
#          dict["solunar"] = pymeeusastrodict(forecast_time)
#
#          list = []
#          for coordinate in coordinates:
#              value = coordinate[2]
#              latitude = coordinate[1]
#              if value > 0 and abs(latitude) > 10:
#                  list.append(coordinate)
#
#          coordinatedict = {}
#          # dict["coordinates"] = list
#          for coordinate in list:
#              lng  = coordinate[0]
#              lat = coordinate[1]
#              v = coordinate[2]
#              coordinatedict[str(lat * 360 + lng)] = v
#          dict["coordinates"] = coordinatedict
#
#          result[x_code] = 200
#          result[x_data] = dict
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#
#
# def auroraprobabilitywith(hip):
#
#      if hip < 1:
#          return  0
#      elif hip > 100:
#
#          return 100
#      else:
#          p =  int(math.floor(hip))
#          return p
#
# @api3.route("/aurora/minutes")
# def auroraminutes():
#      longitude_factor = 0.9754
#      latitude_factor = 0.8754
#      latitude_north = 69.54
#      latitude_south = -69.54
#      result= {}
#      try:
#          result_hpi = json.loads(aurorahpiminutes())
#          print(result_hpi)
#          datalist= result_hpi[x_data]
#          n = len(datalist)
#          latest = datalist[n-1]
#          forecast_time = latest["forecast_time"]
#          south_hpi = latest["south_hpi"]
#          north_hpi = latest["north_hpi"]
#          datadict = {}
#          datadict["forecast_time"] = forecast_time
#          datadict["Observation Time"] = ""
#          datadict["Forecast Time"] = ""
#          datadict["type"] = ""
#          solunardict = pymeeusastrodict(forecast_time)
#          datadict["solunar"] = solunardict
#
#          true_solar_time  =  solunardict["true_solar_time"]
#
#
#
#          if true_solar_time > 86400:
#              true_solar_time = true_solar_time - 86400
#          elif true_solar_time < 0:
#              true_solar_time = true_solar_time + 86400
#
#          if true_solar_time > 86400:
#              true_solar_time = true_solar_time - 86400
#          elif true_solar_time < 0:
#              true_solar_time = true_solar_time + 86400
#
#          longitude_center = (86400-true_solar_time) / 240.0 - 11
#
#
#          if longitude_center < -180:
#              longitude_center = longitude_center + 360
#          if longitude_center > 180:
#              longitude_center = longitude_center - 360
#
#          if longitude_center < -180:
#              longitude_center = longitude_center + 360
#          if longitude_center > 180:
#              longitude_center = longitude_center - 360
#
#
#
#
#          coorinatesdict = {}
#
#          for lng in range(-180,180):
#              for lat in range(-90,90):
#                  deltalng = math.fabs(lng - longitude_center)
#                  if deltalng > 180:
#                      deltalng = 360 - deltalng
#                  if lat > 0:
#                      lnghpi = north_hpi *pow(longitude_factor,deltalng)
#                      deltalat = math.fabs(latitude_north - lat)
#
#                      lathpi = lnghpi * pow(latitude_factor,deltalat)
#                      probability = auroraprobabilitywith(lathpi)
#                      if probability > 1:
#                          coorinatesdict[str(lat * 360 + lng)] = int(math.floor(probability))
#                  else:
#                      lnghpi = south_hpi * pow(longitude_factor, deltalng)
#                      deltalat = math.fabs(latitude_south - lat)
#                      lathpi = lnghpi * pow(latitude_factor, deltalat)
#                      probability = auroraprobabilitywith(lathpi)
#                      if probability > 1:
#                          coorinatesdict[str(lat * 360 + lng)] = int(math.floor(probability))
#
#
#          datadict["coordinates"] = coorinatesdict
#          result[x_code] = 200
#          result[x_data] = datadict
#
#          return json.dumps(result)
#
#
#      except Exception as e:
#          print(e)
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#
# def auroraovalminutes(latest):
#      longitude_factor = 0.99
#      latitude_factor = 0.87
#      latitude_north = 69.54
#      latitude_south = -69.54
#      try:
#
#              forecast_time = latest["forecast_time"]
#              south_hpi = latest["south_hpi"]
#              north_hpi = latest["north_hpi"]
#              north_png = latest["north_png"]
#              south_png = latest["south_png"]
#
#              datadict = {}
#              datadict["forecast_time"] = forecast_time
#              datadict["Observation Time"] = ""
#              datadict["Forecast Time"] = ""
#              datadict["type"] = ""
#              solunardict = pymeeusastrodict(forecast_time)
#              datadict["solunar"] = solunardict
#
#              true_solar_time  =  solunardict["true_solar_time"]
#
#
#
#
#
#              if true_solar_time > 86400:
#                  true_solar_time = true_solar_time - 86400
#              elif true_solar_time < 0:
#                  true_solar_time = true_solar_time + 86400
#
#              if true_solar_time > 86400:
#                  true_solar_time = true_solar_time - 86400
#              elif true_solar_time < 0:
#                  true_solar_time = true_solar_time + 86400
#
#              longitude_center = (86400-true_solar_time) / 240.0 + 11
#
#
#              if longitude_center < -180:
#                  longitude_center = longitude_center + 360
#              if longitude_center > 180:
#                  longitude_center = longitude_center - 360
#
#              if longitude_center < -180:
#                  longitude_center = longitude_center + 360
#              if longitude_center > 180:
#                  longitude_center = longitude_center - 360
#
#
#
#
#              coorinateslsit = []
#
#              if longitude_center < 0:
#                  longitude_center = longitude_center + 360
#
#
#              for lng in range(0,360):
#                  for lat in range(-90,91):
#                      deltalng = math.fabs(lng - longitude_center)
#                      if deltalng > 180:
#                          deltalng = 360 - deltalng
#                      if lat < 0:
#                          lnghpi = south_hpi * pow(longitude_factor, deltalng)
#                          deltalat = math.fabs(latitude_south - lat)
#                          lathpi = lnghpi * pow(latitude_factor, deltalat)
#                          probability = auroraprobabilitywith(lathpi)
#                          coorinateslsit.append([lng,lat,probability])
#
#
#
#                      else:
#                          lnghpi = north_hpi * pow(longitude_factor, deltalng)
#                          deltalat = math.fabs(latitude_north - lat)
#
#                          lathpi = lnghpi * pow(latitude_factor, deltalat)
#                          probability = auroraprobabilitywith(lathpi)
#                          coorinateslsit.append([lng,lat,probability])
#
#
#
#
#              dt = latest["forecast_time_str"]
#              auroradict = {}
#              auroradict["Forecast Time"] = dt
#              auroradict["coordinates"] = coorinateslsit
#
#              auroraoval(0,north_png,north_hpi,longitude_center,auroradict)
#
#              auroraoval(1,south_png,south_hpi,longitude_center,auroradict)
#
#
#
#      except Exception as e:
#          print(e)
#
# @api3.route('/aurora/hour')
# def aurorhour():
#
#      result = {}
#      url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = json.loads(content)
#          datalist = []
#
#          n = len(list)
#
#          now = datetime.now()
#          nowtimestamp = now.timestamp()
#
#          for i in range(1,n):
#              vlist = list[i]
#              datadict = {}
#              datadict["time_tag"] = vlist[0]
#              datadict["kp"] = vlist[1]
#              datadict["observed"] = vlist[2]
#              datadict["noaa_scale"] = vlist[3]
#
#              ftime = vlist[0]
#              date = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")
#
#              tz_offset = timezonfoffset()
#
#              forecast_time = int(date.timestamp()) + tz_offset
#
#              if forecast_time > nowtimestamp - 3600 * 4:
#                  datadict["solunar"] = pymeeusastrodict(forecast_time)
#                  datadict["forecast_time"] = forecast_time
#                  datalist.append(datadict)
#                  datadict1 = {}
#                  datadict1["solunar"] = pymeeusastrodict(forecast_time + 3600)
#                  datadict1["forecast_time"] = forecast_time + 3600
#                  datalist.append(datadict1)
#
#                  datadict2 = {}
#                  datadict2["solunar"] = pymeeusastrodict(forecast_time + 3600 * 2)
#                  datadict2["forecast_time"] = forecast_time + 3600 * 2
#                  datalist.append(datadict2)
#
#
#
#          result[x_code] = 200
#          result[x_data] = datalist
#
#
#
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# @api3.route('/aurora/dst')
# def aurordst():
#
#      result = {}
#      url = "https://services.swpc.noaa.gov/products/kyoto-dst.json"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = json.loads(content)
#          datalist = []
#
#          n = len(list)
#
#
#          for i in range(1,n):
#              vlist = list[i]
#              datadict = {}
#              datadict["time_tag"] = vlist[0]
#              datadict["dst"] = int(vlist[1])
#
#              ftime = vlist[0]
#              date = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")
#
#              tz_offset = timezonfoffset()
#
#              forecast_time = int(date.timestamp()) + tz_offset
#
#              datadict["time"] = forecast_time
#              datalist.append(datadict)
#
#
#
#          result[x_code] = 200
#          result[x_data] = datalist
#
#
#
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# @api3.route('/aurora/kp')
# def aurorkp():
#
#      result = {}
#      url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = json.loads(content)
#          datalist = []
#
#          n = len(list)
#
#          now = datetime.now()
#          nowtimestamp = now.timestamp()
#
#          for i in range(1,n):
#              vlist = list[i]
#              datadict = {}
#
#              datadict["kp"] = float(vlist[1])
#              datadict["a_running"] = int(vlist[2])
#              datadict["station_count"] = int(vlist[3])
#
#              ftime = vlist[0][:-4]
#              date = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")
#
#              tz_offset = timezonfoffset()
#
#              forecast_time = int(date.timestamp()) + tz_offset
#
#
#
#
#
#
#
#          result[x_code] = 200
#          result[x_data] = datalist
#
#
#
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#  # @api3.route('/aurora/day')
#  # def auroraday():
#  #
#  #     result = {}
#  #
#  #     url = "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt"
#  #     try:
#  #         req = urllib.request.Request(url)
#  #         response = urllib.request.urlopen(req)
#  #         content = response.read()
#  #         list = []
#  #         beigain = False
#  #
#  #         for line in content.splitlines():
#  #             text = line.decode("utf8").strip()
#  #
#  #             if beigain:
#  #                 tlist = text.split(" ")
#  #                 for t in tlist:
#  #                     if len(t) > 0:
#  #                         list.append(t)
#  #             else:
#  #                if text.find("NOAA Kp index forecast") > -1:
#  #                    beigain = True
#  #         dict  ={}
#  #         now = datetime.now(tz)
#  #         year = now.year
#  #         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
#  #          "Aug", "Sep", "Oct", "Nov", "Dec"]
#  #         monthstr = list[0]
#  #         month = 1
#  #         for i in range(1,13):
#  #             m = months[i-1]
#  #             if m == monthstr:
#  #                 month = i
#  #                 break
#  #         day = int(list[1])
#  #
#  #         startdate = datetime(year, month, day,0,0,0,tzinfo=tz)
#  #
#  #         starttime = int(startdate.timestamp())
#  #         timelist = []
#  #         for i in range(0,24):
#  #             timelist.append(starttime + i * 3600 * 3)
#  #
#  #         datalist = []
#  #         for i in range(0,8):
#  #             datalist.append(float(list[7 + 4 * i]))
#  #         for i in range(0,8):
#  #             datalist.append(float(list[8 + 4 * i]))
#  #         for i in range(0,8):
#  #             datalist.append(float(list[9 + 4 * i]))
#  #         dict["kp"] = datalist
#  #         dict["time"] = timelist
#  #         result[x_code] = 200
#  #         result[x_data] = dict
#  #         return json.dumps(result)
#  #     except Exception as e:
#  #
#  #         result[x_code] = 201
#  #         result[x_meesage] = "%s"%e
#  #         return json.dumps(result)
#
#
# @api3.route('/aurora/hpi/minutes')
# def aurorahpiminutes():
#
#      result = {}
#
#
#      url = "https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = []
#          beigain = False
#
#          tz_offset = timezonfoffset()
#
#          now = datetime.now()
#          nowtimestamp = now.timestamp()
#
#          for line in content.splitlines():
#              text = line.decode("utf8").strip()
#
#              if beigain:
#                  datadict = {}
#                  tlist = text.split(" ")
#                  vlist = []
#                  for t in tlist:
#                      if len(t.strip()) > 0:
#                          vlist.append(t.strip())
#                  if len(vlist) > 3:
#                      odate = datetime.strptime(vlist[0].strip(), "%Y-%m-%d_%H:%M")
#                      datadict["observe_time"] = int(odate.timestamp()) + tz_offset
#
#                      fdate = datetime.strptime(vlist[1].strip(), "%Y-%m-%d_%H:%M")
#                      datadict["forecast_time"] = int(fdate.timestamp()) + tz_offset
#
#                      otime_str = odate.strftime("%Y-%m-%d_%H%M")
#                      datadict["north_url"] = "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_N_" + otime_str + ".webp"
#                      datadict["south_url"] = "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_S_" + otime_str + ".webp"
#
#                      datadict["north_png"] = "aurora_N_"+otime_str
#                      datadict["south_png"] = "aurora_S_" + otime_str
#
#
#
#                      datadict["south_hpi"] = int(vlist[3])
#                      datadict["north_hpi"] = int(vlist[2])
#                      datadict["forecast_time_str"] = vlist[1] +":00Z"
#
#                      if datadict["forecast_time"] > nowtimestamp - 60:
#                          list.append(datadict)
#
#
#
#
#              else:
#                 if text.find("#-------") > -1:
#                     beigain = True
#
#
#
#
#
#          result[x_code] = 200
#          result[x_data] = list
#          return json.dumps(result)
#      except Exception as e:
#          print(e)
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# @api3.route('/aurora/hpi')
# def aurorahpi():
#
#      result = {}
#
#      url = "https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = []
#          beigain = False
#
#          tz_offset = timezonfoffset()
#
#          now = datetime.now()
#          nowtimestamp = now.timestamp()
#
#          for line in content.splitlines():
#              text = line.decode("utf8").strip()
#
#              if beigain:
#                  datadict = {}
#                  tlist = text.split(" ")
#                  vlist = []
#                  for t in tlist:
#                      if len(t.strip()) > 0:
#                          vlist.append(t.strip())
#                  if len(vlist) > 3:
#                      odate = datetime.strptime(vlist[0].strip(), "%Y-%m-%d_%H:%M")
#                      datadict["observe_time"] = int(odate.timestamp()) + tz_offset
#
#                      fdate = datetime.strptime(vlist[1].strip(), "%Y-%m-%d_%H:%M")
#                      datadict["forecast_time"] = int(fdate.timestamp()) + tz_offset
#
#                      otime_str = odate.strftime("%Y-%m-%d_%H%M")
#                      datadict["north_url"] = "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_N_" + otime_str + ".webp"
#                      datadict["south_url"] = "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_S_" + otime_str + ".webp"
#
#                      datadict["north_png"] = "aurora_N_"+otime_str
#                      datadict["south_png"] = "aurora_S_" + otime_str
#
#
#
#                      datadict["south_hpi"] = int(vlist[3])
#                      datadict["north_hpi"] = int(vlist[2])
#                      datadict["forecast_time_str"] = vlist[1] +":00Z"
#
#                      if datadict["forecast_time"] > nowtimestamp - 60:
#                          north_file = os.path.join(basedir, "static/aurora/oval", datadict["south_png"] + ".webp")
#                          if os.path.exists(north_file):
#                              list.append(datadict)
#                          else:
#                              pass
#
#
#
#              else:
#                 if text.find("#-------") > -1:
#                     beigain = True
#
#
#
#
#
#          result[x_code] = 200
#          result[x_data] = list
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#
# @api3.route("/aurora/hpi/oval/task")
# def hpitask():
#      while 1> 0:
#          aurorahpioval()
#          time.sleep(200)
#
#
# def aurorahpioval():
#
#      result = {}
#
#      url = "https://www.astronomyobserver.net/api/v3.0/aurora/hpi/minutes"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          reusltdict = json.loads(content)
#          list = reusltdict[x_data]
#
#          filelist = []
#
#          # for datadict in list:
#          #     north_file = os.path.join(basedir, "static/Aurora/oval", datadict["south_png"] + ".webp")
#          #     if os.path.exists(north_file):
#          #         pass
#          #     else:
#          #         auroraovalminutes(datadict)
#          #         filelist.append(datadict["south_png"])
#          #         filelist.append(datadict["north_png"])
#
#
#          n = len(list)
#          latest = list[n-1]
#          # latest["north_png"] = "aurora_N_" + "latest"
#          # latest["south_png"] = "aurora_S_" + "latest"
#          auroraovalminutes(latest)
#          filelist.append(latest["south_png"])
#          filelist.append(latest["north_png"])
#
#          filelist.append("aurora_N_" + "latest")
#          filelist.append("aurora_S_" + "latest")
#
#          remote_host = astronomyobserver_ip
#          remote_port = 22
#          remote_username = "root"
#          remote_password = astronomyobserver_password
#          remote_folder = "/home/www/flask/taoke/static/Aurora/oval"
#
#          ssh = paramiko.SSHClient()
#          ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#          ssh.connect(remote_host, remote_port, remote_username, remote_password)
#
#          # 创建SFTP客户端
#          sftp = ssh.open_sftp()
#
#          for file in filelist:
#
#              webppath = os.path.join(basedir, "static/Aurora/oval", file +".webp")
#              remote_file_path = os.path.join(remote_folder, file + ".webp")
#              sftp.put(webppath, remote_file_path)
#
#          sftp.close()
#          ssh.close()
#
#          result[x_code] = 200
#          result[x_data] = list
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# @api3.route("/aurora/scale")
# def auroraScale():
#      url = "https://services.swpc.noaa.gov/products/noaa-scales.json"
#      result = {}
#
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          resultdict = json.loads(content)
#          datalist = []
#          dict_last = resultdict["-1"]
#          dict_last["index"] = -1
#          datalist.append(dict_last)
#          dict_least = resultdict["0"]
#          dict_least["index"] = 0
#          datalist.append(dict_last)
#          dict_0day = resultdict["1"]
#          dict_0day["index"] = 1
#          datalist.append(dict_0day)
#          dict_1day = resultdict["2"]
#          dict_1day["index"] = 2
#          datalist.append(dict_1day)
#          dict_2day = resultdict["3"]
#          dict_2day["index"] = 3
#          datalist.append(dict_2day)
#          result[x_code] = 200
#          result[x_data] = datalist
#          return json.dumps(result)
#      except Exception as e:
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#
#
#
#
# @api3.route('/aurora/day')
# def auror27day():
#
#      result = {}
#
#      url = "https://services.swpc.noaa.gov/text/27-day-outlook.txt"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = []
#          beigain = False
#
#          for line in content.splitlines():
#              text = line.decode("utf8").strip()
#
#              if beigain:
#                  tlist = text.split(" ")
#                  for t in tlist:
#                      t = t.strip()
#                      if len(t) > 0:
#                          list.append(t)
#              else:
#                 if text.find("#  Date ") > -1:
#                     beigain = True
#
#          datalist = []
#          n = int(len(list)/6)
#          for i in range(0,n):
#              # otime = list[4 * i]
#              dict = {}
#              year = int(list[6 * i + 0])
#              months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
#                        "Aug", "Sep", "Oct", "Nov", "Dec"]
#              monthstr = list[6 * i + 1]
#              month = 1
#              for j in range(1, 13):
#                  m = months[j - 1]
#                  if m == monthstr:
#                      month = j
#                      break
#              day = int(list[6*i + 2])
#
#              startdate = datetime(year, month, day, 0, 0, 0, tzinfo=tz)
#              dict["time"] = startdate.timestamp()
#              dict["flux"] = int(list[6*i + 3])
#              dict["ap"] = int(list[6*i + 4])
#              dict["kp"] = int(list[6*i + 5])
#              datalist.append(dict)
#
#          result[x_code] = 200
#          result[x_data] = datalist
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# @api3.route('/aurora/cme')
# def aurorcme():
#
#      result = {}
#
#      url = "https://www.sidc.be/cactus/out/cmecat.txt"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#
#          datalist = []
#          beigain = False
#
#          tz_offset = timezonfoffset()
#
#          for line in content.splitlines():
#              text = line.decode("utf8").strip()
#
#              if beigain:
#                  if text.find("# Flow") > -1:
#                      beigain = False
#                      continue
#                  dict = {}
#                  list = text.split("|")
#                  if len(list)< 9:
#                      continue
#                  dict["CME"] = list[0].strip()
#                  dict["t0"] = list[1].strip()
#                  fdate = datetime.strptime(list[1].strip(), "%Y/%m/%d %H:%M")
#                  dict["time"] = int(fdate.timestamp()) + tz_offset
#                  dict["dt0"] = int(list[2].strip())
#                  dict["pa"] = int(list[3].strip())
#                  dict["v"] = int(list[4].strip())
#                  dict["da"] = int(list[5].strip())
#                  dict["dv"] = int(list[6].strip())
#                  dict["minv"] = int(list[7].strip())
#                  dict["maxv"] =  int(list[8].strip())
#                  if len(list) > 9:
#                      dict["halo"] = list[9].strip()
#                  else:
#                      dict["halo"] = ""
#                  datalist.append(dict)
#
#              else:
#                 if text.find("# CME") > -1:
#                     beigain = True
#
#
#          result[x_code] = 200
#          result[x_data] = datalist
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# @api3.route("/aurora/cme/tip")
# def auroracmetip():
#      languange = request.args.get("language")
#
#      list = [
#          {"title":"CME",
#           "content":"CME number"},
#          {"title": "t0",
#           "content": "onset time, earliest indication of liftoff"},
#
#          {"title": "dt0",
#           "content": "duration of liftoff (hours)"},
#          {"title": "pa",
#           "content": "principal angle, counterclockwise from North (degrees)"},
#          {"title": "da",
#           "content": "angular width (degrees)"},
#          {"title": "v",
#           "content": "median velocity (km/s)"},
#          {"title": "dv",
#           "content": "variation (1 sigma) of velocity over the width of the CME"},
#
#          {"title": "minv",
#           "content": "lowest velocity detected within the CME"},
#          {"title": "maxv",
#           "content": "highest velocity detected within the CME"},
#
#          {"title": "halo?",
#           "content": "II if da>90, III if da>180, IV if da>270, indicating potential halo/partial halo CME"},
#
#
#
#      ]
#
#      zlist = [
#          {"title": "CME",
#           "content": "CME 编号"},
#          {"title": "t0",
#           "content": "开始时间，最早的抛射迹象"},
#
#          {"title": "dt0",
#           "content": "抛射持续时间（小时）"},
#          {"title": "pa",
#           "content": "主角度，从北向逆时针（度）"},
#          {"title": "da",
#           "content": "角宽度（度）"},
#          {"title": "v",
#           "content": "中值速度（km/s）"},
#          {"title": "dv",
#           "content": "CME 宽度上速度的变化（1 sigma）"},
#
#          {"title": "minv",
#           "content": "在 CME 内检测到的最低速度"},
#          {"title": "maxv",
#           "content": "在 CME 内检测到的最高速度"},
#
#          {"title": "halo?",
#           "content": "如果 da>90，则为 II，如果 da>180，则为 III，如果 da>270，则为 IV，表示潜在的halo/部分halo CME"},
#      ]
#
#      jplist = [
#          {"title": "CME",
#           "content": "CME 番号"},
#
#          {"title": "t0",
#           "content": "開始時間、放出の最も早い兆候"},
#
#          {"title": "dt0",
#           "content": "放出の継続時間 (時間)"},
#
#          {"title": "pa",
#           "content": "主角、北から反時計回り (度)"},
#
#          {"title": "da",
#           "content": "角幅 (度)"},
#
#          {"title": "v",
#           "content": "平均速度 (km/s)"},
#
#          {"title": "dv",
#           "content": "CME の幅全体にわたる速度の変化 (1 シグマ)"},
#
#          {"title": "minv",
#           "content": "CME 内で検出された最低速度"},
#
#          {"title": "maxv",
#           "content": "CME 内で検出された最高速度"},
#
#          {"title": "halo?",
#           "content": "da>90 の場合は II、da>180 の場合は III、da>270 の場合は IV で、潜在的なhalo/部分halo CME を示します"}
#      ]
#
#      result = {}
#
#
#      result[x_code] = 200
#      if languange == "zh":
#          result[x_data] = zlist
#      elif languange == "jp":
#          result[x_data] = jplist
#      else:
#          result[x_data] = list
#      return json.dumps(result)
#
#
#
#
# @api3.route('/aurora/solarwind')
# def aurorsolarwind():
#
#      result = {}
#      url = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = json.loads(content)
#          datalist = []
#
#          tz_offset = timezonfoffset()
#
#          n = len(list)
#
#          for i in range(1,n):
#              vlist = list[i]
#              datadict = {}
#              try:
#                  datadict["time_tag"] = vlist[0]
#                  datadict["speed"] = float(vlist[1])
#                  datadict["density"] = float(vlist[2])
#                  try:
#                      datadict["bz"] = float(vlist[6])
#                  except:
#                      datadict["bz"] = 0
#                  try:
#                      datadict["bt"] = float(vlist[7])
#                  except:
#                      datadict["bt"] = 0
#                  datadict["propagated_time_tag"] = vlist[11]
#                  ftime = vlist[0][:-4]
#                  fdate = datetime.strptime(ftime, "%Y-%m-%d %H:%M:%S")
#                  datadict["time"] = int(fdate.timestamp()) + tz_offset
#                  ptime = vlist[11][:-4]
#                  pdate = datetime.strptime(ptime, "%Y-%m-%d %H:%M:%S")
#                  datadict["propagated_time"] = int(pdate.timestamp()) + tz_offset
#                  datalist.append(datadict)
#              except Exception as e:
#                  pass
#
#
#
#          result[x_code] = 200
#          result[x_data] = datalist
#
#
#
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#
# @api3.route("/aurora/oval/<imagename>")
# def auroraOvalImage(imagename):
#      path = os.path.join(basedir, "static/Aurora/oval")
#      filename = imagename
#      try:
#          fpath = os.path.join(path, filename)
#          return send_file(fpath, as_attachment=True)
#
#      except Exception as e:
#          return ""
#
#
#
# @api3.route("/aurora/proton")
# def auroraproton():
#      result = {}
#      url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json"
#      try:
#          req = urllib.request.Request(url)
#          response = urllib.request.urlopen(req)
#          content = response.read()
#          list = json.loads(content)
#          datadict = {}
#
#          tz_offset = timezonfoffset()
#
#          mev10list = []
#          mev50list = []
#          mev100list = []
#          mev500list = []
#
#
#
#          for dict in list:
#              time_tag = dict["time_tag"]
#              dict["time"] = timetagtotimestamp(time_tag,tz_offset)
#              energy = dict["energy"]
#              if energy == ">=10 MeV":
#                  mev10list.append(dict)
#              elif energy == ">=50 MeV":
#                  mev50list.append(dict)
#              elif energy == ">=100 MeV":
#                  mev100list.append(dict)
#              elif energy == ">=500 MeV":
#                  mev500list.append(dict)
#
#
#
#
#
#          datadict["mev10"] = mev10list
#          datadict["mev50"] = mev50list
#          datadict["mev100"] = mev100list
#          datadict["mev500"] = mev500list
#          result[x_code] = 200
#          result[x_data] = datadict
#
#
#
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
#
#
# def aurora_forecast(type,aurora):
#      """
#      Get the latest Aurora Forecast from https://www.swpc.noaa.gov.
#
#      Returns
#      -------
#      img : numpy array
#          The pixels of the image in a numpy array.
#      img_proj : cartopy CRS
#          The rectangular coordinate system of the image.
#      img_extent : tuple of floats
#          The extent of the image ``(x0, y0, x1, y1)`` referenced in
#          the ``img_proj`` coordinate system.
#      origin : str
#          The origin of the image to be passed through to matplotlib's imshow.
#      dt : datetime
#          Time of forecast validity.
#
#      """
#
#      # GitHub gist to download the example data from
#      # url = ('https://services.swpc.noaa.gov/json/ovation_aurora_latest.json')
#      # To plot the current forecast instead, uncomment the following line
#
#      # parse timestamp
#      dt = datetime.strptime(aurora['Forecast Time'], '%Y-%m-%dT%H:%M:%SZ')
#
#      # # convert lists of [lon, lat, value] to 2D array of probability values
#      if 0 ==  type:
#          list = []
#          auroralist = aurora['coordinates']
#          for v in  auroralist:
#              lat = v[1]
#              if lat > 44:
#                  list.append(v)
#
#          aurora_data = np.array(list)
#          img = np.reshape(aurora_data[:, 2], (46, 360), order='F')
#
#          img_proj = ccrs.PlateCarree()
#          img_extent = (0, 359, 45, 90)
#          return img, img_proj, img_extent, 'lower',dt
#      else:
#          list = []
#          auroralist = aurora['coordinates']
#          for v in auroralist:
#              lat = v[1]
#              if lat < -44:
#                  list.append(v)
#
#          aurora_data = np.array(list)
#          img = np.reshape(aurora_data[:, 2], (46, 360), order='F')
#
#          img_proj = ccrs.PlateCarree()
#          img_extent = ( 0,359, -90, -45)
#          return img, img_proj, img_extent, 'lower', dt
#
#
# def aurora_cmap():
#      """Return a colormap with aurora like colors"""
#      stops = {'red': [(0.00, 0.3137, 0.3137),
#                       (0.10, 0.004, 0.004),
#                       (0.30, 0.227, 0.227),
#                       (0.50, 1.0, 1.0),
#                       (0.70, 1.0, 1.0),
#                       (0.80, 1.0, 1.0),
#                       (0.90, 0.98, 0.98),
#                       (1.00, 0.722, 0.722)],
#
#               'green': [(0.00, 0.6275, 0.6275),
#                         (0.10, 0.894, 0.894),
#                         (0.30, 1.0, 1.0),
#                         (0.50, 0.984, 0.984),
#                         (0.70, 0.651, 0.651),
#                         (0.80, 0.4706, 0.4706),
#                         (0.90, 0.004, 0.004),
#                         (1.00, 0.114, 0.114)],
#
#               'blue': [(0.00, 0.3137, 0.3137),
#                        (0.10, 0.000, 0.000),
#                        (0.30, 0.02, 0.02),
#                        (0.50, 0.0, 0.0),
#                        (0.70, 0.008, 0.008),
#                        (0.80, 0.0, 0.0),
#                        (0.90, 0.000, 0.000),
#                        (1.00, 0, 0)],
#
#               'alpha': [ (0.0, 0.0, 0.0),
#                          (0.01, 0.4, 0.4),
#                         (0.10, 1.0, 1.0),
#                         # (0.30, 0.9, 1.0),
#                         # (0.50, 1.0, 1.0),
#                         # (0.70, 1.0, 1.0),
#                         # (0.80, 1.0, 1.0),
#                         # (0.90, 1.0, 1.0),
#                         (1.00, 1.0, 1.0)]}
#
#      return LinearSegmentedColormap('aurora', stops)
#
#
# def auroraoval(type,png,hpi,logitude_center,auroradata):
#      plt.rcParams['figure.facecolor'] = 'black'
#
#      fig = plt.figure(figsize=[8, 8])
#
#      gs = gridspec.GridSpec(1, 1, left=0.01, right=0.99, bottom=0.01, top=0.99)
#
#
#      # We choose to plot in an Orthographic projection as it looks natural
#      # and the distortion is relatively small around the poles where
#      # the aurora is most likely.
#
#      # ax1 for Northern Hemisphere
#
#
#
#      if 0 == type:
#          ax = fig.add_subplot(gs[0], projection=ccrs.Orthographic(logitude_center, 70))
#
#      else:
#
#      # ax2 for Southern Hemisphere
#          lng_south =  -logitude_center
#
#
#          ax = fig.add_subplot(gs[0], projection=ccrs.Orthographic(logitude_center, -70))
#
#      url = 'https://www.astronomyobserver.net/api/v3.0/aurora/minutes/json'
#
#      # load data (JSON format)
#      response = urlopen(url)
#      aurora = json.loads(response.read().decode('utf-8'))
#      img, crs, extent, origin,dt = aurora_forecast(type,aurora)
#
#
#
#      # for ax in [ax1, ax2]:
#      ax.coastlines(zorder=3)
#
#      ax.stock_img()
#      ax.gridlines()
#
#
#
#
#      # resol = '50m'  # use data at this scale
#      # bodr = cfeature.NaturalEarthFeature(category='cultural',
#      #                                            name='admin_0_boundary_lines_land', scale=resol, facecolor='none',
#      #                                            alpha=0.7)
#      # land = cfeature.NaturalEarthFeature('physical', 'land', \
#      #                                            scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land'])
#      # ocean =  cfeature.NaturalEarthFeature('physical', 'ocean', \
#      #                                             scale=resol, edgecolor='none', facecolor=cfeature.COLORS['water'])
#      # lakes = cfeature.NaturalEarthFeature('physical', 'lakes', \
#      #                                             scale=resol, edgecolor='b', facecolor=cfeature.COLORS['water'])
#      # rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', \
#      #                                              scale=resol, edgecolor='b', facecolor='none')
#      #
#      # ax.add_feature(land, facecolor='beige')
#      # ax.add_feature(ocean, linewidth=0.2)
#      # ax.add_feature(lakes)
#      # ax.add_feature(rivers, linewidth=0.5)
#      # ax.add_feature(bodr, linestyle='--', edgecolor='k', alpha=1)
#      # print(dt_time)
#      ax.add_feature(Nightshade(dt))
#
#
#      add_lake(ax, facecolor="#5992F6")
#      # add_river(ax,ec = "blue",fc="None", linewidth=.5)
#      add_us_state(ax,ec = "black",fc="None", linewidth=.3)
#      add_MNG_county(ax,ec = "#1900FF",fc="None", linewidth=.3)
#      add_europe_county(ax,ec = "#1900FF",fc="None", linewidth=.3)
#
#      plt.text(0.03, 0.03, 'Aurora Map', fontsize=15,color="#12F000",transform=ax.transAxes)
#
#      plt.text(0.03, 0.96, "HPI: " + str(hpi) +" GW", fontsize=15,color="#12F000",transform=ax.transAxes)
#
#      otime_str = dt.strftime("%m-%d %H:%M")
#
#      plt.text(0.69, 0.96, "For " + otime_str + " (UTC)", fontsize=15,color="#12F000",transform=ax.transAxes)
#
#      colorimagepath = os.path.join(basedir,"static/Aurora","auroratip.jpg")
#      # colorimage = mpimage.imread(colorimagepath)
#      watermark_image = PILImage.open(colorimagepath)
#
#
#      ax.imshow(img, vmin=0, vmax=100, transform=crs,
#                    extent=extent, origin=origin, zorder=2,
#                    cmap=aurora_cmap())
#
#      if 0 == type:
#
#
#
#          locationList = [
#              {"lat": 62.454,
#          "name": "Yellowknife",
#          "lng": -114.373},
#              {"lat": 64.835,
#          "name": "Fairbanks",
#          "lng": -147.777},
#              {"name": "Whitehorse",
#          "lat": 60.721,
#          "lng": -135.057},
#              {"name": "Rovaniemi",
#          "lat": 66.5,
#          "lng": 25.733},
#              {"name": "Reykjavik",
#          "lat": 64.128,
#
#          "lng": -21.828},
#              {"name": "Tromsøya",
#          "lat": 69.649,
#          "lng": 18.955},
#          #     {"name": "Abisko",
#          # "lat": 68.3167,
#          # "lng": 18.6833},
#
#
#              {"name": "Mohe",
#          "lat": 53.56,
#          "lng": 122.34},
#
#              {"name":"Muurmanski",
#          "lat": 68.993,
#          "lng": 33.118},
#
#              {"name": "Wakkanai",
#          "lat": 45.416,
#          "lng": 141.673},
#
#              {"name": "Altay",
#          "lat": 47.827,
#          "lng": 88.121},
#
#              {"name": "Aroostook",
#          "lat": 46.65,
#          "lng": -68.59},
#
#              {"name": "Cook",
#               "lat": 47.917,
#               "lng": -90.55},
#
#              {"name": "Glacier",
#              "lat": 48.7,
#              "lng": -113.02},
#
#              {"name": "Vancouver",
#               "lat": 49.261,
#               "lng": -123.114},
#
#              {"name": "London",
#               "lat":  51.507,
#               "lng": 0.1275},
#              #
#              # {"name": "Copenhagen",
#              #  "lat": 55.676,
#              #  "lng": 12.202},
#              #
#              {"name": "Stockholm",
#               "lat": 59.329,
#               "lng": 18.069},
#
#          ]
#
#          for dict in locationList:
#              lat  =dict["lat"]
#              lng = dict["lng"]
#              name = dict["name"]
#              oreintion = "right"
#              if name == "Glacier":
#                  oreintion = "left"
#
#              if name == "Rovaniemi":
#                  oreintion = "left"
#              if name == "Muurmanski":
#                  oreintion = "left"
#              ax.plot(lng, lat, 'ob', transform=ccrs.PlateCarree())
#              transform = ccrs.PlateCarree()._as_mpl_transform(ax)
#              ax.annotate(name, xy=(lng, lat), xycoords=transform,
#                          ha=oreintion, va='top')
#      else:
#
#          pass
#
#      path = os.path.join(basedir, "static/Aurora/oval", png +".png")
#
#
#      plt.savefig(path)
#      plt.close()
#
#      webppath = os.path.join(basedir,"static/Aurora/oval",png+".webp")
#
#      oimage = PILImage.open(path)
#      watermark_width, watermark_height = watermark_image.size
#      original_width, original_height = oimage.size
#
#      x = original_width - watermark_width - 20
#      y = original_height - watermark_height - 24
#      oimage.paste(watermark_image, (x, y))
#      oimage.save(webppath,"webp")
#
#      if 0 == type:
#          latestpath = os.path.join(basedir, "static/Aurora/oval",  "aurora_N_latest.webp")
#          oimage.save(latestpath, "webp")
#      else:
#          latestpath = os.path.join(basedir, "static/Aurora/oval",  "aurora_S_latest.webp")
#          oimage.save(latestpath, "webp")
#
#
#
#      oimage.close()
#
#
#
#      os.remove(path)
#
#      return "done"
#
#
# def add_lake(ax, **kwargs):
#
#      path = os.path.join(basedir,"static/Aurora/ne_50m_lakes","ne_50m_lakes.shp")
#      proj = ccrs.PlateCarree()
#      reader = Reader(path)
#      provinces = reader.geometries()
#      ax.add_geometries(provinces, proj, **kwargs)
#      reader.close()
#
# def add_river(ax, **kwargs):
#
#      path = os.path.join(basedir,"static/Aurora/ne_50m_rivers_lake_centerlines","ne_50m_rivers_lake_centerlines.shp")
#      proj = ccrs.PlateCarree()
#      reader = Reader(path)
#      provinces = reader.geometries()
#      ax.add_geometries(provinces, proj, **kwargs)
#      reader.close()
#
# def add_us_state(ax, **kwargs):
#
#      path = os.path.join(basedir,"static/Aurora/us-state-boundaries","us-state-boundaries.shp")
#      proj = ccrs.PlateCarree()
#      reader = Reader(path)
#      provinces = reader.geometries()
#      ax.add_geometries(provinces, proj, **kwargs)
#      reader.close()
# def add_europe_county(ax, **kwargs):
#
#      path = os.path.join(basedir,"static/Aurora/world-administrative-boundaries","world-administrative-boundaries.shp")
#      proj = ccrs.PlateCarree()
#      reader = Reader(path)
#      provinces = reader.geometries()
#      ax.add_geometries(provinces, proj, **kwargs)
#      reader.close()
#
# def add_MNG_county(ax, **kwargs):
#
#      path = os.path.join(basedir,"static/Aurora/MNG","world-administrative-boundaries.shp")
#      proj = ccrs.PlateCarree()
#      reader = Reader(path)
#      provinces = reader.geometries()
#      ax.add_geometries(provinces, proj, **kwargs)
#      reader.close()
#
#
#
# def sanitize_lonlist(lons):
#      new_list = []
#      oldval = 0
#      # used to compare with the adjacent longitudes
#      # and values exceed, disconnect linestring
#      treshold = 10
#      for ix,ea in enumerate(lons):
#          diff = oldval - ea
#          if (ix>0):
#              if (diff>treshold):
#                  ea = ea+360
#          oldval = ea
#          new_list.append(ea)
#      return new_list
#
# def add_china_province(ax,**kwargs):
#
#      path = os.path.join(basedir,"static/Aurora","china_province.geojson")
#      tracks = gpd.read_file(path)
#      proj = ccrs.PlateCarree()
#      # grab x and y of the first geometry object
#      ax.add_geometries(tracks.geometry, proj, **kwargs)
#
#
#
#
#
#
# @api3.route("/aurora/nowcast/tip")
# def auroranowcasttp():
#      languange = request.args.get("language")
#
#      list = [
#          {"title":"Solar flares",
#           "content":"A solar flare is a relatively intense, localized emission of electromagnetic radiation in the Sun's atmosphere. Flares occur in active regions and are often, but not always, accompanied by coronal mass ejections, solar particle events, and other eruptive solar phenomena. The occurrence of solar flares varies with the 11-year solar cycle.\nSolar flares are thought to occur when stored magnetic energy in the Sun's atmosphere accelerates charged particles in the surrounding plasma. This results in the emission of electromagnetic radiation across the electromagnetic spectrum.\nThe extreme ultraviolet and X-ray radiation from solar flares is absorbed by the daylight side of Earth's upper atmosphere, in particular the ionosphere, and does not reach the surface. This absorption can temporarily increase the ionization of the ionosphere which may interfere with short-wave radio communication. The prediction of solar flares is an active area of research."},
#
#          {"title": "Coronal Mass Ejections",
#           "content": "Coronal Mass Ejections (CMEs) are large expulsions of plasma and magnetic field from the Sun’s corona. They can eject billions of tons of coronal material and carry an embedded magnetic field (frozen in flux) that is stronger than the background solar wind interplanetary magnetic field (IMF) strength. CMEs travel outward from the Sun at speeds ranging from slower than 250 kilometers per second (km/s) to as fast as near 3000 km/s. The fastest Earth-directed CMEs can reach our planet in as little as 15-18 hours. Slower CMEs can take several days to arrive. They expand in size as they propagate away from the Sun and larger CMEs can reach a size comprising nearly a quarter of the space between Earth and the Sun by the time it reaches our planet."},
#          {"title":"DSCOVR",
#           "content":"DSCOVR is a satellite operated by NOAA,used to observe the Solar wind. Generally, it take about one hour fo the solar wind to travel from DSCOVR to Earth."},
#
#          {"title": "Solar wind Bz",
#           "content": "Bz indicate the north/south direction of the solar wind's magnetic field. When Bz is negative value(Points south ward), Solar wind's magnetic filed is opposite to Eearth's magnetic field.This enhances the flow of energy and charged particlea, increases the probability of observing aurora"},
#
#          {"title":"Solar wind Bt",
#           "content":"The solar wind is a plasma, and therefore carries its own magnetic field. Its magnitude is given as “Bt”. Typically, the strength of the solar wind magnetic field is only a few nT (nano-Tesla), but when this gets to larger than 10 nT it could be a sign of pending geomagnetic activity."}
#      ]
#
#      zhlist = [
#          {"title": "太阳耀斑",
#           "content": "太阳耀斑是太阳大气中相对强烈的局部电磁辐射发射。耀斑发生在活跃区域，通常（但并非总是）伴随着日冕物质抛射、太阳粒子事件和其他爆发性太阳现象。太阳耀斑的发生随 11 年的太阳周期而变化。\n据信，当太阳大气中储存的磁能加速周围等离子体中的带电粒子时，就会发生太阳耀斑。这会导致电磁辐射在电磁波谱中发射。\n太阳耀斑产生的极紫外和 X 射线辐射被地球上层大气的白天一侧吸收，特别是电离层，无法到达地面。这种吸收会暂时增加电离层的电离，从而干扰短波无线电通信。太阳耀斑的预测是一个活跃的研究领域。"},
#
#          {"title": "日冕物质抛射",
#           "content": "日冕物质抛射日冕物质抛射 (CME) 是太阳日冕中大量等离子体和磁场的喷发。它们可以喷出数十亿吨日冕物质，并携带一个比背景太阳风行星际磁场 (IMF) 强度更强的嵌入式磁场（冻结的通量）。日冕物质抛射从太阳向外传播的速度范围从低于 250 公里/秒 (km/s) 到接近 3000 公里/秒。最快的地球导向日冕物质抛射可以在短短 15-18 小时内到达我们的星球。较慢的日冕物质抛射可能需要几天才能到达。它们在远离太阳传播时会扩大尺寸，较大的日冕物质抛射到达我们的星球时可以达到地球和太阳之间空间的近四分之一。"},
#          {"title": "DSCOVR",
#           "content": "DSCOVR 是由 NOAA 运营的卫星，用于观察太阳风。通常，太阳风从 DSCOVR 传播到地球大约需要一个小时。"},
#
#          {"title": "太阳风 Bz",
#           "content": "Bz 表示太阳风磁场的南北方向。当 Bz 为负值（指向南方）时，太阳风的磁场与地球磁场相反。这增强了能量和带电粒子的流动，增加了观察极光的概率"},
#
#          {"title": "太阳风 Bt",
#           "content": "太阳风是一种等离子体，因此带有自己的磁场。其幅度为“Bt”。通常，太阳风磁场的强度只有几 nT（纳特斯拉），但当它大于 10 nT 时，它可能预示着即将发生的地磁活动。"}
#      ]
#
#      jplist = [
#          {"title": "太陽フレア",
#           "content": "太陽フレアは、太陽の大気圏における比較的強力で局所的な電磁放射の放出です。フレアは活動領域で発生し、多くの場合、コロナ質量放出、太陽粒子イベント、その他の太陽の爆発現象を伴いますが、常に伴うわけではありません。太陽フレアの発生は、11 年の太陽周期によって異なります。\n太陽フレアは、太陽の大気圏に蓄積された磁気エネルギーが周囲のプラズマ内の荷電粒子を加速するときに発生すると考えられています。その結果、電磁スペクトル全体にわたって電磁放射が放出されます。\n太陽フレアからの極端紫外線と X 線放射は、地球の上層大気の昼側、特に電離層によって吸収され、地表には届きません。この吸収によって電離層の電離が一時的に増加し、短波無線通信に干渉する可能性があります。太陽フレアの予測は、活発な研究分野です。"},
#
#          {"title": "コロナ質量放出",
#           "content": "コロナ質量放出放出 (CME) は、太陽のコロナからプラズマと磁場が大量に放出される現象です。数十億トンのコロナ物質を放出し、背景の太陽風惑星間磁場 (IMF) の強度よりも強い磁場 (凍結した磁場) を運びます。CME は、250 キロメートル/秒 (km/s) より遅い速度から、3000 キロメートル/秒近くまでの範囲の速度で太陽から外側に飛び出します。地球に向けられた CME のうち最も速いものは、わずか 15 ～ 18 時間で地球に到達します。遅い CME は、到着までに数日かかることがあります。太陽から遠ざかるにつれてサイズが大きくなり、より大きな CME は、地球に到達するまでに地球と太陽の間の空間のほぼ 4 分の 1 を占めるサイズに達することがあります。"},
#          {"title": "DSCOVR",
#           "content": "DSCOVR は、NOAA が運用する衛星で、太陽風を観測するために使用されます。通常、太陽風が DSCOVR から地球まで移動するには約 1 時間かかります。"},
#
#          {"title": "太陽風 Bz",
#           "content": "Bz は太陽風の磁場の南北方向を示します。Bz が負の値 (南向き) の場合、太陽風の磁場は地球の磁場と反対になります。これにより、エネルギーと荷電粒子の流れが強化され、オーロラを観測する可能性が高まります。"},
#
#          {"title": "太陽風 Bt",
#           "content": "太陽風はプラズマであるため、独自の磁場を持ちます。その大きさは「Bt」で示されます。通常、太陽風の磁場の強さはわずか数 nT (ナノテスラ) ですが、これが 10 nT を超えると、地磁気活動が迫っている兆候である可能性があります。"}
#      ]
#
#
#
#      result = {}
#      result[x_code] = 200
#      if languange == "zh":
#          result[x_data] = zhlist
#      elif languange == "jp":
#          result[x_data] = jplist
#      else:
#          result[x_data] = list
#      return  json.dumps(result)
#
#
# @api3.route("/aurora/images")
# def auroraimages():
#
#      languange = request.args.get("language")
#
#
#      list = [
#          # {"name":"Tonight's North America",
#          #  "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png",
#          #  "tip":"This is a prediction of the intensity and location of the aurora borealis tonight and tomorrow night over North America. It also shows a 'viewline' that represents the southern-most locations from which you may see the aurora on the northern horizon.  This product is based on the OVATION model and uses the maximum forecast geomagnetic activity (Kp) between 6pm and 6am US Central Time.  The images are updated continuously, with the transition when \"tomorrow night\" becomes \"tonight\" occurring at 12:00Z (i.e., within an hour of the end of the 6pm-6am Central Time window that is used here to define \"night\").",
#          #  "type":0},
#          #
#          # {"name":"Tomorrow night's North America",
#          #  "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png",
#          #  "tip":"This is a prediction of the intensity and location of the aurora borealis tonight and tomorrow night over North America. It also shows a 'viewline' that represents the southern-most locations from which you may see the aurora on the northern horizon.  This product is based on the OVATION model and uses the maximum forecast geomagnetic activity (Kp) between 6pm and 6am US Central Time.  The images are updated continuously, with the transition when \"tomorrow night\" becomes \"tonight\" occurring at 12:00Z (i.e., within an hour of the end of the 6pm-6am Central Time window that is used here to define \"night\").",
#          #  "type":0},
#
#          {"name": "Aurora Latest North",
#           "link": "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_N_latest.webp",
#           "tip": "Since SWPC's Aurora Oval images are unavailable, the App uses SWPC's HPI data to simulate and draw images for reference only.",
#           "type": 0},
#
#          {"name": "Aurora Latest South",
#           "link": "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_S_latest.webp",
#           "tip": "Since SWPC's Aurora Oval images are unavailable, the App uses SWPC's HPI data to simulate and draw images for reference only.",
#           "type": 0},
#
#
#          {"name":"Space Weather Overview",
#           "link":"https://services.swpc.noaa.gov/images/swx-overview-small.gif",
#           "tip":"These plots provide a quick look at some of the most frequently examined space weather indices.",
#           "type":0},
#
#          {"name":"WSA-Enlil Solar Wind Prediction",
#           "link":"https://services.swpc.noaa.gov/images/animations/enlil/latest.jpg",
#           "tip":"In the movie, the Sun is represented as a yellow dot, the Earth by a green dot, and the STEREO spacecraft by the red and blue dots.  The top row represents the WSA-Enlil predicted solar wind density and the bottom row the predicted solar wind velocity.  On the left is a pinwheel plot of the ecliptic plane, showing all of the solar wind structures that are likely to encounter Earth or which have recently encountered Earth, in what is effectively an 'overhead' view.  While the STEREO spacecraft are shown, this ecliptic slice does not normally pass through these satellites, though it is typically fairly close.  In the middle are meridional slices that go through the Earth, showing the solar wind structures that will encounter Earth from a 'side' view.  On the right, the predicted density and velocity values for the location of Earth and the two STEREO spacecraft are plotted.",
#           "images":"https://services.swpc.noaa.gov/products/animations/enlil.json",
#           "type":1},
#
#          {"name": "Latest HUXt Ensemble Forecast",
#           "link": "https://huxt-bucket.s3.eu-west-2.amazonaws.com/wsa_huxt_forecast_latest.png",
#           "tip": "Top-left: Time series of solar wind speed.\nMiddle-left: Time series of CME arrival probability at Earth.\nBottom-left: Table of the Earth-directed CME properties and forecast arrival times/speeds.\nTop-right: Summary of the input data. The colour map shows the WSA solar wind speed at 21.5 rS in HEEQ coordinates. \nBottom-right: The probability density of CME arrival speeds, for the Earth-impacting CMEs only.",
#           "type": 0},
#
#          {"name":"D Region Absorption Prediction",
#           "link":"https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png",
#           "tip":"The D-Region Absorption Product addresses the operational impact of the solar X-ray flux and SEP events on HF radio communication. Long-range communications using high frequency (HF) radio waves (3 - 30 MHz) depend on reflection of the signals in the ionosphere. Radio waves are typically reflected near the peak of the F2 layer (~300 km altitude), but along the path to the F2 peak and back the radio wave signal suffers attenuation due to absorption by the intervening ionosphere.\nThe D-Region Absorption Prediction model is used as guidance to understand the HF radio degradation and blackouts this can cause.",
#           "images":"https://services.swpc.noaa.gov/products/animations/d-rap_global.json",
#           "type":1},
#
#          {"name":"Lasco c2",
#           "link":"https://services.swpc.noaa.gov/images/animations/lasco-c2/latest.jpg",
#           "tip":"LASCO images have been used by the SWPC forecast office to characterize the solar corona heating and transient events, including CME's, and to see the effects of the corona on the solar wind. More recently, the LASCO images are vital to the WSA-Enlil model that became operational in October of 2011. WSA-Enlil has become an important tool for forecasting the impact of Coronal Mass Ejections and the effects of the Solar Wind on the Earth.",
#           "images":"https://services.swpc.noaa.gov/products/animations/lasco-c2.json",
#           "type":1},
#
#          {"name":"Lasco c3",
#           "link":"https://services.swpc.noaa.gov/images/animations/lasco-c3/latest.jpg",
#           "tip":"LASCO images have been used by the SWPC forecast office to characterize the solar corona heating and transient events, including CME's, and to see the effects of the corona on the solar wind. More recently, the LASCO images are vital to the WSA-Enlil model that became operational in October of 2011. WSA-Enlil has become an important tool for forecasting the impact of Coronal Mass Ejections and the effects of the Solar Wind on the Earth.",
#           "images":"https://services.swpc.noaa.gov/products/animations/lasco-c3.json",
#           "type":1},
#
#          {"name":"GOES Solar Ultraviolet Imager Thematic Map",
#           "link":"https://services.swpc.noaa.gov/images/animations/suvi/primary/map/latest.png",
#          "tip":"",
#           "images":"https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json",
#           "type":1},
#
#          {"name": "GOES Solar Ultraviolet Imager 94 Angstroms",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/094/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json",
#           "type": 1},
#
#          {"name": "GOES Solar Ultraviolet Imager 131 Angstroms",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/131/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-131.json",
#           "type": 1},
#
#          {"name": "GOES Solar Ultraviolet Imager 171 Angstroms",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-171.json",
#           "type": 1},
#
#          {"name": "GOES Solar Ultraviolet Imager 195 Angstroms",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-195.json",
#           "type": 1},
#
#          {"name": "GOES Solar Ultraviolet Imager 284 Angstroms",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/284/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-284.json",
#           "type": 1},
#
#          {"name": "GOES Solar Ultraviolet Imager 304 Angstroms",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-304.json",
#           "type": 1},
#
#
#          {"name": "HMI Intensitygram - Flattened",
#           "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
#           "tip": "",
#           "type": 0},
#
#
#          {"name": "Solar Synoptic Map",
#           "link": "https://services.swpc.noaa.gov/images/synoptic-map.jpg",
#           "tip": "SWPC forecasters use their synoptic maps to view the various characteristics of solar surface at a locked-in time, on a daily basis. They create a snapshot of the features of the Sun each day by drawing the various phenomena they see, including active regions, coronal holes, neutral lines (boundary between magnetic polarities),  plages and filaments and prominences. This map is a valuable tool for assessing the conditions on the sun and making the appropriate forecast for those conditions.",
#           "type": 0},
#
#
#      ]
#
#
#      zhlist = [
#          # {"name":"今夜北美",
#          #  "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png",
#          #  "tip":"这是对今晚和明晚北美极光强度和位置的预测。它还显示了一条“视线”，代表您可以在北方地平线上看到极光的最南端位置。该产品基于 OVATION 模型，并使用美国中部时间下午 6 点至早上 6 点之间的最大预测地磁活动 (Kp)。图像不断更新，从“明晚”到“今晚”的过渡发生在 12:00Z（即，在中部时间下午 6 点至早上 6 点结束的一小时内，这里用于定义“夜晚”）。\n这两张地图显示了今晚和明晚的极光和视线。极光的亮度和位置通常显示为以地球磁极为中心的绿色椭圆形。当预测极光更强烈时，绿色椭圆形会变成红色。通常可以在日落后或日出前在地球上的某个地方观察到极光。白天看不到极光。极光不一定在正上方，但当极光明亮且条件合适时，从远至 1000 公里外都可以观察到。\n可以在极光 - 30 分钟预报页面上找到短期预报（约 30 分钟）以及过去 24 小时的活动。SWPC 的新极光仪表板（实验性）收集了 SWPC 网站上的产品和信息，提供一站式服务。",
#          #  "type":0},
#          #
#          # {"name":"明夜北美",
#          #  "link":"https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png",
#          #  "tip": "这是对今晚和明晚北美极光强度和位置的预测。它还显示了一条“视线”，代表您可以在北方地平线上看到极光的最南端位置。该产品基于 OVATION 模型，并使用美国中部时间下午 6 点至早上 6 点之间的最大预测地磁活动 (Kp)。图像不断更新，从“明晚”到“今晚”的过渡发生在 12:00Z（即，在中部时间下午 6 点至早上 6 点结束的一小时内，这里用于定义“夜晚”）。\n这两张地图显示了今晚和明晚的极光和视线。极光的亮度和位置通常显示为以地球磁极为中心的绿色椭圆形。当预测极光更强烈时，绿色椭圆形会变成红色。通常可以在日落后或日出前在地球上的某个地方观察到极光。白天看不到极光。极光不一定在正上方，但当极光明亮且条件合适时，从远至 1000 公里外都可以观察到。\n可以在极光 - 30 分钟预报页面上找到短期预报（约 30 分钟）以及过去 24 小时的活动。SWPC 的新极光仪表板（实验性）收集了 SWPC 网站上的产品和信息，提供一站式服务。",
#          #  "type":0},
#
#          # {"name": "Aurora-30 minute forecast(North)",
#          #  "link": "https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg",
#          #  "tip": "",
#          #  "images": "https://services.swpc.noaa.gov/products/animations/ovation_north_24h.json",
#          #  "type": 1},
#          #
#          # {"name": "Aurora-30 minute forecast(South)",
#          #  "link": "https://services.swpc.noaa.gov/images/animations/ovation/south/latest.jpg",
#          #  "tip": "",
#          #  "images": "https://services.swpc.noaa.gov/products/animations/ovation_south_24h.json",
#          #  "type": 1},
#
#          {"name": "极光北半球",
#           "link": "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_N_latest.webp",
#           "tip": "由于SWPC的Aurora Oval 图像不可用，App使用SWPC的HPI数据模拟绘制图像，仅供参考.",
#           "type": 0},
#
#          {"name": "极光南半球",
#           "link": "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_S_latest.webp",
#           "tip": "由于SWPC的Aurora Oval 图像不可用，App使用SWPC的HPI数据模拟绘制图像，仅供参考.",
#           "type": 0},
#
#          {"name":"空间天气预览",
#           "link":"https://services.swpc.noaa.gov/images/swx-overview-small.gif",
#           "tip":"这些图表可以让我们快速浏览一些最常检查的空间天气指数。",
#           "type":0},
#
#          {"name":"WSA-Enlil 太阳风预测",
#           "link":"https://services.swpc.noaa.gov/images/animations/enlil/latest.jpg",
#           "tip":"两部分：1) 一个半经验的近日模块，用于近似太阳风底部的流出；2) 一个复杂的三维磁流体力学数值模型，用于模拟由此产生的流向地球的流动演变。前一个模块由对太阳表面磁场的观测驱动，该观测是在太阳旋转过程中进行的，并合成为一幅天气图；该输入用于驱动参数化的日冕近日膨胀，随后输入到第二个行星际模块中，以计算准稳定（环境）太阳风流出。最后，当检测到指向地球的 CME 时，NASA 航天器的日冕仪图像用于描述 CME 的基本特性，包括时间、位置、方向和速度。该输入（“锥体”模型）被注入预先存在的环境条件中，随后的瞬态演变构成了预测 CME 到达地球的时间、强度和持续时间的基础。\n在影片中，太阳用黄点表示，地球用绿点表示，STEREO 航天器用红点和蓝点表示。上行太阳风密度，下行表示太阳风速度。左侧是黄道面的风车图，显示了所有可能与地球相遇或最近与地球相遇的太阳风结构，实际上是“俯视”视图。虽然显示了 STEREO 航天器，但这个黄道切片通常不会穿过这些卫星，尽管它们通常相当接近。中间是穿过地球的子午线切片，从“侧面”显示了将与地球相遇的太阳风结构。右侧绘制了地球和两个 STEREO 航天器位置的预测密度和速度值。",
#           "images":"https://services.swpc.noaa.gov/products/animations/enlil.json",
#           "type":1},
#          {"name": "最新的 HUXt 集合预报",
#           "link": "https://huxt-bucket.s3.eu-west-2.amazonaws.com/wsa_huxt_forecast_latest.png",
#           "tip": "左上：太阳风速度的时间序列。\n中左：CME 到达地球概率的时间序列。\n左下：地球指向的 CME 属性和预测到达时间/速度的表格。\n右上：输入数据摘要。彩色图显示了 HEEQ 坐标中 21.5 rS 处的 WSA 太阳风速度。\n右下：CME 到达速度的概率密度，仅适用于撞击地球的 CME。",
#           "type": 0},
#
#          {"name":"D 区吸收预测",
#           "link":"https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png",
#           "tip":"D 区吸收产品解决了太阳 X 射线通量和 SEP 事件对 HF 无线电通信的运行影响。使用高频 (HF) 无线电波 (3 - 30 MHz) 的远程通信取决于电离层中信号的反射。无线电波通常在 F2 层峰顶附近反射（高度约 300 公里），但沿着到 F2 峰顶和返回的路径，无线电波信号会因中间电离层的吸收而衰减。\nD 区吸收预测模型用作指导，以了解由此可能导致的 HF 无线电退化和停电。",
#           "images":"https://services.swpc.noaa.gov/products/animations/d-rap_global.json",
#           "type":1},
#
#          {"name":"Lasco c2",
#           "link":"https://services.swpc.noaa.gov/images/animations/lasco-c2/latest.jpg",
#           "tip":"LASCO 图像已被 SWPC 预报办公室用来描述日冕加热和瞬变事件（包括 CME）的特征，并观察日冕对太阳风的影响。最近，LASCO 图像对于 2011 年 10 月开始运行的 WSA-Enlil 模型至关重要。WSA-Enlil 已成为预测日冕物质抛射影响和太阳风对地球影响的重要工具。",
#           "images":"https://services.swpc.noaa.gov/products/animations/lasco-c2.json",
#           "type":1},
#
#          {"name":"Lasco c3",
#           "link":"https://services.swpc.noaa.gov/images/animations/lasco-c3/latest.jpg",
#           "tip":"LASCO 图像已被 SWPC 预报办公室用来描述日冕加热和瞬变事件（包括 CME）的特征，并观察日冕对太阳风的影响。最近，LASCO 图像对于 2011 年 10 月开始运行的 WSA-Enlil 模型至关重要。WSA-Enlil 已成为预测日冕物质抛射影响和太阳风对地球影响的重要工具。",
#           "images":"https://services.swpc.noaa.gov/products/animations/lasco-c3.json",
#           "type":1},
#
#          {"name":"GOES 太阳紫外成像仪主题图",
#           "link":"https://services.swpc.noaa.gov/images/animations/suvi/primary/map/latest.png",
#          "tip":"",
#           "images":"https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json",
#           "type":1},
#
#          {"name": "GOES 太阳紫外成像仪 94 埃米",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/094/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json",
#           "type": 1},
#
#          {"name": "GOES 太阳紫外成像仪 131 埃米",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/131/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-131.json",
#           "type": 1},
#
#          {"name": "GOES 太阳紫外成像仪 171 埃米",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-171.json",
#           "type": 1},
#
#          {"name": "GOES 太阳紫外成像仪 195 埃米",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-195.json",
#           "type": 1},
#
#          {"name": "GOES 太阳紫外成像仪 284 埃米",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/284/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-284.json",
#           "type": 1},
#
#          {"name": "GOES 太阳紫外成像仪 304 埃米",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-304.json",
#           "type": 1},
#
#          # {"name": "HMI Magnetogram",
#          #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg",
#          #  "tip": "",
#          #  "type": 0},
#          #
#          # {"name": "HMI Colorized Magnetogram",
#          #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",
#          #  "tip": "",
#          #  "type": 0},
#          #
#          # {"name": "HMI Intensitygram - colored",
#          #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg",
#          #  "tip": "",
#          #  "type": 0},
#          #
#          # {"name": "HMI Intensitygram - Flattened",
#          #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
#          #  "tip": "",
#          #  "type": 0},
#
#          {"name": "HMI Intensitygram - Flattened",
#           "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
#           "tip": "",
#           "type": 0},
#
#          # {"name": "HMI Dopplergram",
#          #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMID.jpg",
#          #  "tip": "",
#          #  "type": 0},
#
#          {"name": "太阳综合图",
#           "link": "https://services.swpc.noaa.gov/images/synoptic-map.jpg",
#           "tip": "SWPC 预报员使用他们的天气图来查看每天固定时间太阳表面的各种特征。他们通过绘制他们看到的各种现象来创建每天太阳特征的快照，包括活动区域、冕洞、中性线（磁极之间的边界）、斑块、细丝和日珥。这张图是评估太阳状况并针对这些状况做出适当预测的宝贵工具。",
#           "type": 0},
#
#
#      ]
#
#
#      jplist = [
#          # {"name": "今夜の北米",
#          #  "link": "https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tonights_static_viewline_forecast.png",
#          #  "tip": "これは、今夜と明日の夜に北米で発生するオーロラの強度と位置の予測です。また、北の地平線上にオーロラが見える最南端の位置を表す「ビューライン」も表示します。この製品は OVATION モデルに基づいており、米国中部標準時の午後 6 時から午前 6 時までの最大予測地磁気活動 (Kp) を使用します。画像は継続的に更新され、\"明日の夜\" が \"今夜\" に切り替わるのは 12:00Z (つまり、ここで \"夜\" を定義するために使用されている午後 6 時から午前 6 時までの中部標準時ウィンドウの終了から 1 時間以内) です。",
#          #  "type": 0},
#          #
#          # {"name": "明日の夜の北米",
#          #  "link": "https://services.swpc.noaa.gov/experimental/images/aurora_dashboard/tomorrow_nights_static_viewline_forecast.png",
#          #  "tip": "これは、今夜と明日の夜の北米上空のオーロラの強度と位置の予測です。また、北の地平線上にオーロラが見える最南端の位置を表す「ビューライン」も表示されます。この製品は OVATION モデルに基づいており、米国中部標準時の午後 6 時から午前 6 時までの最大予測地磁気活動 (Kp) を使用します。画像は継続的に更新され、\"明日の夜\"が\"今夜\"に変わるのは12:00Z（つまり、ここで\"夜\"を定義するために使用されている午後6時から午前6時の中央標準時のウィンドウの終了から1時間以内）です。",
#          #  "type": 0},
#
#          # {"name": "Aurora-30 minute forecast(North)",
#          #  "link": "https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg",
#          #  "tip": "",
#          #  "images": "https://services.swpc.noaa.gov/products/animations/ovation_north_24h.json",
#          #  "type": 1},
#          #
#          # {"name": "Aurora-30 minute forecast(South)",
#          #  "link": "https://services.swpc.noaa.gov/images/animations/ovation/south/latest.jpg",
#          #  "tip": "",
#          #  "images": "https://services.swpc.noaa.gov/products/animations/ovation_south_24h.json",
#          #  "type": 1},
#
#          {"name": "オーロラ北半球",
#           "link": "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_N_latest.webp",
#           "tip": "SWPC の Aurora Oval 画像が利用できないため、アプリは SWPC の HPI データを使用して、参照のみを目的として描画画像をシミュレートします。",
#           "type": 0},
#
#          {"name": "オーロラ南半球",
#           "link": "https://www.astronomyobserver.net/api/v3.0/aurora/oval/aurora_S_latest.webp",
#           "tip": "SWPC の Aurora Oval 画像が利用できないため、アプリは SWPC の HPI データを使用して、参照のみを目的として描画画像をシミュレートします.",
#           "type": 0},
#
#          {"name": "宇宙天気の概要",
#           "link": "https://services.swpc.noaa.gov/images/swx-overview-small.gif",
#           "tip": "これらのプロットは、最も頻繁に調査される宇宙天気指標のいくつかを簡単に見ることができます。",
#           "type": 0},
#
#          {"name": "WSA-Enlil太陽風予測",
#           "link": "https://services.swpc.noaa.gov/images/animations/enlil/latest.jpg",
#           "tip": "モデリング システムは、2 つの主要な部分で構成されています。1) 太陽風の基底部での流出を近似する半経験的太陽近傍モジュール、および 2) 地球への結果として生じる流れの進化をシミュレートする高度な 3D 磁気流体力学数値モデルです。前者のモジュールは、太陽の自転中に取得され、総観マップに合成された太陽表面磁場の観測によって駆動されます。この入力は、太陽コロナの太陽近傍でのパラメーター化された膨張を駆動するために使用され、その後、2 番目の惑星間モジュールに入力されて、準定常 (周囲) 太陽風の流出を計算します。最後に、地球に向けられた CME が検出されると、NASA 宇宙船からのコロナグラフ画像を使用して、タイミング、場所、方向、速度など、CME の基本的な特性が特徴付けられます。この入力 (「コーン」モデル) は、既存の周囲条件に注入され、その後の過渡的進化が、地球への CME 到着時間、その強度、およびその期間の予測の基礎となります。\nムービーでは、太陽は黄色の点、地球は緑の点、STEREO 宇宙船は赤と青の点で表されています。上の行は WSA-Enlil 予測の太陽風密度、下の行は予測の太陽風速度です。左側は黄道面の風車プロットで、地球に遭遇する可能性のある、または最近地球に遭遇したすべての太陽風構造を、実質的に「上空」からの眺めで示しています。STEREO 宇宙船が表示されていますが、この黄道スライスは通常これらの衛星を通過しませんが、通常はかなり近くにあります。中央は地球を通過する子午線スライスで、地球に遭遇する太陽風構造を「横」から見ています。右側には、地球と 2 つの STEREO 宇宙船の位置の予測密度と速度値がプロットされています。",
#           "images": "https://services.swpc.noaa.gov/products/animations/enlil.json",
#           "type": 1},
#
#          {"name": "最新の HUXt アンサンブル予報",
#           "link": "https://huxt-bucket.s3.eu-west-2.amazonaws.com/wsa_huxt_forecast_latest.png",
#           "tip": "左上: 太陽風速度の時系列。\n左中: 地球への CME 到達確率の時系列。\n左下: 地球に向けられた CME の特性と予測到達時間/速度の表。\n右上: 入力データの概要。カラー マップは、HEEQ 座標の 21.5 rS における WSA 太陽風速度を示しています。\n右下: 地球に影響を及ぼす CME のみの CME 到達速度の確率密度。",
#           "type": 0},
#
#          {"name": "D 領域吸収予測",
#           "link": "https://services.swpc.noaa.gov/images/animations/d-rap/global/d-rap/latest.png",
#           "tip": "D 領域吸収製品は、太陽 X 線フラックスと SEP イベントが HF 無線通信に及ぼす運用上の影響を扱っています。高周波 (HF) 無線波 (3～30 MHz) を使用した長距離通信は、電離層での信号の反射に依存します。電波は通常、F2 層のピーク付近 (高度約 300 km) で反射されますが、F2 ピークまでの経路に沿って、また戻る途中で、介在する電離層による吸収により電波信号が減衰します。\nD 領域吸収予測モデルは、これが原因となる可能性のある HF 無線の劣化とブラックアウトを理解するためのガイドとして使用されます。",
#           "images": "https://services.swpc.noaa.gov/products/animations/d-rap_global.json",
#           "type": 1},
#
#          {"name": "Lasco c2",
#           "link": "https://services.swpc.noaa.gov/images/animations/lasco-c2/latest.jpg",
#           "tip": "LASCO 画像は、SWPC 予報局によって、太陽コロナの加熱と CME を含む過渡現象の特徴付け、および太陽風に対するコロナの影響を確認するために使用されています。最近では、LASCO 画像は、2011 年 10 月に運用が開始された WSA-Enlil モデルにとって不可欠です。WSA-Enlil は、コロナ質量放出の影響と太陽風が地球に与える影響を予測するための重要なツールとなっています。",
#           "images": "https://services.swpc.noaa.gov/products/animations/lasco-c2.json",
#           "type": 1},
#
#          {"name": "Lasco c3",
#           "link": "https://services.swpc.noaa.gov/images/animations/lasco-c3/latest.jpg",
#           "tip": "LASCO 画像は、SWPC 予報局によって、太陽コロナの加熱と CME を含む過渡現象の特徴付け、およびコロナが太陽風に与える影響を調べるために使用されています。最近では、LASCO 画像は 2011 年 10 月に運用が開始された WSA-Enlil モデルにとって不可欠です。WSA-Enlil は、コロナ質量放出の影響と太陽風が地球に与える影響を予測するための重要なツールとなっています。",
#           "images": "https://services.swpc.noaa.gov/products/animations/lasco-c3.json",
#           "type": 1},
#
#          {"name": "GOES 太陽紫外線イメージャー テーママップ",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/map/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-map.json",
#           "type": 1},
#
#          {"name": "GOES 太陽紫外線イメージャー 94 オングストローム",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/094/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-094.json",
#           "type": 1},
#
#          {"name": "GOES 太陽紫外線イメージャー131 オングストローム",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/131/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-131.json",
#           "type": 1},
#
#          {"name": "GOES ソーラー紫外線イメージャー 171 オングストローム",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-171.json",
#           "type": 1},
#
#          {"name": "GOES ソーラー紫外線イメージャー 195オングストローム",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-195.json",
#           "type": 1},
#
#          {"name": "GOES ソーラー紫外線イメージャー 284 オングストローム",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/284/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-284.json",
#           "type": 1},
#
#          {"name": "GOES ソーラー紫外線イメージャー 304 オングストローム",
#           "link": "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png",
#           "tip": "",
#           "images": "https://services.swpc.noaa.gov/products/animations/suvi-primary-304.json",
#           "type": 1},
#
#          {"name": "HMI 強度グラム - フラット化",
#           "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
#           "tip": "",
#           "type": 0},
#
#          {"name": "太陽総観図",
#           "link": "https://services.swpc.noaa.gov/images/synoptic-map.jpg",
#           "tip": "SWPC の予報官は、総観図を使用して、毎日、特定の時間に太陽表面のさまざまな特性を表示します。彼らは、活動領域、コロナホール、中性線（磁気極性の境界）、プラージュ、フィラメント、プロミネンスなど、観測したさまざまな現象を描き、毎日太陽の特徴のスナップショットを作成します。この地図は、太陽の状態を評価し、それらの状態を適切に予測するための貴重なツールです。",
#           "type": 0},
#      ]
#
#
#
#      result = {}
#      result[x_code] = 200
#      if languange == "zh":
#          result[x_data] = zhlist
#      elif languange == "jp":
#          result[x_data] = jplist
#      else:
#          result[x_data] = list
#      return  json.dumps(result)
#
#
# @api3.route('/aurora/xray')
# def aurorsolarxray():
#
#      result = {}
#      url1 = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json"
#      url2 = "https://services.swpc.noaa.gov/json/goes/secondary/xray-flares-7-day.json"
#      urllist =[]
#      urllist.append(url1)
#      urllist.append(url2)
#      try:
#          datalist = []
#          for url  in urllist:
#              req = urllib.request.Request(url)
#              response = urllib.request.urlopen(req)
#              content = response.read()
#              list = json.loads(content)
#
#
#              tz_offset = timezonfoffset()
#
#              n = len(list)
#
#
#
#              for i in range(0,n):
#                  datadict = list[i]
#
#                  try:
#                      time_tag = datadict["time_tag"]
#                      datadict["time"] = timetagtotimestamp(time_tag,tz_offset)
#                      datadict["begin_time"] = timetagtotimestamp(datadict["begin_time"],tz_offset)
#                      maxtime = timetagtotimestamp(datadict["max_time"],tz_offset)
#                      datadict["max_time"] = maxtime
#                      datadict["end_time"] = timetagtotimestamp(datadict["end_time"],tz_offset)
#                      datadict["max_ratio_time"] = timetagtotimestamp(datadict["max_ratio_time"],tz_offset)
#
#                      max_class = datadict["max_class"]
#                      if max_class.find("M") > -1 or max_class.find("X") > -1:
#                          datalist.append(datadict)
#                  except Exception as e:
#                      pass
#
#
#
#          result[x_code] = 200
#
#          datalist1 = sorted(datalist,key=lambda x:x["time"])
#          timelist = []
#          datalist2 = []
#          for dict in datalist1:
#              time = dict["time"]
#              if time in timelist:
#                  pass
#              else:
#                  timelist.append(time)
#                  datalist2.append(dict)
#
#          result[x_data] = datalist2
#
#
#
#          return json.dumps(result)
#      except Exception as e:
#
#          result[x_code] = 201
#          result[x_meesage] = "%s"%e
#          return json.dumps(result)
#
# def timezonfoffset():
#
#      return time.localtime().tm_gmtoff
# def timetagtotimestamp(time,tz_offset):
#      date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
#      return  int(date.timestamp()) + tz_offset
#
# def pymeeusastrodict(timestamp):
#      dict = {}
#
#      dt = datetime.fromtimestamp(timestamp, tz=tz)
#      year = dt.year
#      month = dt.month
#      day = dt.day + dt.hour / 24.0 + dt.minute / 60.0 / 24.0 + dt.second / 3600.0 / 24.0
#      epoch = Epoch(year, month, day)
#      jd = epoch.jde()
#
#      es = pymeeus.Coordinates.true_obliquity(year,month,day)
#      el = pymeeus.Coordinates.nutation_longitude(year,month,day)
#
#      delta_t = round(Epoch.tt2ut(year, month), 3)
#      ast = round(epoch.apparent_sidereal_time(es,el),9)
#      sun_ra,sun_dec,sun_r = Sun.apparent_rightascension_declination_coarse(epoch)
#      moon_ra, moon_dec, moon_r, moon_ppi = Moon.apparent_equatorial_pos(epoch)
#      moon_ill = Moon.illuminated_fraction_disk(epoch)
#      dict["time"] = timestamp
#      dict["jd"] = jd
#      dict["delta_t"] = delta_t
#      dict["es"] = float(es)
#      dict["ast"] = ast * 24
#      dict["sun_ra"] = float(sun_ra) / 15.0
#      dict["sun_dec"]= float(sun_dec)
#      dict["sun_r"] = sun_r
#      dict["moon_ra"] = float(moon_ra) / 15.0
#      dict["moon_dec"] = float(moon_dec)
#      dict["moon_r"] = moon_r
#      dict["moon_ill"] = moon_ill
#      dict["true_solar_time"] = dict["ast"] * 3600 - dict["sun_ra"] * 3600 + 43200
#
#
#      return dict
#
#
#  # {"name": "AIA 0193  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg",
#  #  "tip": "This channel highlights the outer atmosphere of the Sun - called the corona - as well as hot flare plasma. Hot active regions, solar flares, and coronal mass ejections will appear bright here. The dark areas - called coronal holes - are places where very little radiation is emitted, yet are the main source of solar wind particles.",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0193.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 0304  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg",
#  #  "tip": "This channel is especially good at showing areas where cooler dense plumes of plasma (filaments and prominences) are located above the visible surface of the Sun. Many of these features either can't be seen or appear as dark lines in the other channels. The bright areas show places where the plasma has a high density.",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0304.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 0171  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg",
#  #  "tip": "This channel is especially good at showing coronal loops - the arcs extending off of the Sun where plasma moves along magnetic field lines. The brightest spots seen here are locations where the magnetic field near the surface is exceptionally strong. ",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0171.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 0211  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0211.jpg",
#  #  "tip": "This channel (as well as AIA 335) highlights the active region of the outer atmosphere of the Sun - the corona. Active regions, solar flares, and coronal mass ejections will appear bright here. The dark areas - called coronal holes - are places where very little radiation is emitted, yet are the main source of solar wind particles. ",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0211.mp4",
#  #  "type": 2},
#
#  # {"name": "AIA 0131  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0131.jpg",
#  #  "tip": "This channel (as well as AIA 094) is designed to study solar flares. It measures extremely hot temperatures around 10 million K (18 million F), as well as cool plasmas around 400,000 K (720,000 F). It can take images every 2 seconds (instead of 10) in a reduced field of view in order to look at flares in more detail. ",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0131.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 0335  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0335.jpg",
#  #  "tip": "This channel (as well as AIA 211) highlights the active region of the outer atmosphere of the Sun - the corona. Active regions, solar flares, and coronal mass ejections will appear bright here. The dark areas - or coronal holes - are places where very little radiation is emitted, yet are the main source of solar wind particles.",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0335.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 0094  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0094.jpg",
#  #  "tip": "This channel (as well as AIA 131) is designed to study solar flares. It measures extremely hot temperatures around 6 million Kelvin (10.8 million F). It can take images every 2 seconds (instead of 10) in a reduced field of view in order to look at flares in more detail.",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_0094.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 1600  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_1600.jpg",
#  #  "tip": "This channel (as well as AIA 1700) often shows a web-like pattern of bright areas that highlight places where bundles of magnetic fields lines are concentrated. However, small areas with a lot of field lines will appear black, usually near sunspots and active regions.",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_1600.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 1700  Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_1700.jpg",
#  #  "tip": "This channel (as well as AIA 1600) often shows a web-like pattern of bright areas that highlight places where bundles of magnetic fields lines are concentrated. However, small areas with a lot of field lines will appear black, usually near sunspots and active regions.",
#  #  "video": "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_512_1700.mp4",
#  #  "type": 2},
#  #
#  # {"name": "AIA 211 Å, 193 Å, 171 Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_211193171.jpg",
#  #  "tip": "This image combines three images with different, but very similar, temperatures. The colors are assigned differently than in the single images. Here AIA 211 is red, AIA 193 is green, and AIA 171 is blue. Each highlights a different part of the corona",
#  #  "type": 0},
#  #
#  # {"name": "AIA 304 Å, 211 Å, 171 Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_304_211_171_2048.jpg",
#  #  "tip": "This image combines three images with quite different temperatures. The colors are assigned differently than in the single images. Here AIA 304 is red (showing the chromosphere), AIA 211 is green (corona), and AIA 171 is dark blue (corona).",
#  #  "type": 0},
#  #
#  # {"name": "AIA 094 Å, 335 Å, 193 Å",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_094_335_193_2048.jpg",
#  #  "tip": "This image combines three images with different temperatures. Each image is assigned a color, and they are not the same used in the single images. Here AIA 094 is red, AIA 335 is green, and AIA 193 is blue. Each highlights a different part of the corona.",
#  #  "type": 0},
#  #
#  # {"name": "AIA 171 Å & HMIB",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_HMImag_171_2048.jpg",
#  #  "tip": "",
#  #  "type": 0},
#  #
#  # {"name": "HMI Magnetogram",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg",
#  #  "tip": "",
#  #  "type": 0},
#  #
#  # {"name": "HMI Colorized Magnetogram",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",
#  #  "tip": "",
#  #  "type": 0},
#  #
#  # {"name": "HMI Intensitygram - colored",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg",
#  #  "tip": "",
#  #  "type": 0},
#  #
#  # {"name": "HMI Intensitygram - Flattened",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
#  #  "tip": "",
#  #  "type": 0},
#  #
#  # {"name": "HMI Intensitygram",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMII.jpg",
#  #  "tip": "",
#  #  "type": 0},
#  #
#  # {"name": "HMI Dopplergram",
#  #  "link": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMID.jpg",
#  #  "tip": "",
#  #  "type": 0}
#
