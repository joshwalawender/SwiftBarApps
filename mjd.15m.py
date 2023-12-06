#!/Users/joshw/anaconda3/envs/py39/bin/python
#
# <xbar.title>MJD</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Josh Walawender</xbar.author>
# <xbar.author.github>joshwalawender</xbar.author.github>
# <xbar.desc>Show the current Modified Julian Date</xbar.desc>
#
from astropy.time import Time
from astroplan import moon_illumination, Observer
from astropy import units as u
from astropy import coordinates
now = Time.now()
loc = coordinates.EarthLocation(coordinates.Longitude(-155.71513333*u.deg),
                                coordinates.Latitude(20.02868056*u.deg),
                                677*u.meter
                                )
observer = Observer(location=loc, name="Ohina")

# lst = observer.local_sidereal_time(now)
# lst_str = f"{lst.hms.h:.0f}:{lst.hms.m:02.0f}"

moon = coordinates.get_moon(now, loc)
moon_alt = observer.altaz(now, moon).alt

sun = coordinates.get_sun(now)
sun_alt = observer.altaz(now, sun).alt


print(f"MJD {now.mjd:.2f}")
print('---')
if moon_alt < 0:
#     moonrise = observer.target_rise_time(now, moon)
#     moon = coordinates.get_moon(moonrise, loc)
#     moon_alt = observer.altaz(now, moon).alt
    print(f"A {moon_illumination(now):.0%} Moon is Down")
#     print(f"Moonrise at {moonrise.datetime.strftime('%H:%M:%S')} UT ({moon_alt:.1f})")
else:
#     moonset = observer.target_set_time(now, moon).datetime
    print(f"A {moon_illumination(now):.0%} Moon is Up")
#     print(f"Moonset at {moonset.strftime('%H:%M:%S')} UT")

if sun_alt < 0:
    sunrise = observer.target_rise_time(now, sun).datetime
    print(f'Sun is Down')
    print(f"Sunrise at {sunrise.strftime('%H:%M:%S')} UT")
else:
    sunset = observer.target_set_time(now, sun)
    print(f'Sun is Up (alt={sun_alt:.0f})')
    print(f"Sunset at {sunset.strftime('%H:%M:%S')} UT")
