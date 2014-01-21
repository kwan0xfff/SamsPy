#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Deduce basic material properties of propellant combination.
"""

import sys

def deduce(ppltdata, mixture, mass):
    """Deduce basic material properties of propellant combination.
      ppltdata - propellant data source
      mixture - shortname of oxidizer-fuel combination
      mass - amount of propellant in kilograms
    Returns:
      pplt - propellant info
    """
    try:
        mixtures = ppltdata['mixtures']
        matlprops = ppltdata['matlprops']
    except KeyError as badkey:
        sys.stderr.write("missing propellant info %s\n" % str(badkey))
        raise

    pplt = {}                   # propellent info
    prop_indices = [ 0 ]        # start as mono-propellant
    try:
        mixinfo = mixtures[mixture]
    except KeyError as mix:
        sys.stderr.write("cannot find propellant mixture %s\n" % str(mix))
        raise
    for ispx in ( 'isp', 'isp-sl', 'isp-vac' ):
        if ispx in mixinfo:
            pplt[ispx] = mixinfo[ispx]
    if 'components' in mixinfo:
        assert len(mixinfo['components']) == 2, \
            "bi-propellants expected as components"
        prop_indices = [ 0, 1]
        ofratio = mixinfo['OFR']        # oxidizer/fuel ratio
        fr_oxid = ofratio / (ofratio + 1)       # fraction oxidizer
        pplt['matlNames'] = mixinfo['components']
    else:    # monopropellant code might go here
        pplt['fractions'] = [ 1.0 ]

    materials = [ matlprops[pplt['matlNames'][n]] for n in prop_indices ]
    pplt['fractions'] = ( fr_oxid, 1.0 - fr_oxid )
    pplt['masses'] = [ pplt['fractions'][n]*mass for n in prop_indices ]
    pplt['liqdens'] = [ materials[n]['liqdens'] for n in prop_indices ]
    pplt['volumes'] = [pplt['masses'][n]/pplt['liqdens'][n]
        for n in prop_indices ]

    return pplt


if __name__ == '__main__':
    import yaml

    fh = open(sys.argv[1], 'r')
    data = yaml.load(fh)
    print ("propellant analysis using", sys.argv[1])
    results = deduce(data, 'lox-lh2', 100)
    print (results)

# vim: set sw=4 tw=80 :
