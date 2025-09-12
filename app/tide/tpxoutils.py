import math
import bisect

import numpy as np
import xarray as xr
from pymeeus.Epoch import Epoch

from .tidal_constituents import CONST_ID

__all__ = [
    'astrol',
    'nodal',
    'infer_minor',

    ]


def astrol(mjd):
    """
    Computes the basic astronomical mean longitudes  s, h, p, N.
    Note N is not N', i.e. N is decreasing with time.
    These formulae are for the period 1990 - 2010, and were derived
    by David Cartwright (personal comm., Nov. 1990).
    mjd is UTC in decimal MJD.

    All longitudes returned in degrees.
    R. D. Ray    Dec. 1990

    Non-vectorized version.

    """
    circle = 360.0


    t = calc_deltaT(jd=mjd)
    tjd = mjd + t

    T = (tjd - 2451545.0) / 36525.0


    s = 218.3166328 + 481267.88114585 * T - 0.001599322 * T * T + 1.855835e-6 * T * T * T - 1.53388e-8 * T * T * T * T;


    D = (((-8.8445e-9 * T + 1.83195e-6) * T - 1.8819e-3) * T +
         445267.1114034) * T + 297.8501921


    h = s - D


    p = ((-1.249172e-5 * T - 1.032e-2) * T + 4069.0137287) * T + 83.3532465

    N = ((2.22222e-6 * T + 2.0708e-3) * T - 1934.136261) * T + 125.04452

    pp = 282.94 + 1.7192 * T
    #
    # T = mjd - 51544.4993
    #
    # # mean longitude of moon
    # s = 218.3164 + 13.17639648 * T
    #
    # # mean longitude of sun
    # h = 280.4661 +  0.98564736 * T
    #
    # # mean longitude of lunar perigee
    # p =  83.3535 +  0.11140353 * T
    #
    # # mean longitude of ascending lunar node
    # N = 125.0445 -  0.05295377 * T

    s = np.mod(s, circle)
    h = np.mod(h, circle)
    p = np.mod(p, circle)
    N = np.mod(N, circle)

    return s, h, p, N


def calc_deltaT(jd):
    year = (jd - 1721059.5) / 365.2425
    dt = 0
    t = 0
    if year < -500:
        t = (year - 1820) / 100
        dt = -20 + 32 * t * t
    elif year >= -500 and year < 500 :
        t = year / 100
        dt = 10583.6 - 1014.41 * t + 33.78311 * t * t - 5.952053 * t * t * t - 0.1798452 * t * t * t * t + 0.022174192 * t * t * t * t * t + 0.0090316521 * t * t * t * t * t * t
    elif year >= 500 and year < 1600 :
        t = (year - 1000) / 100
        dt = 1574.2 - 556.01 * t + 71.23472 * t * t + 0.319781 * t * t * t - 0.8503463 * t * t * t * t - 0.005050998 * t * t * t * t * t + 0.0083572073 * t * t * t * t * t * t
    elif year >= 1600 and year < 1700 :
        t = year - 1600
        dt = 120 - 0.9808 * t - 0.01532 * t * t + t * t * t / 7129
    elif year >= 1700 and year < 1800 :
        t = year - 1700
        dt = 8.83 + 0.1603 * t - 0.0059285 * t * t + 0.00013336 * t * t * t - t * t * t * t / 1174000
    elif year >= 1800 and year < 1860 :
        t = year - 1800
        dt = 13.72 - 0.332447 * t + 0.0068612 * t * t + 0.0041116 * t * t * t - 0.00037436 * t * t * t * t + 0.0000121272 * t * t * t * t * t - 0.0000001699 * t * t * t * t * t * t + 0.000000000875 * t * t * t * t * t * t * t
    elif year >= 1860 and year < 1900 :
        t = year - 1860
        dt = 7.62 + 0.5737 * t - 0.251754 * t * t + 0.01680668 * t * t * t - 0.0004473624 * t * t * t * t + t * t * t * t * t / 233174
    elif year >= 1900 and year < 1920 :
        t = year - 1900
        dt = -2.79 + 1.494119 * t - 0.0598939 * t * t + 0.0061966 * t * t * t - 0.000197 * t * t * t * t
    elif year >= 1920 and year < 1941 :
        t = year - 1920
        dt = 21.20 + 0.84493 * t - 0.076100 * t * t + 0.0020936 * t * t * t
    elif year >= 1941 and year < 1961 :
        t = year - 1950
        dt = 29.07 + 0.407 * t - t * t / 233 + t * t * t / 2547
    elif year >= 1961 and year < 1986 :
        t = year - 1975
        dt = 45.45 + 1.067 * t - t * t / 260 - t * t * t / 718
    elif year >= 1986 and year < 2005 :
        t = year - 2000
        dt = 63.86 + 0.3345 * t - 0.060374 * t * t + 0.0017275 * t * t * t + 0.000651814 * t * t * t * t + 0.00002373599 * t * t * t * t * t
    elif year >= 2005 and year < 2050 :
        t = year - 2000
        dt = 62.92 + 0.32217 * t + 0.005589 * t * t
    elif year >= 2050 and year < 2150 :
        t = (year - 1820) / 100
        dt = -20 + 32 * t * t - 0.5628 * (2150 - year)
    else :
        t = (year - 1820) / 100
        dt = -20 + 32 * t * t

    return dt


