#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
lvpropest - Launch vehicle propulsion estimator
"""

import argparse
import sys
import yaml

from samspy.vehicle import multistage, propel
from samspy import lb2kg, m2ft
from samspy.writers.Text import Text
from samspy.writers.ReportsLV1 import BasicLV

#import pdb

DESC = """Launch Vehicle Propulsion Estimator.
Basic performance and propulsion analysis for a multi-stage rocket.
"""

def parseargs(argv):
    "Parse command line arguments."

    parser = argparse.ArgumentParser(description=DESC)
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

    #writer = HTML(sys.stdout)
    writer = Text(sys.stdout)
    putrow = writer.putfmtrow
    putitem = writer.putitem

    basicrept = BasicLV(writer)

    fh = open(parsed.vehicle, 'r')
    design = yaml.load(fh)
    fh = open(parsed.propellants, 'r')
    propeldb = yaml.load(fh)

    if parsed.verbose:
        import pprint
        pp = pprint.PrettyPrinter(width=41, stream=sys.stderr)
        pp.pprint(["design", design])

    performance = multistage.performance(design)

    sequence = design['stageorder']

    deltaVlist = []

    putitem('Mass and deltaV:')
    for activestage in sequence:
        putitem('Stage: ' + activestage)
        stageperf = performance[activestage]
        basicrept.putStageMassesDeltaV(activestage, stageperf)
        deltaVlist.append(stageperf['deltaV'])

    totalDeltaV = sum(deltaVlist)
    putitem('Total deltaV:')
    putrow('Total deltaV (m/s, ft/s)', '%11.4f', [totalDeltaV, totalDeltaV*m2ft])

    reptfmts = {}
    reptfmts['propel.deduce'] = propel.reptfmt_deduce

    stages = design['stages']
    for activestage in sequence:
        stageperf = performance[activestage]
        if 'Isp' not in stages[activestage] or stages[activestage]['Isp'] == 0:
            continue
        mixture = stages[activestage]['mixture']
        Mpropel = stageperf['Mignite']-stageperf['Mburnout']
        propellants = propel.deduce(propeldb, mixture, Mpropel)
        stageperf['gRange'] = design['gRange']
        flows, reptflows = propel.flows(propellants, stageperf)
        reptfmts['propel.flows'] = reptflows
        basicrept.putPropellants(activestage, stageperf, propellants, reptfmts)

    putitem('Totals:')
    drytot = multistage.masses(design['stageorder'], stages, mtype='Mdry')
    putrow('dry mass', '%11.4f', [drytot, drytot/lb2kg])


sys.exit(main(sys.argv))

# vim: set sw=4 tw=80 :
