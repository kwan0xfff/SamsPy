#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Launch vehicle -- basic analysis.
"""

from getopt import getopt, GetoptError
import sys
import yaml

from samspy.vehicle import multistage, propel
from samspy import lb2kg, m2ft, gEarth, N2lb

def printrow(label, fmt, datalist):
    """Print a report row with label, format, datalist.
    All labels have a common width.
    """
    line = "    %-24s" % label
    for item in datalist:
        line = line + ' ' + fmt % item
    sys.stdout.write( line + '\n')

def parseargs(argv):
    "Parse command line arguments."

    parsed = {}
    try:
        (opts, args) = getopt(argv[1:], "p:h",
            [ 'propellants', 'help' ])
    except GetoptError as ex:
        sys.stderr.write("error: %s\n" % str(ex))
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-p' or opt == '--propellants':
            parsed['propellants'] = arg
        if opt == '-h' or opt == '--help':
            parsed['help'] = True

    if len(args) != 1:
        raise ValueError("Vehicle description YAML required")
    parsed['vehicle'] = args[0]
    return parsed


def main(argv):
    """Determine basic vehicle propellant and mass parameters of vehicle."""

    parsed = parseargs(argv)

    fh = open(parsed['vehicle'], 'r')
    design = yaml.load(fh)
    fh = open(parsed['propellants'], 'r')
    propeldb = yaml.load(fh)

    staging = multistage.performance(design)
    sequence = design['stageorder']
    maxG = design['maxG']

    for activestage in sequence:
        stageinfo = staging[activestage]
        print ('%-32s Mignite %7.1f Mburnout %7.1f kilo' % (activestage,
            stageinfo['Mignite'], stageinfo['Mburnout'] ))
        print ('%-32s Mignite %7.1f Mburnout %7.1f lbm' % (activestage,
            stageinfo['Mignite']/lb2kg, stageinfo['Mburnout']/lb2kg ))
        print ('%-32s  deltaV %7.1f' % (activestage, stageinfo['deltaV']))

    deltaV = staging['totalDeltaV']
    printrow ('Total deltaV (m/s, ft/s)', '%11.4f', [deltaV, deltaV*m2ft])

    stages = design['stages']
    for activestage in sequence:
        stageinfo = staging[activestage]
        if 'Isp' not in stages[activestage] or stages[activestage]['Isp'] == 0:
            continue
        mixture = stages[activestage]['mixture']
        Mpropel = stageinfo['Mignite']-stageinfo['Mburnout']
        propresults = propel.deduce(propeldb, mixture, Mpropel)

        print ('Stage:', activestage)
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
            printrow (label, fmt, results)
        avgdens = sum(propresults['masses'])/sum(propresults['volumes'])
        printrow ('avg dens (kg/l)', '%11.4f', [avgdens])

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

        printrow ('massflow (kg/s)', '%11.4f', [mflow])
        printrow ('burn time (s)', '%11.4f', [burntime])
        printrow ('G (ignite, burnout)', '%7.3f', [GIgnite, GBurnout])
        printrow ('thrust (N, lbf)', '%11.4f', [thrust, thrust*N2lb])
        printrow ('wt ignite (N, lbm)', '%11.4f', [wIgnite, wIgnite*N2lb])
        printrow ('wt burnout (N, lbm)', '%11.4f', [wBurnout, wBurnout*N2lb])
        printrow ('deltaV (m/s, ft/s)', '%11.4f', [deltaV, deltaV*m2ft])
        printrow ('wet mass', '%11.4f', [wetmass, wetmass/lb2kg])
        printrow ('dry mass', '%11.4f', [drymass, drymass/lb2kg])

    print ('Totals:')
    drytot = multistage.masses(design['stageorder'], stages, mtype='Mdry')
    printrow ('dry mass', '%11.4f', [drytot, drytot/lb2kg])


sys.exit(main(sys.argv))

# vim: set sw=4 tw=80 :