def nodal(mjd:float, constit:list):
    """
    Calculates the nodal corrections for tidal constituents.

    Parameters
    ----------
    mjd : float
        Modified Julian Day (MJD) since 1992-01-01.
    constit : list
        List of constituents to use.

    Returns
    -------
    pf, pu : np.ndarray
        Nodal corrections for the constituents.

    """
    # index_labels = ['m2', 's2', 'k1', 'o1', 'n2', 'p1', 'k2', 'q1', '2n2', 'mu2',
    #                 'nu2', 'l2', 't2', 'j1', 'm1', 'oo1', 'rho1', 'mf', 'mm', 'ssa',
    #                 'm4', 'ms4', 'mn4', 'mk3', 's6', '2sm2']
    # index = [29, 34, 18, 11, 26, 16, 36,  9, 24, 25,
    #          27, 32, 33, 22, 13, 23, 10,  4,  2,  1,
    #          44, 45, 43, 49, 41, 50, 39]




    pp = 282.94     # solar perigee at epoch 2000
    rad = math.pi/180

    hour = (mjd - int(mjd)) * 24.0
    t1 = 15.0 * hour
    t2 = 30.0 * hour

    # get the basic astronomical mean longitudes
    s, h, p, omega = astrol(mjd)
    # list of all constituents available for this function
    cindex = ['sa', 'ssa', 'mm', 'msf', 'mf', 'mt', 'alpha1', '2q1', 'sigma1',
              'q1', 'rho1', 'o1', 'tau1', 'm1', 'chi1', 'pi1', 'p1', 's1', 'k1',
              'psi1', 'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'n2', 'nu2',
              'm2a', 'm2', 'm2b', 'lambda2', 'l2', 't2', 's2', 'r2', 'k2', 'eta2',
              'mns2', '2sm2', 'm3', 'mk3', 's3', 'mn4', 'm4', 'ms4', 'mk4', 's4',
              's5', 'm6', 's6', 's7', 's8']

    sinn = np.sin(omega*rad)
    cosn = np.cos(omega*rad)
    sin2n = np.sin(2*omega*rad)
    cos2n = np.cos(2*omega*rad)
    sin3n = np.sin(3*omega*rad)

    # arg not needed!
    arg = np.empty((53), dtype=np.float64)
    arg[0]  = h - pp                    # Sa
    arg[1]  = 2*h                       # Ssa
    arg[2]  = s - p                     # Mm
    arg[3]  = 2*s - 2*h                 # MSf
    arg[4]  = 2*s                       # Mf
    arg[5]  = 3*s - p                   # Mt
    arg[6]  = t1 - 5*s + 3*h + p - 90   # alpha1
    arg[7]  = t1 - 4*s + h + 2*p - 90   # 2Q1
    arg[8]  = t1 - 4*s + 3*h - 90       # sigma1
    arg[9]  = t1 - 3*s + h + p - 90     # q1
    arg[10] = t1 - 3*s + 3*h - p - 90   # rho1
    arg[11] = t1 - 2*s + h - 90         # o1
    arg[12] = t1 - 2*s + 3*h + 90       # tau1
    arg[13] = t1 - s + h + 90           # M1
    arg[14] = t1 - s + 3*h - p + 90     # chi1
    arg[15] = t1 - 2*h + pp - 90        # pi1
    arg[16] = t1 - h - 90               # p1
    arg[17] = t1 + 90                   # s1
    arg[18] = t1 + h + 90               # k1
    arg[19] = t1 + 2*h - pp + 90        # psi1
    arg[20] = t1 + 3*h + 90             # phi1
    arg[21] = t1 + s - h + p + 90       # theta1
    arg[22] = t1 + s + h - p + 90       # J1
    arg[23] = t1 + 2*s + h + 90         # OO1
    arg[24] = t2 - 4*s + 2*h + 2*p      # 2N2
    arg[25] = t2 - 4*s + 4*h            # mu2
    arg[26] = t2 - 3*s + 2*h + p        # n2
    arg[27] = t2 - 3*s + 4*h - p        # nu2
    arg[28] = t2 - 2*s + h + pp         # M2a
    arg[29] = t2 - 2*s + 2*h            # M2
    arg[30] = t2 - 2*s + 3*h - pp       # M2b
    arg[31] = t2 - s + p + 180          # lambda2
    arg[32] = t2 - s + 2*h - p + 180    # L2
    arg[33] = t2 - h + pp               # t2
    arg[34] = t2                        # S2
    arg[35] = t2 + h - pp + 180         # R2
    arg[36] = t2 + 2*h                  # K2
    arg[37] = t2 + s + 2*h - pp         # eta2
    arg[38] = t2 - 5*s + 4.0*h + p      # MNS2
    arg[39] = t2 + 2*s - 2*h            # 2SM2
    arg[40] = 1.5*arg[29]               # M3
    arg[41] = arg[18] + arg[29]         # MK3
    arg[42] = 3*t1                      # S3
    arg[43] = arg[26] + arg[29]         # MN4
    arg[44] = 2*arg[29]                 # M4
    arg[45] = arg[29] + arg[34]         # MS4
    arg[46] = arg[29] + arg[36]         # MK4
    arg[47] = 4*t1                      # S4
    arg[48] = 5*t1                      # S5
    arg[49] = 3*arg[29]                 # M6
    arg[50] = 3*t2                      # S6
    arg[51] = 7.0*t1                    # S7
    arg[52] = 4*t2                      # S8


    f = np.empty((53), dtype=np.float64)
    f[0]  = 1                                     # Sa
    f[1]  = 1                                     # Ssa
    f[2]  = 1 - 0.130*cosn                        # Mm
    f[3]  = 1                                     # MSf
    f[4]  = 1.043 + 0.414*cosn                    # Mf
    f[5]  = np.sqrt((1+.203*cosn+.040*cos2n)**2 + (.203*sinn+.040*sin2n)**2)  # Mt
    f[6]  = 1                                     # alpha1
    f[7]  = np.sqrt((1.+.188*cosn)**2+(.188*sinn)**2)  # 2Q1
    f[8]  = f[7]                                  # sigma1
    f[9]  = f[7]                                  # q1
    f[10] = f[7]                                  # rho1
    f[11] = np.sqrt((1.0+0.189*cosn-0.0058*cos2n)**2 + (0.189*sinn-0.0058*sin2n)**2)    # O1
    f[12] = 1                                     # tau1
    tmp1  = 1.36*np.cos(p*rad)+.267*np.cos((p-omega)*rad)  # Ray's
    tmp2  = 0.64*np.sin(p*rad)+.135*np.sin((p-omega)*rad)
    f[13] = np.sqrt(tmp1**2 + tmp2**2)                 # M1
    f[14] = np.sqrt((1.+.221*cosn)**2+(.221*sinn)**2)  # chi1
    f[15] = 1                                     # pi1
    f[16] = 1                                     # P1
    f[17] = 1                                     # S1
    f[18] = np.sqrt((1.+.1158*cosn-.0029*cos2n)**2 + (.1554*sinn-.0029*sin2n)**2)       # K1
    f[19] = 1                                     # psi1
    f[20] = 1                                     # phi1
    f[21] = 1                                     # theta1
    f[22] = np.sqrt((1.+.169*cosn)**2+(.227*sinn)**2)  # J1
    f[23] = np.sqrt((1.0+0.640*cosn+0.134*cos2n)**2 + (0.640*sinn+0.134*sin2n)**2 )      # OO1
    f[24] = np.sqrt((1.-.03731*cosn+.00052*cos2n)**2 + (.03731*sinn-.00052*sin2n)**2)    # 2N2
    f[25] = f[24]                                 # mu2
    f[26] = f[24]                                 # N2
    f[27] = f[24]                                 # nu2
    f[28] = 1                                     # M2a
    f[29] = f[24]                                 # M2
    f[30] = 1                                     # M2b
    f[31] = 1                                     # lambda2
    temp1 = 1.-0.25*np.cos(2*p*rad) - 0.11*np.cos((2*p-omega)*rad) - 0.04*cosn
    temp2 = 0.25*np.sin(2*p) + 0.11*np.sin((2*p-omega)*rad) + 0.04*sinn
    f[32] = np.sqrt(temp1**2 + temp2**2)          # L2
    f[33] = 1                                     # t2
    f[34] = 1                                     # S2
    f[35] = 1                                     # R2
    f[36] = np.sqrt((1.+.2852*cosn+.0324*cos2n)**2 + (.3108*sinn+.0324*sin2n)**2)  # K2
    f[37] = np.sqrt((1.+.436*cosn)**2+(.436*sinn)**2)  # eta2
    f[38] = f[29]**2                              # MNS2
    f[39] = f[29]                                 # 2SM2
    f[40] = 1   # wrong                           # M3
    f[41] = f[18]*f[29]                           # MK3
    f[42] = 1                                     # S3
    f[43] = f[29]**2                              # MN4
    f[44] = f[43]                                 # M4
    f[45] = f[43]                                 # MS4
    f[46] = f[29]*f[36]                           # MK4
    f[47] = 1                                     # S4
    f[48] = 1                                     # S5
    f[49] = f[29]**3                              # M6
    f[50] = 1                                     # S6
    f[51] = 1                                     # S7
    f[52] = 1


    u = np.empty((53), dtype=np.float64)
    u[ 0] = 0                                    # Sa
    u[ 1] = 0                                    # Ssa
    u[ 2] = 0                                    # Mm
    u[ 3] = 0                                    # MSf
    u[ 4] = -23.7*sinn + 2.7*sin2n - 0.4*sin3n   # Mf
    u[ 5] = np.arctan(-(.203*sinn+.040*sin2n)/ (1+.203*cosn+.040*cos2n))/rad   # Mt
    u[ 6] = 0                                    # alpha1
    u[ 7] = np.arctan(.189*sinn/(1.+.189*cosn))/rad      # 2Q1
    u[ 8] = u[7]                                 # sigma1
    u[ 9] = u[7]                                 # q1
    u[10] = u[7]                                 # rho1
    u[11] = 10.8*sinn - 1.3*sin2n + 0.2*sin3n    # O1
    u[12] = 0                                    # tau1
    u[13] = np.arctan2(tmp2,tmp1)/rad            # M1
    u[14] = np.arctan(-.221*sinn/(1.+.221*cosn))/rad     # chi1
    u[15] = 0                                    # pi1
    u[16] = 0                                    # P1
    u[17] = 0                                    # S1
    u[18] = np.arctan((-.1554*sinn+.0029*sin2n)/ (1.+.1158*cosn-.0029*cos2n))/rad   # K1
    u[19] = 0                                    # psi1
    u[20] = 0                                    # phi1
    u[21] = 0                                    # theta1
    u[22] = np.arctan(-.227*sinn/(1.+.169*cosn))/rad     # J1
    u[23] = np.arctan(-(.640*sinn+.134*sin2n)/ (1.+.640*cosn+.134*cos2n))/rad  # OO1
    u[24] = np.arctan((-.03731*sinn+.00052*sin2n)/ (1.-.03731*cosn+.00052*cos2n))/rad  # 2N2
    u[25] = u[24]                                # mu2
    u[26] = u[24]                                # N2
    u[27] = u[24]                                # nu2
    u[28] = 0                                    # M2a
    u[29] = u[24]                                # M2
    u[30] = 0                                    # M2b
    u[31] = 0                                    # lambda2
    u[32] = np.arctan(-temp2/temp1)/rad          # L2
    u[33] = 0                                    # t2
    u[34] = 0                                    # S2
    u[35] = 0                                    # R2
    u[36] = np.arctan(-(.3108*sinn+.0324*sin2n)/ (1.+.2852*cosn+.0324*cos2n))/rad  # K2
    u[37] = np.arctan(-.436*sinn/(1.+.436*cosn))/rad     # eta2
    u[38] = u[29]*2                              # MNS2
    u[39] = u[29]                                # 2SM2
    u[40] = 1.5*u[29]                            # M3
    u[41] = u[29] + u[18]                        # MK3
    u[42] = 0                                    # S3
    u[43] = u[29]*2                              # MN4
    u[44] = u[43]                                # M4
    u[45] = u[29]                                # MS4
    u[46] = u[29]+u[36]                          # MK4
    u[47] = 0                                    # S4
    u[48] = 0                                    # S5
    u[49] = u[29]*3                              # M6
    u[50] = 0                                    # S6
    u[51] = 0                                    # S7
    u[52] = 0                                    # S8

    # filter input constituents based on list of available ones
    constit = [c for c in constit if c.lower() in cindex]
    # get number of constituents to include
    nconstit = len(constit)
    # init output arrays
    pu = np.zeros((nconstit,1))
    pf = np.ones((nconstit,1))

    # add nodal corrections for tidal constituents from input list
    for i, cons in enumerate(constit):
        if cons.lower() in CONST_ID:
            ii = cindex.index(cons)
            #print(f'[INFO]   nodal():  add < {cons.lower()} >')
            pf[i,:] = f[ii]
            pu[i,:] = u[ii] * rad
        else:
            print(f'[WARNING]   nodal(): < {cons.lower()} > not part of primary tidal constituents!')

    return pf, pu



