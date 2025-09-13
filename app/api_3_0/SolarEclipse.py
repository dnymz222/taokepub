# #coding=utf8
# import os.path
#
# from . import api3
#
# from app import db
#
# import datetime as date_time_m
#
# import math
#
#
# from datetime import  datetime
# from config import basedir
# from PIL import Image as PILImage
#
#
#
# from matplotlib.colors import LinearSegmentedColormap
# import matplotlib.pyplot as plt
# import numpy as np
#
# import cartopy.crs as ccrs
#
# from cartopy.feature.nightshade import Nightshade
#
#
# from cartopy.io.shapereader import Reader
#
# import matplotlib.gridspec as gridspec
#
#
# from app.SolarEclipse import SolarEclipse
# from app.SolarEclipseCalculate import SolarEclipseCalculate
#
# import  geopandas as  gpd
# # import cv2
# from app.SolarEclipseTime import SolarEclipseTime
#
# @api3.route("/solareclipse/ten/check")
# def solareclipsetencheck():
#     for i in range(0,300):
#         startyear = 10 * i  + 1
#         endyear =  10 * (i + 1)
#         solareclipses = db.session.query(SolarEclipse).filter(SolarEclipse.year > startyear - 1).filter(
#             SolarEclipse.year < endyear + 1).all()
#         n = 0
#
#         for solareclipse in solareclipses:
#             if solareclipse.eclipse_type.find("T")==0 or solareclipse.eclipse_type.find("H") == 0 or solareclipse.eclipse_type.find("A")==0:
#                 n = n + 1
#         if n > 18:
#             print(startyear)
#         else:
#             print(n)
#     return "done"
#
# # @api3.route("/solar/video")
# # def solarvideo():
# #
# #
# #     date = "2025-03-29"
# #
# #     path = os.path.join(basedir,"static/Solareclipse/" + date +"/Chinese")
# #
# #     imagelist = []
# #
# #     for i in range(0,420):
# #         imagename  = "solar_"+ date +"_" + str(i) + ".png"
# #         imagepath = os.path.join(path,imagename)
# #         if os.path.exists(imagepath):
# #             imagelist.append(imagepath)
# #
# #     mp4path = os.path.join(basedir,"static/Solareclipse", date + "_zh.mp4")
# #
# #     frame = cv2.imread(imagelist[0])
# #     height,width,layers = frame.shape
# #
# #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# #
# #     video = cv2.VideoWriter(mp4path, fourcc, 10, (width, height))
# #     for image in imagelist:
# #         video.write(cv2.imread(image))
# #
# #     cv2.destroyAllWindows()
# #     video.release()
# #
# #
# #
# #     return "done"
#
#
# @api3.route("/solareclipse/time")
# def solareclipsecalct():
#
#
#     solareclipse = db.session.query(SolarEclipse).all()
#
#
#     for solareclipse in solareclipse:
#         start_t = solareclipse.start_t
#         end_t = solareclipse.end_t
#         start_t = math.floor(start_t * 10000 + 0.5) /  10000.0
#         end_t = math.floor(end_t * 10000 + 0.5) / 10000.0
#         # if start_t is None:
#         #     pass
#         # else:
#         #     continue
#         # index= 0
#         # for i in range(-89 * 3 -2, 89  * 3):
#         #     for j in range(-180*3, 180 * 3):
#         #         lat = i / 3.0
#         #         lng = j / 3.0
#         #         calcuale = SolarEclipseCalculate(latitude=lat,longitude=lng,altitude=0,hour=0,eclipse=solareclipse)
#         #         calcuale.calculate()
#         #         if calcuale.eclipseType > 0:
#         #             if 0 == index:
#         #                 start_t = calcuale.c1[1]
#         #                 end_t = calcuale.c4[1]
#         #             else:
#         #                 if start_t > calcuale.c1[1]:
#         #                     start_t = calcuale.c1[1]
#         #                 if end_t < calcuale.c4[1]:
#         #                     end_t = calcuale.c4[1]
#         #             index = index + 1
#
#         solareclipse.start_t = start_t
#         solareclipse.end_t = end_t
#         try:
#             db.session.commit()
#             print(solareclipse.year)
#             print(start_t)
#             print(end_t)
#         except:
#             db.session.rollback()
#
#
#
#
#
#     return "done"
#
#
# @api3.route("/solareclipse/time/oval")
# def solareclipsetimeoval():
#
#
#     solareclipse = db.session.query(SolarEclipse).filter(SolarEclipse.year> 2024).filter(SolarEclipse.year < 2031).all()
#
#
#     for solareclipse in solareclipse:
#         start_t = solareclipse.start_t + 0.2 / 60.0
#         end_t = solareclipse.end_t
#
#         imagelist = []
#         dirname = "%d-%02d-%02d" % (solareclipse.year, solareclipse.month, solareclipse.day)
#
#         dirpath = os.path.join(basedir, "static/Solareclipse/Video/PNG", dirname)
#         if os.path.exists(dirpath):
#             pass
#         else:
#             os.mkdir(dirpath)
#         n =  int(math.ceil ((end_t - start_t) * 60))
#         for i in range(0, n):
#             t = start_t + i / 60.0
#             imagename = str(i)
#             imagepath = os.path.join(dirpath, imagename + ".png")
#             if os.path.exists(imagepath):
#                 imagelist.append(imagepath)
#                 continue
#             eclipsetime = SolarEclipseTime(t=t,eclipse=solareclipse)
#             solareclipsetimeOval(solarEclipsetime=eclipsetime,index=i)
#             imagelist.append(imagepath)
#         year  = int(solareclipse.year)
#         century = int(math.ceil(year/100.0))
#         dirpath1 = os.path.join(basedir, "static/Solareclipse/Image/PNG", str(century))
#         imagename1 = "%d-%02d-%02d.png" % (solareclipse.year, solareclipse.month, solareclipse.day)
#         imagepath1 = os.path.join(dirpath1,imagename1)
#         if os.path.exists(imagepath1):
#             imagelist.append(imagepath1)
#         else:
#             print(imagepath1)
#
#         # mp4path = os.path.join(basedir, "static/Solareclipse/Video", dirname + ".mp4")
#         #
#         # frame = cv2.imread(imagelist[0])
#         # height, width, layers = frame.shape
#         #
#         # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         #
#         # video = cv2.VideoWriter(mp4path, fourcc, 12, (width, height))
#         # for image in imagelist:
#         #     video.write(cv2.imread(image))
#         #
#         # cv2.destroyAllWindows()
#         # video.release()
#
#     return "done"
#
# @api3.route("/solareclipse/centry/<index>")
# def solareclipsecentery(index):
#     index_int = int(index)
#     start = -1999
#     start_year = -1999 + index_int * 100
#     endyear = start_year  + 99
#
#     solareclipse = db.session.query(SolarEclipse).filter(SolarEclipse.year> start_year - 1).filter(SolarEclipse.year < endyear + 1).all()
#
#     colorimagepath = os.path.join(basedir, "static/Solareclipse/Image/WEBP", str(index_int - 19))
#     if os.path.exists(colorimagepath):
#         pass
#     else:
#         os.mkdir(colorimagepath)
#     pngimagepath = os.path.join(basedir, "static/Solareclipse/Image/PNG", str(index_int - 19))
#     if os.path.exists(pngimagepath):
#         pass
#     else:
#         os.mkdir(pngimagepath)
#
#     for solareclipse in solareclipse:
#
#
#
#         solareclipseOval(solareclipse,str(index_int - 19))
#
#
#     return "done"
#
#
#
#
# @api3.route("/solareclipse/map")
# def solareclipseOval(solarEclipseItem: SolarEclipse,century: str):
#     monthlist = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#
#     imagename = "%d-%02d-%02d" % (solarEclipseItem.year, solarEclipseItem.month, solarEclipseItem.day)
#
#     dirpath = os.path.join(basedir, "static/Solareclipse/Image/PNG", century)
#
#     path = os.path.join(dirpath, imagename + ".png")
#
#     wdirpath = os.path.join(basedir, "static/Solareclipse/Image/WEBP", century)
#
#     webppath = os.path.join(wdirpath, imagename +".webp")
#
#     if os.path.exists(webppath):
#         return
#
#
#
#     plt.rcParams['figure.facecolor'] = 'black'
#
#     fig = plt.figure(figsize=[16, 16])
#
#     gs = gridspec.GridSpec(1, 1, left=0.01, right=0.99, bottom=0.01, top=0.99)
#
#
#     # We choose to plot in an Orthographic projection as it looks natural
#     # and the distortion is relatively small around the poles where
#     # the aurora is most likely.
#
#     # ax1 for Northern Hemisphere
#
#
#
#
#     ax = fig.add_subplot(gs[0], projection=ccrs.Orthographic(solarEclipseItem.lng_dd_ge, solarEclipseItem.lat_dd_ge))
#
#
#
#     # url = 'https://www.astronomyobserver.net/api/v3.0/aurora/minutes/json'
#     #
#     # # load data (JSON format)
#     # response = urlopen(url)
#     # aurora = json.loads(response.read().decode('utf-8'))
#     img, crs, extent, origin,dt = aurora_forecast(solarEclipseItem)
#
#
#
#     # for ax in [ax1, ax2]:
#     ax.coastlines(zorder=3)
#
#     ax.stock_img()
#     ax.gridlines()
#
#
#
#
#     # resol = '50m'  # use data at this scale
#     # bodr = cfeature.NaturalEarthFeature(category='cultural',
#     #                                            name='admin_0_boundary_lines_land', scale=resol, facecolor='none',
#     #                                            alpha=0.7)
#     # land = cfeature.NaturalEarthFeature('physical', 'land', \
#     #                                            scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land'])
#     # ocean =  cfeature.NaturalEarthFeature('physical', 'ocean', \
#     #                                             scale=resol, edgecolor='none', facecolor=cfeature.COLORS['water'])
#     # lakes = cfeature.NaturalEarthFeature('physical', 'lakes', \
#     #                                             scale=resol, edgecolor='b', facecolor=cfeature.COLORS['water'])
#     # rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', \
#     #                                              scale=resol, edgecolor='b', facecolor='none')
#     #
#     # ax.add_feature(land, facecolor='beige')
#     # ax.add_feature(ocean, linewidth=0.2)
#     # ax.add_feature(lakes)
#     # ax.add_feature(rivers, linewidth=0.5)
#     # ax.add_feature(bodr, linestyle='--', edgecolor='k', alpha=1)
#     # print(dt_time)
#
#     dt_utc = dt -  date_time_m.timedelta(seconds=solarEclipseItem.dt)
#
#     ax.add_feature(Nightshade(dt_utc))
#
#
#     add_lake(ax, facecolor="#5992F6")
#     add_river(ax,ec = "blue",fc="None", linewidth=.15)
#     add_us_state(ax,ec = "black",fc="None", linewidth=.3)
#     # add_MNG_county(ax,ec = "#1900FF",fc="None", linewidth=.3)
#     add_europe_county(ax,ec = "#1900FF",fc="None", linewidth=.3)
#
#     add_africa_county(ax,   ec = "#1900FF",fc="None", linewidth=.3)
#     add_america_county(ax, ec= "#1900FF", fc="None", linewidth=.3)
#     add_asia_county(ax, ec="#1900FF", fc="None", linewidth=.3)
#     add_china_province(ax,ec = "black",fc="None", linewidth=.3)
#
#
#     plt.text(0.02, 0.03, "'Eclipse Map' App", fontsize=30,color="#F38C30",transform=ax.transAxes)
#
#     plt.text(0.02, 0.96, solarEclipseItem.eclipsectypename() + " (Mag:%.3f)"%solarEclipseItem.magnitude, fontsize=30,color="#F38C30",transform=ax.transAxes)
#
#     # otime_str = dt_utc.strftime("%Y-%m-%d %H:%M")
#
#     otime_str = "%d %s %02d %02d:%02d"%(dt_utc.year,monthlist[dt_utc.month - 1],dt_utc.day,dt_utc.hour,dt_utc.minute)
#
#     plt.text(0.7, 0.96,   otime_str + " UTC", fontsize=30,color="#F38C30",transform=ax.transAxes)
#
#     colorimagepath = os.path.join(basedir,"static/Solareclipse","solareclipsecolor.jpg")
#     # colorimage = mpimage.imread(colorimagepath)
#     watermark_image = PILImage.open(colorimagepath)
#
#
#     ax.imshow(img, vmin=0, vmax=100, transform=crs,
#                   extent=extent, origin=origin, zorder=2,
#                   cmap=aurora_cmap())
#
#
#     locationlist = [
#         {"name": "London", "latitude": 51.5, "longitude": -0.16666666666666666, "altitude": 45.4, "minute_offset": 0},
#         {"name": "Paris", "latitude": 48.86666666666667, "longitude": 2.3333333333333335, "altitude": 50.0, "minute_offset": 60},
#         {"name": "Berlin", "latitude": 52.5, "longitude": 13.366666666666667, "altitude": 0.0, "minute_offset": 60},
#         {"name": "Athens", "latitude": 37.96666666666667, "longitude": 23.716666666666665, "altitude": 107.0, "minute_offset": 120},
#         {"name": "Rome", "latitude": 41.9, "longitude": 12.483333333333333, "altitude": 114.9, "minute_offset": 60},
#         {"name": "Moscow", "latitude": 55.75, "longitude": 37.583333333333336, "altitude": 153.9, "minute_offset": 180},
#         {"name": "Jerusalem", "latitude": 31.766666666666666, "longitude": 35.233333333333334, "altitude": 808.9, "minute_offset": 120},
#         {"name": "Istanbul", "latitude": 41.016666666666666, "longitude": 28.966666666666665, "altitude": 18.0, "minute_offset": 180},
#         {"name": "Beijing", "latitude": 39.916666666666664, "longitude": 116.41666666666667, "altitude": 0.0, "minute_offset": 480},
#         {"name": "Xian", "latitude": 34.25, "longitude": 108.86666666666666, "altitude": 0.0, "minute_offset": 480},
#         {"name": "Tokyo", "latitude": 35.7, "longitude": 139.76666666666668, "altitude": 5.8, "minute_offset": 540},
#         {"name": "Sydney", "latitude": -33.86666666666667, "longitude": 151.21666666666667, "altitude": 18.9, "minute_offset": 600},
#         {"name": "Singapore", "latitude": 1.2833333333333332, "longitude": 103.85, "altitude": 10.1, "minute_offset": 480},
#         {"name": "Los Angeles", "latitude": 34.05, "longitude": -118.23333333333333, "altitude": 29.6, "minute_offset": -480},
#         {"name": "Washington", "latitude": 38.88333333333333, "longitude": -77.03333333333333, "altitude": 4.3, "minute_offset": -300},
#         {"name": "New York", "latitude": 40.71666666666667, "longitude": -74.01666666666667, "altitude": 40.2, "minute_offset": -300},
#         {"name": "Buenos Aires", "latitude": -34.6, "longitude": -58.45, "altitude": 27.1, "minute_offset": -180},
#         {"name": "Rio de Janeiro", "latitude": -22.9, "longitude": -43.233333333333334, "altitude": 61.3, "minute_offset": -180}]
#
#     greatdict = {}
#     greatdict["name"] = "Greatest"
#     greatdict["latitude"] = solarEclipseItem.lat_dd_ge
#     greatdict["longitude"] = solarEclipseItem.lng_dd_ge
#     greatdict["altitude"] = 0
#     greatdict["minute_offset"] = 0
#
#     locationlist.append(greatdict)
#
#     for dict in locationlist:
#          lat  =dict["latitude"]
#          lng = dict["longitude"]
#          name = dict["name"]
#          oreintion = "right"
#          ax.plot(lng, lat, 'ob', transform=ccrs.PlateCarree())
#          transform = ccrs.PlateCarree()._as_mpl_transform(ax)
#          ax.annotate(name, xy=(lng, lat), xycoords=transform,ha=oreintion, va='top')
#
#
#
#
#
#     plt.savefig(path)
#     plt.close()
#
#
#
#     oimage = PILImage.open(path)
#     watermark_width, watermark_height = watermark_image.size
#     original_width, original_height = oimage.size
#
#     x = original_width - watermark_width - 24
#     y = original_height - watermark_height - 32
#     oimage.paste(watermark_image, (x, y))
#     oimage.save(webppath,"webp",lossless = True)
#
#     oimage.save(path, "png")
#
#
#
#     oimage.close()
#
#
#
#     # os.remove(path)
#
#     return "done"
#
#
#
#
# def solareclipsetimeOval(solarEclipsetime: SolarEclipseTime,index: int):
#     solarEclipseItem = solarEclipsetime.eclipse
#     dirname = "%d-%02d-%02d" % (solarEclipseItem.year, solarEclipseItem.month, solarEclipseItem.day)
#
#     dirpath = os.path.join(basedir, "static/Solareclipse/Video/PNG", dirname)
#     if os.path.exists(dirpath):
#         pass
#     else:
#         os.mkdir(dirpath)
#
#     imagename =  str(index)
#     path = os.path.join(dirpath, imagename + ".png")
#
#
#     plt.rcParams['figure.facecolor'] = 'black'
#
#     fig = plt.figure(figsize=[16, 16])
#
#     gs = gridspec.GridSpec(1, 1, left=0.01, right=0.99, bottom=0.01, top=0.99)
#
#
#     ax = fig.add_subplot(gs[0], projection=ccrs.Orthographic(solarEclipsetime.centetlongitude, solarEclipsetime.centetlatitude))
#
#
#
#     # url = 'https://www.astronomyobserver.net/api/v3.0/aurora/minutes/json'
#     #
#     # # load data (JSON format)
#     # response = urlopen(url)
#     # aurora = json.loads(response.read().decode('utf-8'))
#     img, crs, extent, origin,dt = solareclipsecalcualtetime(solarEclipsetime)
#
#
#
#     # for ax in [ax1, ax2]:
#     ax.coastlines(zorder=3)
#
#     ax.stock_img()
#     ax.gridlines()
#
#
#
#
#
#     dt_utc = dt
#
#     ax.add_feature(Nightshade(dt_utc))
#
#
#     add_lake(ax, facecolor="#5992F6")
#     add_river(ax,ec = "blue",fc="None", linewidth=.15)
#     add_us_state(ax,ec = "black",fc="None", linewidth=.3)
#     # add_MNG_county(ax,ec = "#1900FF",fc="None", linewidth=.3)
#     add_europe_county(ax,ec = "#1900FF",fc="None", linewidth=.3)
#
#     add_africa_county(ax,   ec = "#1900FF",fc="None", linewidth=.3)
#     add_america_county(ax, ec= "#1900FF", fc="None", linewidth=.3)
#     add_asia_county(ax, ec="#1900FF", fc="None", linewidth=.3)
#     add_china_province(ax,ec = "black",fc="None", linewidth=.3)
#
#
#     plt.text(0.02, 0.03, "'Eclipse Map' App", fontsize=30,color="#F38C30",transform=ax.transAxes)
#
#     plt.text(0.02, 0.96, "Maximum Mag:%.3f"%solarEclipsetime.maxmagnitude, fontsize=30,color="#F38C30",transform=ax.transAxes)
#
#     otime_str = dt_utc.strftime("%Y-%m-%d %H:%M")
#
#     plt.text(0.7, 0.96,   otime_str + " UTC", fontsize=30,color="#F38C30",transform=ax.transAxes)
#
#     colorimagepath = os.path.join(basedir,"static/Solareclipse","solareclipsecolor.jpg")
#     # colorimage = mpimage.imread(colorimagepath)
#     watermark_image = PILImage.open(colorimagepath)
#
#
#     ax.imshow(img, vmin=0, vmax=100, transform=crs,
#                   extent=extent, origin=origin, zorder=2,
#                   cmap=aurora_cmap())
#
#
#     locationlist = [
#         {"name": "London", "latitude": 51.5, "longitude": -0.16666666666666666, "altitude": 45.4, "minute_offset": 0},
#         {"name": "Paris", "latitude": 48.86666666666667, "longitude": 2.3333333333333335, "altitude": 50.0, "minute_offset": 60},
#         {"name": "Berlin", "latitude": 52.5, "longitude": 13.366666666666667, "altitude": 0.0, "minute_offset": 60},
#         {"name": "Athens", "latitude": 37.96666666666667, "longitude": 23.716666666666665, "altitude": 107.0, "minute_offset": 120},
#         {"name": "Rome", "latitude": 41.9, "longitude": 12.483333333333333, "altitude": 114.9, "minute_offset": 60},
#         {"name": "Moscow", "latitude": 55.75, "longitude": 37.583333333333336, "altitude": 153.9, "minute_offset": 180},
#         {"name": "Jerusalem", "latitude": 31.766666666666666, "longitude": 35.233333333333334, "altitude": 808.9, "minute_offset": 120},
#         {"name": "Istanbul", "latitude": 41.016666666666666, "longitude": 28.966666666666665, "altitude": 18.0, "minute_offset": 180},
#         {"name": "Beijing", "latitude": 39.916666666666664, "longitude": 116.41666666666667, "altitude": 0.0, "minute_offset": 480},
#         {"name": "Xian", "latitude": 34.25, "longitude": 108.86666666666666, "altitude": 0.0, "minute_offset": 480},
#         {"name": "Tokyo", "latitude": 35.7, "longitude": 139.76666666666668, "altitude": 5.8, "minute_offset": 540},
#         {"name": "Sydney", "latitude": -33.86666666666667, "longitude": 151.21666666666667, "altitude": 18.9, "minute_offset": 600},
#         {"name": "Singapore", "latitude": 1.2833333333333332, "longitude": 103.85, "altitude": 10.1, "minute_offset": 480},
#         {"name": "Los Angeles", "latitude": 34.05, "longitude": -118.23333333333333, "altitude": 29.6, "minute_offset": -480},
#         {"name": "Washington", "latitude": 38.88333333333333, "longitude": -77.03333333333333, "altitude": 4.3, "minute_offset": -300},
#         {"name": "New York", "latitude": 40.71666666666667, "longitude": -74.01666666666667, "altitude": 40.2, "minute_offset": -300},
#         {"name": "Buenos Aires", "latitude": -34.6, "longitude": -58.45, "altitude": 27.1, "minute_offset": -180},
#         {"name": "Rio de Janeiro", "latitude": -22.9, "longitude": -43.233333333333334, "altitude": 61.3, "minute_offset": -180}]
#
#
#     for dict in locationlist:
#          lat  =dict["latitude"]
#          lng = dict["longitude"]
#          name = dict["name"]
#          oreintion = "right"
#          ax.plot(lng, lat, 'ob', transform=ccrs.PlateCarree())
#          transform = ccrs.PlateCarree()._as_mpl_transform(ax)
#          ax.annotate(name, xy=(lng, lat), xycoords=transform,ha=oreintion, va='top')
#
#
#
#
#
#     plt.savefig(path)
#     plt.close()
#
#
#
#     oimage = PILImage.open(path)
#     watermark_width, watermark_height = watermark_image.size
#     original_width, original_height = oimage.size
#
#     x = original_width - watermark_width - 24
#     y = original_height - watermark_height - 32
#     oimage.paste(watermark_image, (x, y))
#
#     oimage.save(path, "png")
#
#
#
#     oimage.close()
#
#
#
#     # os.remove(path)
#
#     return "done"
#
#
# def aurora_forecast(solarEclipse: SolarEclipse):
#
#
#     vlist = []
#
#     for i in range(0,360 * 10 + 1):
#         for j in range(-90 * 10 , 90 * 10  + 1):
#             latitude = j / 10.0
#             longitude = i / 10.0
#             if longitude > 180:
#                 longitude = longitude - 360
#
#             solarCalculate = SolarEclipseCalculate(latitude,longitude,0,0,solarEclipse)
#             solarCalculate.calculate()
#             vlist.append(solarCalculate.eclipse_v)
#
#     time_str = solarEclipse.td_ge
#
#     timelist = time_str.split(":")
#
#
#     dt = datetime(year=solarEclipse.year,month=solarEclipse.month,day=solarEclipse.day,hour= int(timelist[0]),minute=int(timelist[1]),second=int(timelist[2]))
#
#     # # convert lists of [lon, lat, value] to 2D array of probability values
#
#
#     aurora_data = np.array(vlist)
#     img = np.reshape(aurora_data, (180 * 10 + 1  , 360  * 10 + 1), order='F')
#
#     img_proj = ccrs.PlateCarree()
#     img_extent = (0, 360 , -90  , 90 )
#     return img, img_proj, img_extent, 'lower',dt
#
# def solareclipsecalcualtetime(eclipsetime: SolarEclipseTime):
#
#
#     vlist = eclipsetime.vlist
#
#
#
#
#     dt = datetime(year=eclipsetime.year,month=eclipsetime.month,day=eclipsetime.day,hour= eclipsetime.hour,minute=eclipsetime.minute,second=eclipsetime.second)
#
#     # # convert lists of [lon, lat, value] to 2D array of probability values
#
#
#     aurora_data = np.array(vlist)
#     img = np.reshape(aurora_data, (180 * 10 + 1  , 360  * 10 + 1), order='F')
#
#     img_proj = ccrs.PlateCarree()
#     img_extent = (0, 360 , -90  , 90 )
#     return img, img_proj, img_extent, 'lower',dt
#
#
#
# def aurora_cmap():
#     """Return a colormap with aurora like colors"""
#     stops = {'red': [(0.00, 250/255.0, 250/255.0),
#                      (0.2, 250/255.0, 250/255.0),
#
#                      (0.201, 243 / 255.0, 243 / 255.0),
#                      (0.4, 243/255.0, 243/255.0),
#
#                      (0.401, 216 / 255.0, 216 / 255.0),
#                      (0.60,  216/255.0, 216/255.0),
#
#                      (0.601, 178 / 255.0, 178 / 255.0),
#                      (0.80, 178/255.0, 178/255.0),
#
#                      (0.801, 108 / 255.0, 108 / 255.0),
#                      (0.999, 108/255.0, 108/255.0),
#
#                      (1.00, 0, 0)],
#
#              'green':  [(0.00, 228/255.0, 2228/255.0),
#                      (0.2, 228/255.0, 228/255.0),
#
#                       (0.201, 140 / 255.0, 140 / 255.0),
#                      (0.4, 140/255.0, 140/255.0),
#
#                       (0.401, 85 / 255.0, 85 / 255.0),
#                      (0.60,  85/255.0, 85/255.0),
#
#                      (0.601, 24/255.0, 24/255.0),
#                      (0.80, 24/255.0, 24/255.0),
#
#                      (0.801, 5 / 255.0, 5 / 255.0),
#                      (0.999, 5/255.0, 5/255.0),
#
#                      (1.00, 0, 0)],
#
#              'blue':  [(0.00, 64/255.0, 64/255.0),
#                      (0.2, 64/255.0, 64/255.0),
#
#                      (0.201, 48 / 255.0, 48 / 255.0),
#                      (0.4, 48/255.0, 48/255.0),
#
#                      (0.401, 25 / 255.0, 25 / 255.0),
#                      (0.60,  25/255.0, 25/255.0),
#
#                      (0.601, 2 / 255.0, 2 / 255.0),
#                      (0.80, 2/255.0, 2/255.0),
#
#                      (0.801, 0 / 255.0, 0 / 255.0),
#                      (0.999, 0/255.0, 0/255.0),
#
#                      (1.00, 0, 0)],
#
#              'alpha': [ (0.0, 0.0, 0.0),
#                         (0.01, 0.8, 0.8),
#                        (0.20, 0.8, 0.8),
#                        # (0.30, 0.9, 1.0),
#                        # (0.50, 1.0, 1.0),
#                        # (0.70, 1.0, 1.0),
#                        # (0.80, 1.0, 1.0),
#                        # (0.90, 1.0, 1.0),
#                        (1.00, 0.8, 0.8)]}
#
#     return LinearSegmentedColormap('aurora', stops)
#
# def add_lake(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/Solareclipse/ne_50m_lakes","ne_50m_lakes.shp")
#     proj = ccrs.PlateCarree()
#     reader = Reader(path)
#     provinces = reader.geometries()
#     ax.add_geometries(provinces, proj, **kwargs)
#     reader.close()
#
# def add_river(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/Solareclipse/ne_50m_rivers_lake_centerlines","ne_50m_rivers_lake_centerlines.shp")
#     proj = ccrs.PlateCarree()
#     reader = Reader(path)
#     provinces = reader.geometries()
#     ax.add_geometries(provinces, proj, **kwargs)
#     reader.close()
#
# def add_us_state(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/Solareclipse/us-state-boundaries","us-state-boundaries.shp")
#     proj = ccrs.PlateCarree()
#     reader = Reader(path)
#     provinces = reader.geometries()
#     ax.add_geometries(provinces, proj, **kwargs)
#     reader.close()
# def add_europe_county(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/Solareclipse/world-administrative-boundaries","world-administrative-boundaries.shp")
#     proj = ccrs.PlateCarree()
#     reader = Reader(path)
#     provinces = reader.geometries()
#     ax.add_geometries(provinces, proj, **kwargs)
#     reader.close()
#
# def add_MNG_county(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/Solareclipse/MNG","world-administrative-boundaries.shp")
#     proj = ccrs.PlateCarree()
#     reader = Reader(path)
#     provinces = reader.geometries()
#     ax.add_geometries(provinces, proj, **kwargs)
#     reader.close()
#
# def add_america_county(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/SolarEclipse","america.geojson")
#     tracks = gpd.read_file(path)
#     proj = ccrs.PlateCarree()
#     # grab x and y of the first geometry object
#     ax.add_geometries(tracks.geometry, proj, **kwargs)
#
#
# def add_africa_county(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/SolarEclipse","africa.geojson")
#     tracks = gpd.read_file(path)
#     proj = ccrs.PlateCarree()
#     # grab x and y of the first geometry object
#     ax.add_geometries(tracks.geometry, proj, **kwargs)
#
# def add_asia_county(ax, **kwargs):
#
#     path = os.path.join(basedir,"static/SolarEclipse","asia.geojson")
#     tracks = gpd.read_file(path)
#     proj = ccrs.PlateCarree()
#     # grab x and y of the first geometry object
#     ax.add_geometries(tracks.geometry, proj, **kwargs)
#
# def add_china_province(ax,**kwargs):
#
#     path = os.path.join(basedir,"static/SolarEclipse","china_province.geojson")
#     tracks = gpd.read_file(path)
#     proj = ccrs.PlateCarree()
#     # grab x and y of the first geometry object
#     ax.add_geometries(tracks.geometry, proj, **kwargs)
