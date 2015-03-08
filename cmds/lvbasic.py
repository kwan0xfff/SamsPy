#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Launch vehicle -- basic analysis.
"""

import argparse
import sys
import yaml

from samspy.vehicle import multistage, propel
from samspy import lb2kg, m2ft, gEarth, N2lb
from samspy.writers.Text import Text

def parseargs(argv):
    "Parse command line arguments."

    parser = argparse.ArgumentParser()
    parser.add_argument("vehicle", help="vehicle spec file")
    parser.add_argument("propellants", help="propellants data file")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
            action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("verbosity turned on")
    return args

def main(argv):
    """Determine basic vehicle propellant and mass parameters of vehicle."""

    parsed = parseargs(argv)

    writer = Text(sys.stdout)
    putrow = writer.putfmtrow
    putitem = writer.putitem
    putrow("msglabel", "%8s", [ "hello", "world" ])

    fh = open(parsed.vehicle, 'r')
    design = yaml.load(fh)
    fh = open(parsed.propellants, 'r')
    propeldb = yaml.load(fh)

    staging = multistage.performance(design)
    sequence = design['stageorder']
    maxG = design['maxG']

    for activestage in sequence:
        stageinfo = staging[activestage]
        putitem ('%-32s Mignite %7.1f Mburnout %7.1f kilo' % (activestage,
            stageinfo['Mignite'], stageinfo['Mburnout'] ))
        putitem ('%-32s Mignite %7.1f Mburnout %7.1f lbm' % (activestage,
            stageinfo['Mignite']/lb2kg, stageinfo['Mburnout']/lb2kg ))
        putitem ('%-32s  deltaV %7.1f' % (activestage, stageinfo['deltaV']))

    deltaV = staging['totalDeltaV']
    putrow ('Total deltaV (m/s, ft/s)', '%11.4f', [deltaV, deltaV*m2ft])

    stages = design['stages']
    for activestage in sequence:
        stageinfo = staging[activestage]
        if 'Isp' not in stages[activestage] or stages[activestage]['Isp'] == 0:
            continue
        mixture = stages[activestage]['mixture']
        Mpropel = stageinfo['Mignite']-stageinfo['Mburnout']
        propresults = propel.deduce(propeldb, mixture, Mpropel)

        putitem ('Stage: ' + activestage)
        for label, fmt, prop in (
                ('matl names', '%7s', 'matlNames'),
                ('liqdens (kg/l)', '%7.3f', 'liqdens'),
                ('masses (kg)', '%7.3f', 'masses'),
                ('volume (l)', '%7.3f', 'volumes') ):
            results = list(propresults[prop])
            if prop == 'matlNames':
                results.append('[sum]')
            elif prop in ('masses', 'volumes'):
                results.append(sum(propresults[prop]))
            putrow (label, fmt, results)
        avgdens = sum(propresults['masses'])/sum(propresults['volumes'])
        putrow ('avg dens (kg/l)', '%11.4f', [avgdens])

        # compute thrust based on stageinfo['Mburnout']
        thrust = stageinfo['Mburnout'] * gEarth * maxG
        wIgnite = stageinfo['Mignite'] * gEarth
        wBurnout = stageinfo['Mburnout'] * gEarth
        deltaV = stageinfo['deltaV']
        mflow = thrust / (stageinfo['Isp'] * gEarth)
        wetmass = stageinfo['Mignite']
        drymass = stageinfo['Mburnout']
        burntime = Mpropel / mflow
        GIgnite = thrust / wIgnite
        GBurnout = thrust / wBurnout

        for label, fmt, values in (
            ('massflow (kg/s)', '%11.4f', [mflow]),
            ('burn time (s)', '%11.4f', [burntime]),
            ('G (ignite, burnout)', '%7.3f', [GIgnite, GBurnout]),
            ('thrust (N, lbf)', '%11.4f', [thrust, thrust*N2lb]),
            ('wt ignite (N, lbm)', '%11.4f', [wIgnite, wIgnite*N2lb]),
            ('wt burnout (N, lbm)', '%11.4f', [wBurnout, wBurnout*N2lb]),
            ('deltaV (m/s, ft/s)', '%11.4f', [deltaV, deltaV*m2ft]),
            ('wet mass', '%11.4f', [wetmass, wetmass/lb2kg]),
            ('dry mass', '%11.4f', [drymass, drymass/lb2kg]), ):
            putrow (label, fmt, values)

    putitem ('Totals:')
    drytot = multistage.masses(design['stageorder'], stages, mtype='Mdry')
    putrow ('dry mass', '%11.4f', [drytot, drytot/lb2kg])


sys.exit(main(sys.argv))

# vim: set sw=4 tw=80 :