def infer_minor(z, constituents:list, mjd:float, timesteps):
    """
    Calculate the tidal corrections for minor constituents inferred using
    major constituents.

    Parameters
    ----------
    z : np.ndarray
        Complex harmonic constituents (constituents x points).
    constituents : list
        List of tidal constituents.
    mjd : float
        Modified Julian Day (MJD) since 1992-01-01.
    timesteps : np.ndarray
        Array of timesteps in seconds since 1992-01-01.

    Returns
    -------
    dh : np.ndarray
        Tidal height from minor constituents.

    """
    rad = math.pi/180
    PP = 282.8
    cid8 = ['q1','o1','p1','k1','n2','m2','s2','k2']
    ncid8 = len(cid8)

    # number of constituents & number of points (locations)
    nc, npts = z.shape
    # number of timesteps
    nt = len(np.atleast_1d(timesteps))
    # number of data points to calculate
    n = nt if ((npts == 1) & (nt > 1)) else npts
    # init output array
    dh = np.zeros((n))

    # re-order constituents to correspond to cid8
    ncon = len(constituents)
    z8 = np.zeros((ncid8, npts), dtype='complex')
    ni = 0
    for i in range(ncid8):
        for j in range(ncon):
            if constituents[j].lower() == cid8[i]:
                z8[i] = z[j]
                if i not in [2, 7]:
                    ni += 1

    if ni < 6:
        raise ValueError('Not enough constituents for inference!')

    # list of minor constituents
    minor = ['2q1','sigma1','rho1','m12','m11','chi1','pi1','phi1','theta1',
             'j1','oo1','2n2','mu2','nu2','lambda2','l2','l2','t2']
    # only add minor constituents that are not on the list of major values
    minor_indices = [i for i,m in enumerate(minor) if m not in constituents]

    # relationship between major and minor constituent amplitude and phase
    zmin = np.empty((18, n), dtype='complex')
    zmin[0]  = 0.263 * z8[0] - 0.0252 * z8[1]    # 2Q1
    zmin[1]  = 0.297 * z8[0] - 0.0264 * z8[1]    # sigma1
    zmin[2]  = 0.164 * z8[0] + 0.0048 * z8[1]    # rho1 +
    zmin[3]  = 0.0140 * z8[1] + 0.0101 * z8[3]   # M1
    zmin[4]  = 0.0389 * z8[1] + 0.0282 * z8[3]   # M1
    zmin[5]  = 0.0064 * z8[1] + 0.0060 * z8[3]   # chi1
    zmin[6]  = 0.0030 * z8[1] + 0.0171 * z8[3]   # pi1
    zmin[7]  = -0.0015 * z8[1] + 0.0152 * z8[3]  # phi1
    zmin[8]  = -0.0065 * z8[1] + 0.0155 * z8[3]  # theta1
    zmin[9]  = -0.0389 * z8[1] + 0.0836 * z8[3]  # J1 +
    zmin[10] = -0.0431 * z8[1] + 0.0613 * z8[3]  # OO1 +
    zmin[11] = 0.264 * z8[4] - 0.0253 * z8[5]    # 2N2 +
    zmin[12] = 0.298 * z8[4] - 0.0264 * z8[5]    # mu2 +
    zmin[13] = 0.165 * z8[4] + 0.00487 * z8[5]   # nu2 +
    zmin[14] = 0.0040 * z8[5] + 0.0074 * z8[6]   # lambda2
    zmin[15] = 0.0131 * z8[5] + 0.0326 * z8[6]   # L2 +
    zmin[16] = 0.0033 * z8[5] + 0.0082 * z8[6]   # L2 +
    zmin[17] = 0.0585 * z8[6]                    # t2 +

