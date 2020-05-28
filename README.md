# About

The goal is to determine the optimal angle to set the solar array for the UF solar car.  The car will be parked to set the azimuth angle and then the array will be tilted with a hinge to control the altitude angle.

## Usage

  * Inputs: Latitude, Longitude, Altitude, times
  * Output: Optimal angle for time window that maximizes energy capture

## Extras

  * Consider [solar irradiance](https://en.wikipedia.org/wiki/Solar_irradiance) (diffuse, etc)
  * Consider minimum wattage threshold
  * Consider light frequency breakdown
  * GHI vs POA?
  * Consider unlevel ground (screws with angles)
  * Does the type of solar cell make a difference?  Currently using monocrystalline silicon ~23%.

## Resources:
  * [Topeka irradiance](https://kcc.ks.gov/images/PDFs/charts/Solar_KansasSolarRadiationMap.pdf)
  * [Topeka Suncalc](https://www.suncalc.org/#/38.9325,-95.6784,8/2020.07.13/18:00/1/3)
