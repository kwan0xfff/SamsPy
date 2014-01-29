#!/usr/bin/env python
#-*- coding: utf-8 -*-

import samspy.traj.orbit as orbit
from samspy import deg2rad

muEarth = 398600.4418  # km^3 s^-2 ; mu = GM (grav const * mass)
earth_r = 6378.1  # equatorial, polar is 6371.0
geo_r = 42164.0
geo_sl = geo_r - earth_r        # GEO above sea level
leo_sl = 295.0
leo_r = earth_r + leo_sl
sto_sl = 90000.0
sto_apo_r = earth_r + sto_sl
leo_incline = 22.5
incline_rad = leo_incline * deg2rad

def eps5(want, got):
    """Check the difference between a 'want' value and a 'got' value
    is has a relative precision of less than 1.0e-5.
    """
    scaled = (want - got) / want
    assert scaled < 1.0e-5, "tolerance < eps5"


leo = orbit.Elliptical(mu=muEarth).set_circular(leo_r)
leo.fill_params()

sto = orbit.Elliptical(mu=muEarth, peri=leo_r, apo=sto_apo_r)
sto.fill_params()

ito = orbit.Elliptical(mu=muEarth, peri=geo_r, apo=sto_apo_r)
ito.fill_params()

geo = orbit.Elliptical(mu=muEarth).set_circular(geo_r)
geo.fill_params()

def testOrbitConstCheck():
    eps5(muEarth, 398600.4418)
    eps5(earth_r, 6378.1)

def testOrbitLEO():
    "Test circular orbit."
    eps5(leo.apoapsis, leo_r)
    eps5(leo.apoapsis, leo.periapsis)
    eps5(leo.period, 5425.03357)
    eps5(leo.apoapsis, leo.semimaj)

def testOrbitSTO():
    "Test highly elliptical orbit."
    eps5(sto.apoapsis, sto_apo_r)
    eps5(sto.period, 116398.013)

def testOrbitPlaneChange():
    "Test orbit plane change."
    dv = ito.planechange(sto, incline_rad)
    eps5(dv, 0.95257)

