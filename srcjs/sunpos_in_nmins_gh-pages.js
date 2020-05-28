var SunCalc = require('suncalc2');

get_pos = (mins, coords) => {
  var lat = coords.latitude
  var lon = coords.longitude
  var pos = SunCalc.getPosition((new Date(Date.now()+(mins*60*1000))), lat, lon);
  var az = 180+pos["azimuth"]*180/Math.PI
  var alt = pos["altitude"]*180/Math.PI
  // console.log(az, alt)
  return [az, alt]
}
