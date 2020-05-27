# This file is to test different libraries for getting the sun's position

# Error in get_pos_pvlib_pyephem

# python3 -m pip install pysolar, pvlib, pyemphem, ephem, pyephem_sunpath

import datetime
import pandas
import numpy as np
# import math
import matplotlib.pyplot as plt

# https://pysolar.readthedocs.io/en/latest/
import pysolar

# https://pvlib-python.readthedocs.io/en/stable/index.html
import pvlib

# https://rhodesmill.org/pyephem/
import ephem

# https://pypi.org/project/pyephem-sunpath/
from pyephem_sunpath.sunpath import sunpos as pyephem_sunpath

def get_pos_pysolar(lat, lon, date):
    # https://pysolar.readthedocs.io/en/latest/
    # radiation.get_radiation_direct(date, altitude_deg)
    return pysolar.solar.get_altitude(lat, lon, date), pysolar.solar.get_azimuth(lat, lon, date)

def get_pos_pvlib(lat, lon, date):
    # https://pvlib-python.readthedocs.io/en/stable/_modules/pvlib/solarposition.html
    pv = pvlib.solarposition.get_solarposition(date, lat, lon)
    return (pv["apparent_elevation"][0], pv["azimuth"][0])


def get_pos_pvlib_pyephem(lat,lon,date):
    # https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.solarposition.pyephem.html
    # dt = pandas.DatetimeIndex(pandas.dataframe pandas.to_datetime(date))
    dt = pandas.DatetimeIndex(date)
    # ERROR with time formatting
    # return pvlib.solarposition.pyephem(dt,lat,lon)
    pass

def get_pos_ephem(lat,lon,date):
    obs = ephem.Observer()
    # converting lat, lon to str is necessary
    # see https://github.com/santoshphilip/pyephem_sunpath/blob/5be95e456e179678658c590a381eed5f325c6ea5/pyephem_sunpath/sunpath.py#L31
    obs.lat, obs.lon, obs.date = str(lat), str(lon), date.strftime('%Y/%m/%d %H:%M:%S')
    sun = ephem.Sun()
    sun.compute(obs)
    return sun.alt * 180/np.pi, sun.az * 180/np.pi
    # return math.degrees(sun.alt), math.degrees(sun.az)

def get_pos_pyephem_sunpath(lat,lon,date):
    # https://github.com/santoshphilip/pyephem_sunpath
    return pyephem_sunpath(date, lat, lon, 0) #timezone = 0 -> GMT

def test():
    lat, lon = 29.6483, -82.3494 #UF
    date = datetime.datetime(2020, 5, 27, 12, 13, 1, 130320, tzinfo=datetime.timezone.utc)

    print( get_pos_pysolar(lat, lon, date) )
    print( get_pos_pvlib(lat, lon, date) )
    print( get_pos_ephem(lat,lon,date) )
    print( get_pos_pyephem_sunpath(lat,lon,date) )
# test()

def get_pos_hours(f):
    lat, lon = 29.6483, -82.3494 #UF
    date = datetime.datetime(2020, 5, 27, 12, 13, 1, 130320, tzinfo=datetime.timezone.utc)
    hours = 24
    return np.asarray( [f(lat, lon, date - datetime.timedelta(hours=i)) for i in range(hours)] )

def plot():
    fs = [get_pos_pysolar, get_pos_pvlib, get_pos_ephem, get_pos_pyephem_sunpath]
    for i in range(len(fs)):
        plt.plot(get_pos_hours(fs[i])+i*4)
    plt.xticks(range(24))
    plt.axis([0,23,-50,400])
    plt.show()
plot()
