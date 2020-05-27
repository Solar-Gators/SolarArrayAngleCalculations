import numpy as np
import pandas as pd
import datetime
import pvlib
import tables
from matplotlib import pyplot as plt
# python3 -m pip install tables

# Notes:
# Calculations are in radians for this file

# TODO:
# Consider Solar irradiance
# https://en.wikipedia.org/wiki/Solar_irradiance
# Consider minimum wattage threshold
# Consider frequence breakdown
# GHI vs POA?

# Curious:
# What's the angular precision of the best CCD?

# Resources:
# Topeka irradiance
# https://kcc.ks.gov/images/PDFs/charts/Solar_KansasSolarRadiationMap.pdf
# https://www.e-education.psu.edu/eme810/sites/www.e-education.psu.edu.eme810/files/images/Lesson_04/Aniso_Components_rev.png
# https://www.suncalc.org/#/38.9325,-95.6784,8/2020.07.13/18:00/1/3

# monocrystalline silicon
# 22.4% efficient for testing, 23.7% on the car
# meter voltage and current
# 

def projected_area(area, theta):
    # https://en.wikipedia.org/wiki/Projected_area
    return area * np.cos(theta)
# print( [projected_area(100, th) for th in np.arange(37)*10 * np.pi/180 ] )

def angular_separation(alt1, az1, alt2, az2):
    # https://en.wikipedia.org/wiki/Angular_distance
    # Maybe verify with ephem.separation(m1, m2)?
    # https://rhodesmill.org/pyephem/quick.html
    return np.arccos( np.sin(alt1)*np.sin(alt2)
        + np.cos(alt1)*np.cos(alt2)*np.cos(az1 - az2) )

def test_angular_separation():
    assert angular_separation(0,0,0,np.pi) == np.pi
    assert angular_separation(0,0,np.pi,0) == np.pi
    assert angular_separation(0,np.pi,0,0) == np.pi
    assert angular_separation(np.pi,0,0,0) == np.pi
    assert angular_separation(np.pi,0,0,np.pi) == 0
    print("passes dummy tests")
# test_angular_separation()

def get_pos_pvlib_radians(lat, lon, date):
    # https://pvlib-python.readthedocs.io/en/stable/_modules/pvlib/solarposition.html
    pv = pvlib.solarposition.get_solarposition(date, lat, lon)
    return (np.deg2rad(pv["apparent_elevation"][0]), np.deg2rad(pv["azimuth"][0]))

def get_spos():
    lat, lon, tz = 29.6483, -82.3494, -5 #UF
    lat, lon, tz = 38.9325, -95.6784, -6 #Heartland motorsports park
                           # year, m,  d,  h,  m, s, micros,
    date = datetime.datetime(2020, 5, 27, 12, 13, 0, 130320, tzinfo=datetime.timezone.utc)
    hours = 24
    date -= datetime.timedelta(hours=tz) #-5GMT (march - Nov)
    s_a1 = get_pos_pvlib_radians(lat, lon, date)
    print(s_a1)
    for i in range(25):
        s_a2 = get_pos_pvlib_radians(lat, lon, date + datetime.timedelta(minutes=60*i))
        # print(s_a2)
        da = angular_separation(*s_a1, *s_a2)
        # print(np.rad2deg(da))
        area, power = 10, 100
        power *= projected_area(area, da)
        print(i, power, da, s_a2)
# get_spos()

def get_irradiance(date, alt, az):
    # https://pvlib-python.readthedocs.io/en/stable/auto_examples/plot_ghi_transposition.html#sphx-glr-auto-examples-plot-ghi-transposition-py
    # Creates one day's worth of 10 min intervals
    lat, lon, tz = 38.9325, -95.6784, -6 #Heartland motorsports park

    site = pvlib.location.Location(lat, lon, tz=tz, altitude=959 #above MSL (m)
                                , name="Heartland motorsports park")
    times = pd.date_range(date, freq='10min', periods=6*24, tz=tz)
    # Generate clearsky data using the Ineichen model, which is the default
    # The get_clearsky method returns a dataframe with values for GHI, DNI,
    # and DHI
    clearsky = site.get_clearsky(times)
    # Get solar azimuth and zenith to pass to the transposition function
    solar_position = site.get_solarposition(times=times)
    # Use the get_total_irradiance function to transpose the GHI to POA
    POA_irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=alt,
        surface_azimuth=az,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'])
    # Return DataFrame with only GHI and POA
    return pd.DataFrame({'GHI': clearsky['ghi'],
                         'POA': POA_irradiance['poa_global']})

def plot_example():
    date = datetime.datetime(2020, 6, 20, 12, 0, 0, 0, tzinfo=datetime.timezone.utc)
    alt, az = get_pos_pvlib_radians(38.9325, -95.6784, date + datetime.timedelta(hours=-6))
    alt, az = np.rad2deg(alt), np.rad2deg(az)

    # Get irradiance data for summer and winter solstice, assuming 25 degree tilt
    # and a south facing array
    summer_irradiance = get_irradiance('06-20-2020', alt, az)
    winter_irradiance = get_irradiance('12-21-2020', alt, az)

    # Convert Dataframe Indexes to Hour:Minute format to make plotting easier
    summer_irradiance.index = summer_irradiance.index.strftime("%H:%M")
    winter_irradiance.index = winter_irradiance.index.strftime("%H:%M")

    # Plot GHI vs. POA for winter and summer
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    summer_irradiance['GHI'].plot(ax=ax1, label='GHI')
    summer_irradiance['POA'].plot(ax=ax1, label='POA')
    winter_irradiance['GHI'].plot(ax=ax2, label='GHI')
    winter_irradiance['POA'].plot(ax=ax2, label='POA')
    ax1.set_xlabel('Time of day (Summer)')
    ax2.set_xlabel('Time of day (Winter)')
    ax1.set_ylabel('Irradiance ($W/m^2$)')
    ax1.legend()
    ax2.legend()
    plt.show()
plot_example()
