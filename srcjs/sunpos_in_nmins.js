// Warnings
// Azimuth correction (+180) probably needs to be fixed
//     someone, please check this
// navigator.geolocation needs HTTPS:
//     https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
// SunCalc2 doesn't use altitude as part of their calculation
var SunCalc = require('suncalc2');

var lat = 29.6483,
    lon = -82.3494,
    alt = 32,
    tz  = -4,
    mins = 0
    // lat, lon, alt, tz = 29.6483, -82.3494, 32, -4 #UF
var pos = SunCalc.getPosition((new Date(Date.now()+(mins*60*1000))), lat, lon);
var az = 180+pos["azimuth"]*180/Math.PI
var alt = pos["altitude"]*180/Math.PI

// needs https
// var coords
// navigator.geolocation.getCurrentPosition(p => {
//   console.log(p)
//   coords = p.coords
// })

// Try this in the browser console
// navigator.geolocation.getCurrentPosition(p => {console.log(p.coords)})
