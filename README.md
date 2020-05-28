# About

The goal is to determine the optimal angle to set the solar array for the UF solar car.  The car will be parked to set the azimuth angle and then the array will be tilted with a hinge to control the altitude angle.

Check out Kelly's [angle calculations](AngleCalculations.pdf)

Check out an initial [web prototype](https://solar-gators.github.io/SolarArrayAngleCalculations/) using [suncalc2](https://www.npmjs.com/package/suncalc2).

## Ideal Usage
  * Inputs: Latitude, Longitude, Altitude, Times (Y:M:D h:m:s)
  * Output: Optimal angle for time window that maximizes energy capture

## Current Status
  * Onboarding in progress
  * srcpy/sun_angle_test.py Example sun position calculations
  * srcpy/pv_sim.py Example irradiance calculation from pvlib's gallery
  * Discussion of Matlab version(s)

## Extras
  * Consider [solar irradiance](https://en.wikipedia.org/wiki/Solar_irradiance) (diffuse, etc)
  * Consider minimum wattage threshold
  * Consider light frequency breakdown
  * GHI vs POA?
  * Consider unlevel ground (screws with angles)
  * Does the type of solar cell make a difference?  Currently using monocrystalline silicon ~23%.
  * Turn it into a phone/web app?

## Resources
  * [Topeka irradiance](https://kcc.ks.gov/images/PDFs/charts/Solar_KansasSolarRadiationMap.pdf)
  * [Topeka Suncalc](https://www.suncalc.org/#/38.9325,-95.6784,8/2020.07.13/18:00/1/3)
