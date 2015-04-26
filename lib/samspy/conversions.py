#!/usr/bin/env python
#-*- coding: utf-8 -*-

"Conversion multiplication factors"

import math


# unit conversions
m2ft = 3.2808399        # meters to feet
lb2kg = 0.45359237      # pounds-mass to kilogams
gEarth = 9.80665        # 1 G, grav accel at sea level (1 G), m/s^2

# force
N2lb = 0.224808943      # Newtons to pounds

# volumes
l2gal = 0.264172        # liters to US gallons
l2ft3 = 0.0353147       # liters to cubic feet
l2m3 = 0.001            # liters to cubic meters

# power
W2BTUph = 3.41214163    # watts to BTU/hr
kW2hp = 1.34102209      # kilowatts to horsepower

# math conversion constants
deg2rad = math.pi / 180.0


# time conversion
def s2hms (sec):
    "Convert seconds to hours, minutes, seconds."
    t = sec
    h = t // 3600.0
    t -= h * 3600.0
    m = t // 60.0
    t -= m * 60.0
    s = t 
    return (h, m, s)

# vim: set sw=4 tw=80 :
