#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# multistage.py -- multi-stage analysis

import sys
import math
from samspy import gEarth

def rocketeq(ve, m0, m1):
    '''Compute delta V based on ve (effective exhaust velocity),
    and initial and final mass (m0 and m1 respectively).
    Original derivation:  Tsiolkovsky
    '''
    deltav = ve * math.log(m0/m1)
    return deltav

def masses(stagelist, stages, mtype='Mwet'):
    '''Sum up the stage masses of 'mtype'. '''
    mlist = [ stages[s][mtype] for s in stagelist ]
    return sum(mlist)

def stagedeltaV(stagelist, stages, infolvl=0):
    '''Compute ignition and burnout masses and resulting deltaV.'''
    activestage = stagelist[0]
    upperstages = stagelist[1:]
    Mpropel = stages[activestage]['Mwet'] - stages[activestage]['Mdry']
    Isp = stages[activestage]['Isp']

    Mignite = masses(stagelist, stages)
    Mburnout = Mignite - Mpropel
    deltaV = rocketeq(Isp*gEarth, Mignite, Mburnout)
    results = { 'Mignite' : Mignite, 'Mburnout' : Mburnout,
            'Isp': Isp, 'deltaV': deltaV }
    return results

def performance(design):
    '''Analyze performacne in terms of delta V.
    '''
    stageorder = design['stageorder']
    stages = design['stages']
    mass = masses(stageorder, stages)
    deltaVlist = []
    perfinfo = {}
    stageinfo = {}

    stagelast = len(stageorder)
    for nx in range(len(stageorder)):
        stagenum = nx + 1
        stagelist = stageorder[nx:stagelast]
        stageinfo = stagedeltaV(stagelist, stages, infolvl=2)
        deltaV = stageinfo['deltaV']
        deltaVlist.append(deltaV)
        perfinfo[stageorder[nx]] = stageinfo

    perfinfo['totalDeltaV'] = sum(deltaVlist)
    return perfinfo

if __name__ == '__main__':
    import yaml

    fh = open(sys.argv[1], 'r')
    design = yaml.load(fh)
    results = performance(design)
    sequence = design['stageorder']

    for activestage in sequence:
        stageinfo = results[activestage]
        print ('%-32s Mignite %7.1f Mburnout %7.1f' % (activestage, 
            stageinfo['Mignite'], stageinfo['Mburnout'] ))
        print ('%-32s  deltaV %7.1f' % (activestage, stageinfo['deltaV']))

    print ('Total deltaV', "%7.1f"%results['totalDeltaV'])

# vim: set sw=4 tw=80 :
