#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Basic launch vehicle report (LV1).
"""

from samspy import lb2kg, m2ft, gEarth, N2lb

class BasicLV:
    """ Basic launch vehicle report.
    """

    def __init__(self, writer):
        """Text output formatters.
        'writer' is a formatter with an opened output stream.
        """
        self.writer = writer

    def putStageMassesDeltaV(self, name, stageperf):
        """Write stage masses and deltaV to output stream.
        name : stage name
        stageperf : dict including 'Mignite', 'Mburnout' in kg.
        """
        putitem = self.writer.putitem
        putrow = self.writer.putfmtrow
        # stagename phase (kg, lbm)   %7.1f %7.1f
        for label, prop in (
            ('Mignite (kg, lbm)', stageperf['Mignite']),
            ('Mburnout (kg, lbm)', stageperf['Mburnout']), ):
            putrow (label, '%11.4f', [ prop, prop/lb2kg ])
        for label, prop in (
            ('deltaV (m/s, ft/s)', stageperf['deltaV']),):
            putrow (label, '%11.4f', [ prop, prop*m2ft ])

    def putPropellants(self, name, stageperf, propellants, reptfmts):
        """Write propellant information.
        Assumes constant thrust computed from max G.
        """
        putitem = self.writer.putitem
        putrow = self.writer.putfmtrow

        putitem ('Stage: ' + name)
        reptfmt = reptfmts['propel.deduce']
        for label, fmt, prop in reptfmt:
            results = list(propellants[prop])
            if prop == 'matlNames':
                results.append('[sum]')
            elif prop in ('masses', 'volumes'):
                results.append(sum(propellants[prop]))
            putrow (label, fmt, results)
        avgdens = sum(propellants['masses'])/sum(propellants['volumes'])
        putrow ('avg dens (kg/l)', '%11.4f', [avgdens])

        reptfmt = reptfmts['propel.flows']
        for label, fmt, prop in reptfmt:
            putrow (label, fmt, prop)


#set sw=4 tw=80 :
