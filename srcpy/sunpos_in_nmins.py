# The goal is to find the sun's position at the midpoint between now and some time.
# Calculations are in radians for this file

import numpy as np
import datetime
import pvlib
from matplotlib import pyplot as plt

def get_pos_pvlib_radians(lat, lon, alt, date):
    # https://pvlib-python.readthedocs.io/en/stable/_modules/pvlib/solarposition.html
    pv = pvlib.solarposition.get_solarposition(date, lat, lon, altitude=alt)
    return (np.deg2rad(pv["apparent_elevation"][0]), np.deg2rad(pv["azimuth"][0]))

def get_spos_after_nmins(nmins):
    lat, lon, alt, tz = 29.6483, -82.3494, 32, -4 #UF
    # lat, lon, tz = 38.9325, -95.6784, -5 #Heartland motorsports park
    date = datetime.datetime.now() + datetime.timedelta(minutes=nmins)
    s_a1 = get_pos_pvlib_radians(lat, lon, alt, date - datetime.timedelta(hours=tz))
    print(  date  )
    print(  s_a1, np.rad2deg(s_a1[0]), np.rad2deg(s_a1[1])  )
get_spos_after_nmins(60)
