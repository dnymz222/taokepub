import os.path

from . import tide

from config import basedir

import xarray as xr

import json

import numpy as np

import math
import gzip

from  mpmath import sec
import shutil


def longitude_to_360(lon):
    """ Convert longitude (DD) to 0 to 360 degree range. """
    if isinstance(lon, np.ndarray):
        lon = np.atleast_1d(lon)
    return lon % 360

def longitude_to_180(lon):
    """ Convert longitude (DD) to -180 to 180 degree range. """
    if isinstance(lon, np.ndarray):
        lon = np.atleast_1d(lon)
    return ((lon + 180) % 360) - 180



def tile_to_longitude(x, z):
        longitude = float(x / math.pow(2, z) * 360 - 180)
        return longitude

def tile_to_latitude(y, z):
        n = float(math.pi - 2 * math.pi * y / math.pow(2, z))
        latitude = float(180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
        return latitude


def longitude_to_tile(longitude, z):
    x =  (longitude + 180) / 360 * math.pow(2, z)
    return int(x)

def longitude_to_tile_float(longitude, z):
    x =  (longitude + 180) / 360.0 * math.pow(2, z)
    return x


def latitude_to_tile(latitude, z):
    lat_rad = latitude / 180.0 * math.pi
    n = math.pow(2, z)
    ytile = n * (1 - (math.log(math.tan(lat_rad) + sec(lat_rad)) / math.pi)) / 2
    return ytile



def latIndex(lat):
    latvalue = lat + 90
    return int(round(latvalue * 30))

def lngIndex(lng):
    lngvalue = 0
    if lng < 1 / 60 :
        lngvalue = lng  + 360
    else:
        lngvalue = lng
    return int(round(lngvalue * 30 - 1))

@tide.route("/china/size")
def tile_to_northpacific_coordinates():

    n = 900
    m = 1200

    startx = 105
    starty = latitude_to_tile(41,6)
    endx  = 135
    endy =  latitude_to_tile(1,6)
    x1 = longitude_to_tile_float(105,6)
    x2 = longitude_to_tile_float(135,6)



    deltay = (endy - starty) / m

    deltax = (x2 - x1) / n
    print("vale")
    print(deltay)
    print(deltax)
    print("scale")
    print(deltay/deltax )


    list = []

    for j in range(0,m + 1):
        for i in range(0,n + 1):
            dict = {}

            lng = startx +  1 / 30.0 * i
            if lng > 180:
                lng = lng - 360
            dict["lng"] = lngIndex(lng)
            lattile = starty + j * deltay
            lat = tile_to_latitude(lattile,6)
            dict["lat"] = latIndex(lat)
            dict["h"] = []
            dict["i"] = i
            dict["j"] = j

            list.append(dict)

        print(lat)
    return list



def tile_to_geographical_coordinates(x, y, z,mds):
    '''
    Function to convert tile bounds to geographical coordinates.
    Based on geographical system we have pairs:
        1. NorthWest: [lat_north, lng_west]
        2. SouthWest: [lat_end_south, lng_west]
        3. NorthEast: [lat_north, lng_end_east]
        4. SouthEast: [lat_end_south, lng_end_west]
    '''



    lat_north = tile_to_latitude(y, z)
    lat_end_south = tile_to_latitude(y + 1, z)
    lng_east = tile_to_longitude(x, z)
    lng_end_west = tile_to_longitude(x + 1, z)

    n = 128
    m = 128
    latdelta = 1 / (m + 0.0)
    # latdelta = (lat_end_south - lat_north) / m
    lngdelta = (lng_end_west - lng_east) / n
    list = []
    location = json.dumps({"lat": lat_north, "lng": lng_east, "lat_end": lat_end_south, "lng_end": lng_end_west})

    print(location)
    for i in range(0,m):
        for j in range(0,n):
            sy = y + latdelta * i
            lat = tile_to_latitude(sy, z)
            # lat = lat_north + i * latdelta
            lng = lng_east + j * lngdelta
            dict = {}
            dict["lat"] = latIndex(lat)
            dict["lng"] = lngIndex(lng)
            dict["h"] = []
            dict["u"] = []
            list.append(dict)
    # if lat_end_south > 42 or lat_north < 2:
    #     return False, list
    # elif lng_east > 145 or lng_end_west < 105:
    #     return False, list
    # if  lat_end_south > 65 or lat_north<-55 :
    have = False
    for dict in list:
            lat = dict["lat"]
            lng = dict["lng"]
            him = mds["hIm"][lng].values
            hre = mds["hRe"][lng].values
            himvalue = him[lat]
            hrevalue = hre[lat]
            if abs(float(himvalue)) > 0.0001 or abs(float(hrevalue)) > 0.0001:
                have = True
                break

    return have, list








def tile_to_geographical_coordinates2(x, y, z):



    lat_north = tile_to_latitude(y, z)
    lat_end_south = tile_to_latitude(y + 1, z)
    lng_east = tile_to_longitude(x, z)
    lng_end_west = tile_to_longitude(x + 1, z)
    latdelta = 1.0 / 128.0
    lngdelta = (lng_end_west - lng_east) / 128.0
    list = []
    location = json.dumps({"lat": lat_north, "lng": lng_east, "lat_end": lat_end_south, "lng_end": lng_end_west})
    print(location)
    for i in range(0,8):
        for j in range(0,8):
            sy = y + (i * 16 + 8) * latdelta
            lat = tile_to_latitude(sy,z)
            lng = lng_east + (j*16+8) * lngdelta
            dict = {}
            dict["lat"] = latIndex(lat)
            dict["lng"] = lngIndex(lng)
            dict["h"] = []
            dict["u"] = []
            list.append(dict)
    if  lat_end_south > 55 or lat_north<-45:
        pass

    # if lat_end_south > 42 or lat_north < 2:
    #     pass
    # elif lng_east > 145 or lng_end_west < 105:
    #     pass

    else:
        vlist = tidetpxoHconstantLocationList2(list)
        filename = "uv_" + str(z)+ "_" + str(x) +"_"+ str(y)
        tpxoPath = os.path.join(basedir, 'static/tileuvnormal',filename)
        jsondata = json.dumps(vlist).encode("utf8")
        have = False
        for hlist in vlist:
            if len(hlist) > 0:
                have = True
                break
        if have:
            with gzip.open(filename=tpxoPath, mode="w", compresslevel=9) as f:
                f.write(jsondata)
                f.close()


    return location


@tide.route("/tpxo/tile")
def tpxotile():
    tpxoPath = os.path.join(basedir, 'static/TPXO')
    constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4", "S1"]
    dslist = []

    n = len(constants)

    filename = "h_" + "m2" + "_tpxo9_atlas_30_v5.nc"
    filepath = os.path.join(tpxoPath, filename)
    mds = xr.open_dataset(filepath)


    for i in range(0,n):
        cons = constants[i]
        c = cons.lower()
        filename =  "h_"+ c +"_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)
        print(ds)
        dslist.append(ds)


    for z in range(0,8):
        for x in range(65,int(pow(2,z)+0.1)):
            for y in range(0, int(pow(2,z)+0.1)):
                h,list = tile_to_geographical_coordinates(x, y, z,mds)
                if h:
                    filename = "h_" + str(z) + "_" + str(x) + "_" + str(y)
                    print(filename)
                    vlist = tidetpxoHconstantLocationList(list,dslist)
                    msgPath = os.path.join(basedir, 'static/tilenormal', filename)
                    msgdata = json.dumps(vlist).encode("utf8")

                    with gzip.open(filename=msgPath, mode="w", compresslevel=9) as f:
                            f.write(msgdata)
                            f.close()
    for ds in dslist:
        ds.close()
    mds.close()
    return "done"


@tide.route("/tpxo/northpacific/tile")
def tpxonorthpacifictile():
    tpxoPath = os.path.join(basedir, 'static/TPXO')
    constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4", "S1"]
    dslist = []

    n = len(constants)

    filename = "h_" + "m2" + "_tpxo9_atlas_30_v5.nc"
    filepath = os.path.join(tpxoPath, filename)
    mds = xr.open_dataset(filepath)


    for i in range(0,n):
        cons = constants[i]
        c = cons.lower()
        filename =  "h_"+ c +"_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)
        print(ds)
        dslist.append(ds)



    try:

        list = tile_to_northpacific_coordinates()


        for dict in list:
            lat = dict["lat"]
            lng = dict["lng"]
            print(str(dict["i"])+ "_" +str( dict["j"]))
            him = mds["hIm"][lng].values
            hre = mds["hRe"][lng].values
            himvalue = him[lat]
            hrevalue = hre[lat]
            if abs(float(himvalue)) > 0.0001 or abs(float(hrevalue)) > 0.0001:
                dict["have"] = True
            else:
                dict["have"] = False

        prePath = os.path.join(basedir, 'static/downloads', "tile_china_pre")
        predata = json.dumps(list).encode("utf8")

        with gzip.open(filename=prePath, mode="w", compresslevel=9) as pf:
            pf.write(predata)
            pf.close()



        vlist = tidetpxoNorthPacificHconstantLocationList(list, dslist)

        msgPath = os.path.join(basedir, 'static/downloads', "tile_china")
        msgdata = json.dumps(vlist).encode("utf8")

        with gzip.open(filename=msgPath, mode="w", compresslevel=9) as f:
            f.write(msgdata)
            f.close()
    except Exception as e:
        print(e)

    for ds in dslist:
        ds.close()

    mds.close()
    return "done"



@tide.route("/tpxo/tile2")
def tpxotile2():
    for z in range(7,9):
        for x in range(0,int(pow(2,z)+0.1)):
        # for x in range(0, 1):
            for y in range(0,int(pow(2,z)+0.1)):
                tile_to_geographical_coordinates2(x, y, z)
    return "done"

@tide.route("/tpxo/tile/file")
def tpxotilefile():
    tpxoPath = os.path.join(basedir, 'static/tilenormal')
    rezippath = os.path.join(basedir, 'static/tilenormal3')
    list = []
    if os.path.exists(rezippath):
        pass
    else:
        os.makedirs(rezippath)

    for parent, _, fileNames in os.walk(tpxoPath):
        for filename in fileNames:
            if filename.find("DS_Store")< 0:
                print(filename)
                path = os.path.join(tpxoPath,filename)
                fo = open(path,"rb")
                data = fo.read()
                decomoressdata = gzip.decompress(data)
                repath = os.path.join(rezippath,filename)
                with gzip.open(filename=repath, mode="w", compresslevel=3) as f:
                    f.write(decomoressdata)
                    f.close()
                fo.close()
    return "done"




@tide.route("/tpxo/tile/file2")
def tpxotilefile2():
    tpxoPath = os.path.join(basedir, 'static/tilelp')
    rezippath = os.path.join(basedir, 'static/tilelpm')
    list = []


    for parent, _, fileNames in os.walk(tpxoPath):
        for filename in fileNames:
            if filename.find("DS_Store")< 0:
                print(filename)
                path = os.path.join(tpxoPath,filename)
                fo = open(path,"rb")
                data = fo.read()
                decomoressdata = gzip.decompress(data)
                repath = os.path.join(rezippath,"l_"+ filename)
                with gzip.open(filename=repath, mode="w", compresslevel=5) as f:
                    f.write(decomoressdata)
                    f.close()
                fo.close()
    return  "done"


@tide.route("/tpxo/db")
def tpxoword():
    consname = ["m2", "s2", "k1", "o1", "n2", "p1", "k2", "q1", "2n2", "m4", "mf", "mm", "mn4", "ms4","s1"]
    CONST_ID = ["m2", "s2", "k1", "o1",
                            "n2", "p1", "k2", "q1",
                            "2n2", "mu2", "nu2", "l2",
                            "t2", "j1", "m1", "oo1",
                            "rho1", "mf", "mm", "ssa",
                            "m4", "ms4", "mn4", "m6",
                            "m8", "mk3", "s6", "2sm2",
                            "2mk3", "s1"]
    cindex = ["sa", "ssa", "mm", "msf", "mf", "mt", "alpha1", "2q1", "sigma1",
              "q1", "rho1", "o1", "tau1", "m1", "chi1", "pi1", "p1", "s1", "k1",
              "psi1", "phi1", "theta1", "j1", "oo1", "2n2", "mu2", "n2", "nu2",
              "m2a", "m2", "m2b", "lambda2", "l2", "t2", "s2", "r2", "k2", "eta2",
              "mns2", "2sm2", "m3", "mk3", "s3", "mn4", "m4", "ms4", "mk4", "s4",
              "s5", "m6", "s6", "s7", "s8"]

    cid8 = ["q1", "o1", "p1", "k1", "n2", "m2", "s2", "k2"]

    list = []
    for c in cid8:
        list.append(consname.index(c))
    print(list)
    return json.dumps(list)





@tide.route("/tide/tpxo/constant/all/<lat>/<lng>")
def tidetpxosingleloctation(lat,lng):
    latindex = latIndex(float(lat))
    lngindex = lngIndex(float(lng))
    return tidetpxoconstantsingleLocation(latindex,lngindex)

def tidetpxoconstantsingleLocation(lat,lng):
    tpxoPath = os.path.join(basedir, 'static/TPXO')
    list = []

    dict = {}
    dict["lng"] = lng
    dict["lat"] = lat
    dict["h"] = []
    dict["u"] = []
    dict["grid"] = []
    list.append(dict)


    constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4","S1"]

    #h
    for cons in constants:
        c = cons.lower()
        filename =  "h_"+ c +"_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)
        # print(ds)
        him = ds["hIm"][lng].values
        hre = ds["hRe"][lng].values
        for dict in list:
            lat = dict["lat"]
            himvalue = him[lat]
            hrevalue = hre[lat]

            hlist = dict["h"]

            if c == "m2":
                if abs(float(himvalue)) < 0.0001 and abs(float(hrevalue)) < 0.0001:
                    dict["value"] = False
                else:
                    dict["value"] = True
            hlist.append(int(himvalue))
            hlist.append(int(hrevalue))
        ds.close()


    for con in constants:
        c = con.lower()
        try:
            filename =  "u_"+ c +"_tpxo9_atlas_30_v5.nc"
            filepath = os.path.join(tpxoPath, filename)
            ds = xr.open_dataset(filepath, engine="netcdf4")
            uim = ds["uIm"][lng].values
            ure = ds["uRe"][lng].values

            vim = ds["vIm"][lng].values
            vre = ds["vRe"][lng].values

            for dict in list:
                lat = dict["lat"]
                uimvalue = uim[lat]
                urevalue = ure[lat]
                vimvalue = vim[lat]
                vrevalue = vre[lat]

                ulist = dict["u"]
                ulist.append(int(uimvalue))
                ulist.append(int(urevalue))
                ulist.append(int(vimvalue))
                ulist.append(int(vrevalue))
            ds.close()
        except Exception as e:
            print(e)

    if 1:
        filename = "grid_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)
        # print(ds)
        hu = ds["hu"][lng].values
        hv = ds["hv"][lng].values
        hz = ds["hz"][lng].values

        for dict in list:
            lat = dict["lat"]
            huvalue = hu[lat]
            hvvalue = hv[lat]
            hzvalue = hz[lat]

            hlist = dict["grid"]
            hlist.append(float(huvalue))
            hlist.append(float(hvvalue))
            hlist.append(float(hzvalue))
        ds.close()

    print(list[0]["h"])
    print(list[0]["u"])
    print(list[0]["grid"])

    return json.dumps(list[0])


def tidetpxoHconstantLocationList(list,dslist):
    tpxoPath = os.path.join(basedir, 'static/TPXO')


    constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4","S1"]
    # constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1"]

    n = len(constants)
    #h
    for i in range(0,n):
        cons = constants[i]
        c = cons.lower()
        # filename =  "h_"+ c +"_tpxo9_atlas_30_v5.nc"
        # filepath = os.path.join(tpxoPath, filename)
        ds = dslist[i]

        for dict in list:
            lat = dict["lat"]
            lng = dict["lng"]
            him = ds["hIm"][lng].values
            hre = ds["hRe"][lng].values
            himvalue = him[lat]
            hrevalue = hre[lat]

            hlist = dict["h"]

            if c == "m2":
                if abs(float(himvalue)) < 0.0001 and abs(float(hrevalue)) < 0.0001:
                    dict["value"] = False
                else:
                    dict["value"] = True
            hlist.append(int(himvalue))
            hlist.append(int(hrevalue))
        # ds.close()



    vlist = []
    for dict in list:
        if dict["value"]:
            hlist = dict["h"]
            vlist.append(hlist)
        else:
            vlist.append([])
    return vlist

def tidetpxoNorthPacificHconstantLocationList(list, dslist):
        tpxoPath = os.path.join(basedir, 'static/TPXO')

        constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4", "S1"]
        # constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1"]

        n = len(constants)

        vlist = []

        for dict in list:
            lat = dict["lat"]
            lng = dict["lng"]
            print( str(dict["i"]) + "_"  + str(dict["j"]))
            have = dict["have"]
            if have:
                hlist = []
                for i in range(0, n):

                    ds = dslist[i]
                    him = ds["hIm"][lng].values
                    hre = ds["hRe"][lng].values
                    himvalue = him[lat]
                    hrevalue = hre[lat]
                    hlist.append(int(himvalue))
                    hlist.append(int(hrevalue))

                vlist.append(hlist)


            else:
                vlist.append([])

        return vlist

    # return json.dumps(list[0])

def tidetpxoHconstantLocationList2(list):
    tpxoPath = os.path.join(basedir, 'static/TPXO')


    # constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1", "2N2", "M4", "MF", "MM", "MN4", "MS4","S1"]
    constants = ["M2", "S2", "K1", "O1", "N2", "P1", "K2", "Q1"]

    if 1:
        filename = "grid_tpxo9_atlas_30_v5.nc"
        filepath = os.path.join(tpxoPath, filename)
        ds = xr.open_dataset(filepath)

        for dict in list:
            lat = dict["lat"]
            lng = dict["lng"]
            hz = ds["hz"][lng].values
            hzvalue = hz[lat]
            ulist = dict["u"]
            if hzvalue > 200:
                pass
            else:
                ulist.append(int(round(hzvalue * 1000)))

        ds.close()



    for con in constants:
        c = con.lower()
        try:
            filename =  "u_"+ c +"_tpxo9_atlas_30_v5.nc"
            filepath = os.path.join(tpxoPath, filename)
            ds = xr.open_dataset(filepath, engine="netcdf4")
            for dict in list:
                ulist = dict["u"]
                if len(ulist) < 1:
                    dict["value"] = False
                else:
                    lat = dict["lat"]
                    lng = dict["lng"]

                    uim = ds["uIm"][lng].values
                    ure = ds["uRe"][lng].values

                    vim = ds["vIm"][lng].values
                    vre = ds["vRe"][lng].values
                    uimvalue = uim[lat]
                    urevalue = ure[lat]
                    vimvalue = vim[lat]
                    vrevalue = vre[lat]

                    if c == "m2":
                        if abs(float(vimvalue)) < 0.0001 and abs(float(vrevalue)) < 0.0001 and abs(float(uimvalue)) < 0.0001 and abs(float(urevalue)) < 0.0001:
                            dict["value"] = False
                        else:
                            dict["value"] = True

                    ulist.append(int(uimvalue))
                    ulist.append(int(urevalue))
                    ulist.append(int(vimvalue))
                    ulist.append(int(vrevalue))
            ds.close()
        except Exception as e:
            print(e)
    vlist = []
    for dict in list:
        if dict["value"]:
            ulist = dict["u"]
            vlist.append(ulist)
        else:
            vlist.append([])
    return vlist


def indexfilenanme(filename):
    list = filename.split("_")
    z = int(list[1])
    x = int(list[2])
    y = int(list[3])
    forwardindex = 0
    for i in range(0,z):
        if i == 0:
            forwardindex += 1
        else:
            index = 1
            for j in range(0,i):
                index *= 4
            forwardindex += index
    colnumbers = 1<<z
    nowindex = y * colnumbers + x
    totalnumbers = forwardindex + nowindex
    return str(totalnumbers)



@tide.route("/tide/aaplus")
def tpxoenaaplus():
    tpxoPath = os.path.join(basedir, 'static/aaplus')



    for parent, _, fileNames in os.walk(tpxoPath):
        for filename in fileNames:
            if filename.find("DS_Store")< 0:
                print("src/main/cpp/aaplus/"+filename)

    return "done"


@tide.route("/vnl10/move")
def vnl10move():
    download_path = os.path.join(basedir, 'static/vnl202410')
    move_path = os.path.join(basedir, 'static/vnl2024')
    emptydict = {}
    for z in range(10, 11):
        for x in range(0, int(pow(2, z) + 0.1)):
            for y in range(0, int(pow(2, z) + 0.1)):
                try:

                    wname = str(z) + "_" + str(x) + "_" + str(y) + ".webp"

                    fPath = os.path.join(download_path, wname)
                    mpath = os.path.join(move_path, wname)

                    if os.path.exists(fPath):
                        shutil.move(fPath, mpath)
                    else:
                        continue
                    print(wname)

                except Exception as e:
                    print(e)

    return "done"


    return "done"