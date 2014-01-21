#!/usr/bin/env python
#-*- coding: utf-8 -*-

import samspy.vehicle as veh
import samspy.vehicle.propel as propel

propellantdata = {
    'mixtures': {
        'lox-lch4': {
            'components': ['LOX', 'LCH4'],
            'name': 'LOX/methane',
        },
        'lox-lh2': {
            'components': ['LOX', 'LH2'],
            'isp': 450.0,
            'name': 'LOX/hydrogen',
            'OFR': 8.0,
        },
    },
    'matlprops': {
        'LOX': {'boilpt': 90.19, 'liqdens': 1.141},
        'LH2': {'boilpt': 20, 'liqdens': 0.068},
        'LCH4': {'boilpt': 112, 'liqdens': 0.422},
    },
}

pplt = veh.propel.deduce(propellantdata, 'lox-lh2', 100)

def testPropName():
    "Propellant names."

    assert pplt['matlNames'][0] == 'LOX'
    assert pplt['matlNames'][1] == 'LH2'

def testPropVolsDens():
    "Propellant volumes and densities."

    #pplt = veh.propel.deduce(propellantdata, 'lox-lh2', 100)
    assert abs(pplt['volumes'][0] - 77.9) < 0.1
    assert abs(pplt['volumes'][1] - 163.4) < 0.1
    assert abs(pplt['liqdens'][0] - 1.141) < 0.001
    assert abs(pplt['liqdens'][1] - 0.068) < 0.001

# vim: set sw=4 tw=80 :
