#!/usr/bin/env python3
#
# <xbar.title>LST</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Josh Walawender</xbar.author>
# <xbar.author.github>joshwalawender</xbar.author.github>
# <xbar.desc>Show the current Modified Julian Date and Local Sidereal Time</xbar.desc>
#
from astropy.time import Time
from astropy import units as u
from astropy import coordinates
import numpy as np
now = Time.now()
loc = coordinates.EarthLocation(coordinates.Longitude(-155.71513333*u.deg),
                                coordinates.Latitude(20.02868056*u.deg),
                                677*u.meter
                                )
now.location = loc
altazframe = coordinates.AltAz(location=loc, obstime=now, pressure=0)

lst = now.sidereal_time('mean')
lst_hour = int(np.floor(lst.hour))
lst_min = (lst.hour - lst_hour)*60
lst_str = f"{lst_hour:02d}:{lst_min:02.0f}"

moon = coordinates.get_moon(now, loc)
moon_alt = ((moon.transform_to(altazframe).alt).to(u.degree)).value

sun = coordinates.get_sun(now)
sun_alt = ((sun.transform_to(altazframe).alt).to(u.degree)).value

# Moon illumination formula from Meeus, “Astronomical 
# Algorithms". Formulae 46.1 and 46.2 in the 1991 edition, 
# using the approximation cos(psi) \approx -cos(i). Error 
# should be no more than 0.0014 (p. 316). 
moon_illum = 0.50*(1 - np.sin(sun.dec.radian)*np.sin(moon.dec.radian)\
             - np.cos(sun.dec.radian)*np.cos(moon.dec.radian)\
             * np.cos(sun.ra.radian-moon.ra.radian))

# print(f"MJD {now.mjd:.1f}, LST {lst_str}")
print(f"LST {lst_str}")
print('---')
if moon_alt < 0:
    print(f"A {moon_illum:.0%} Moon is Down")
else:
    print(f"A {moon_illum:.0%} Moon is Up")

if sun_alt < 0:
    print(f'Sun is Down')
else:
    print(f'Sun is Up (alt={sun_alt:.0f})')
