#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Describe a super-synchronous maneuver to geostationary orbit.
Go from low Earth orbit (LEO) to intermediate transfer orbit (ITO)
to super-synchronous transfer orbit (STO) to geostationary orbit (GEO).
LEO is inclined to equator.

Suffixes on variables and notations:
  _sl = above sea level
  _r = radius to Earth center
  _apo = apoapsis, apogee
  _per = periapsis, perigee
"""

import math
import sys

from samspy import deg2rad, s2hms
import samspy.traj.orbit as orbit

# Earth constants
muEarth = 398600.4418  # km^3 s^-2 ; mu = GM (grav const * mass)
earth_r = 6378.1  # equatorial, polar is 6371.0
geo_r = 42164.0
geo_sl = geo_r - earth_r        # GEO above sea level


def leo_ito_sto_geo (leo_sl, sto_sl, leo_incline):
    """Characterize the sequence of orbits (LEO, ITO, STO, GEO) by
    velocities and transition delta Vs.  Include plane change due to
    initial LEO inclination.
    """

    leo_r = earth_r + leo_sl
    sto_apo_r = earth_r + sto_sl
    incline_rad = leo_incline * deg2rad

    velo = {}
    deltav = {}
    orbits = {}

    leo = orbit.Elliptical(mu=muEarth).set_circular(leo_r)
    leo.fill_params()

    ito = orbit.Elliptical(mu=muEarth, peri=leo_r, apo=sto_apo_r)
    ito.fill_params()

    sto = orbit.Elliptical(mu=muEarth, peri=geo_r, apo=sto_apo_r)
    sto.fill_params()

    geo = orbit.Elliptical(mu=muEarth).set_circular(geo_r)
    geo.fill_params()

    velo['leo'] = leo.velo(leo_r)
    velo['ito_per'] = ito.velo(leo_r)
    velo['ito_apo'] = ito.velo(sto_apo_r)
    velo['sto_apo'] = sto.velo(sto_apo_r)
    velo['sto_per'] = sto.velo(leo_r)
    velo['geo'] = geo.velo(geo_r)

    deltav['leo_ito'] = math.fabs(velo['ito_per'] - velo['leo'])
    deltav['ito_sto'] = ito.planechange(sto, incline_rad)
    deltav['sto_geo'] = math.fabs(velo['geo'] - velo['sto_per'])

    orbits['leo'] = leo
    orbits['ito'] = ito
    orbits['sto'] = sto
    orbits['geo'] = geo

    return velo, deltav, orbits

def print_shape(orbitname, orbit):
    "Print formatted shape parameters of eccentric orbit."
    msgfmt ="%s smj %5d km ecc %5.3f " + \
        "[rxp r(asl)] %5d x %5d km (%3d x %3d km)"
    print(msgfmt % (orbitname, orbit.semimaj, orbit.eccentricity,
        orbit.apoapsis, orbit.periapsis,
        orbit.apoapsis - earth_r, orbit.periapsis - earth_r))

def print_period(orbitname, orbit_obj):
    "Print orbital period -- seconds and hh, mm, ss"
    msgfmt = "%s period %6d sec = %3dh %2dm %3.1fs"
    hh, mm, ss = s2hms(orbit_obj.period)
    print(msgfmt % (orbitname, orbit_obj.period, hh, mm, ss))

def print_velo(orbitname, altitude, speed):
    "Print orbital velocity at noted altitude."
    msgfmt = "%s velo at %6d km = %8.5f km/sec"
    print(msgfmt % (orbitname, altitude, speed))

def print_deltav(eventname, altitude, deltav):
    "Print deltaV of event at noted altitude."
    msgfmt = "%s dv at %6d km = %8.5f km/sec"
    print(msgfmt % (eventname, altitude, deltav))

def report(velo, dv, orbits):
    "Generate report of maneuver parameters."

    leo = orbits['leo']
    ito = orbits['ito']
    sto = orbits['sto']
    geo = orbits['geo']

    print_period("LEO", leo)
    print_period("ITO", ito)
    print_period("STO", sto)
    print_period("GEO", geo)

    print_shape("LEO", leo)
    print_shape("ITO", ito)
    print_shape("STO", sto)
    print_shape("GEO", geo)

    print_velo("LEO", leo.periapsis, velo['leo'])
    print_velo("ITO", ito.periapsis, velo['ito_per'])
    print_velo("ITO", ito.apoapsis , velo['ito_apo'])
    print_velo("STO", sto.apoapsis , velo['sto_apo'])
    print_velo("STO", sto.periapsis, velo['sto_per'])
    print_velo("GEO", geo.periapsis, velo['geo'])

    print_deltav("LEO->ITO", ito.periapsis, dv['leo_ito'])
    print_deltav("ITO->STO", ito.apoapsis, dv['ito_sto'])
    print_deltav("STO->GEO", geo.semimaj, dv['sto_geo'])

def main(argv):
    """Compute super-synchronous maneuver.
    Arguments:
       argv[1] -- LEO atitude above sea level
       argv[2] -- STO atitude above sea level
       argv[3] -- inclination in degrees
    Example argments: 295.0 90000.0 22.5
    """

    leo_sl = float(argv[1])
    sto_sl = float(argv[2])
    inclination = float(argv[3])

    velo, dv, orbits = leo_ito_sto_geo(leo_sl, sto_sl, inclination)
    report(velo, dv, orbits)

main(sys.argv)

# vim: set sw=4 tw=80 :
