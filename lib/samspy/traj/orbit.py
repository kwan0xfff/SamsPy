#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Some basic orbit computation.
"""

import math

class Elliptical:
    """Elliptical orbit.
    """

    def __init__(self, apo=None, peri=None, ecc=None, mu=None):
        """Elliptical constructor.
        Measures apoasis and periapsis are radii from center
        (not sea level).
        """
        self.apoapsis = apo
        self.periapsis = peri
        self.eccentricity = ecc
        self.mu = mu

        # computed parameters
        self.period = None      # orbital period
        self.semimaj = None     # semimajor axis

    def set_circular(self, radius):
        """Set parameters to circular orbit with given radius.
        Return the orbit, allowing it to chain onto __init__().
        """
        self.apoapsis = radius
        self.periapsis = radius
        self.eccentricity = 0.0
        return self

    def fill_params(self):
        """Fill in missing parameters to extent possible.
        """
        if self.semimaj is None:
            if self.apoapsis > 0 and self.periapsis > 0:
                self.derive_semimaj()
        if self.period is None:
            if self.semimaj > 0 and self.mu > 0:
                self.derive_period()
        if self.eccentricity is None:
            if self.apoapsis > 0 and self.periapsis > 0:
                self.derive_eccentricity()

    def derive_semimaj(self):
        """Fill in semimajor axis from apoapsis and periapsis."""
        self.semimaj = (self.apoapsis + self.periapsis) / 2.0

    def derive_period(self):
        """Fill in orbital period from semimajor axis and mu"""
        smj = self.semimaj
        self.period = 2.0 * math.pi * math.sqrt(smj*smj*smj/self.mu)

    def derive_eccentricity(self):
        """Fill in eccentricity axis from apoapsis and periapsis."""
        rp = self.periapsis
        ra = self.apoapsis
        self.eccentricity = (ra - rp) / (ra + rp)

    def velo(self, dist):
        "Velocity (speed) at given distance along orbit trajectory."
        velo = math.sqrt(self.mu * (2.0/dist - 1.0/self.semimaj))
        return velo

    def planechange(self, neworbit, angle):
        """Compute deltaV based on plane change into new orbit at apogee.
        Plane change is given by angle in radians.
        """
        # Utilize law of cosines for sides a, b, c, angleC
        # c*c = a*a + b*b + 2*a*b*cos(angleC)

        self_apo = self.apoapsis
        new_apo = neworbit.apoapsis
        if math.fabs(self_apo - new_apo)/new_apo > 0.0001:
            raise ValueError("apogees do not agree")

        self_v = self.velo(self_apo)
        new_v = neworbit.velo(new_apo)
        c2 = self_v * self_v + new_v * new_v - \
            2.0 * self_v * new_v * math.cos(angle)
        return math.sqrt(c2)


# vim: set sw=4 tw=80 :
