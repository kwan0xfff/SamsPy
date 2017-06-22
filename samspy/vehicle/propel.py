#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Propusion information.
* Deduce basic material properties of propellant combination.
* Compute propellant flow characteristics.
"""

from samspy import lb2kg, m2ft, gEarth, N2lb

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

# report format using writer/formatter putfmtrow()
# label, numeric format, property
reptfmt_deduce =  (
    ('matl names', '%7s', 'matlNames'),
    ('liqdens (kg/l)', '%7.3f', 'liqdens'),
    ('masses (kg)', '%7.3f', 'masses'),
    ('volume (l)', '%7.3f', 'volumes') )

def flows(propellants, stageperf):
    """Determine flow properties given propellant properties and desired
    performance.
      propellants - propellant properties deduced from raw data via deduce()
      stageperf - performance numbers per page
    Returns:
      stageflows - computed flow properties
    """
    stageflows = {}     # result
    sf = stageflows
    reptfmt = []

    minG = stageperf['gRange'][0]
    maxG = stageperf['gRange'][1]

    thrust_fini = stageperf['Mburnout'] * gEarth * maxG
    thrust_init = stageperf['Mignite'] * gEarth * minG
    thrust = (thrust_init, thrust_fini)[ thrust_init < thrust_fini ]
    wIgnite = stageperf['Mignite'] * gEarth
    wBurnout = stageperf['Mburnout'] * gEarth
    Mpropel = stageperf['Mignite']-stageperf['Mburnout']
    deltaV = stageperf['deltaV']
    mflow = thrust / (stageperf['Isp'] * gEarth)
    mflow_min = thrust_fini / (stageperf['Isp'] * gEarth)
    mflows = [ mflow*frac for frac in propellants['fractions'] ]
    mflows_min = [ mflow_min*frac for frac in propellants['fractions'] ]
    mflows.append(mflow)
    mflows_min.append(mflow_min)
    mflows_lb = [ m/lb2kg for m in mflows ]
    vflows = [ mflows[n]/propellants['liqdens'][n] for n in range(2) ]
    vflows.append(vflows[0] + vflows[1])
    wetmass = stageperf['Mignite']
    drymass = stageperf['Mburnout']
    burntime_min = Mpropel / mflow
    burntime_max = Mpropel / mflow_min
    GIgnite = thrust_init / wIgnite
    GBurnout = thrust_fini / wBurnout

    sf['mflows'] = mflows
    sf['mflows_lb'] = mflows_lb
    sf['mflows_min'] = mflows_min
    sf['vflows'] = vflows
    sf['burntime_min'] = burntime_min
    sf['burntime_max'] = burntime_max
    sf['G-range'] = [GIgnite, GBurnout]
    sf['thrust_init'] = thrust_init
    sf['thrust_fini'] = thrust_fini
    sf['thrust'] = thrust
    sf['wIgnite'] = wIgnite
    sf['wBurnout'] = wBurnout
    sf['deltaV'] = deltaV
    sf['wetmass'] = wetmass
    sf['drymass'] = drymass

    report =  (
        ('massflow (kg/s)', '%7.3f', mflows),
        ('massflow (lbm/s)', '%7.3f', mflows_lb),
        ('massflow min (kg/s)', '%7.3f', mflows_min),
        ('volflow (l/s)', '%7.3f', vflows),
        ('burn time min (s)', '%11.4f', [burntime_min]),
        ('burn time max (s)', '%11.4f', [burntime_max]),
        ('G (ignite, burnout)', '%7.3f', [GIgnite, GBurnout]),
        ('thrust init (N, lbf)', '%11.4f', [thrust_init, thrust_init*N2lb]),
        ('thrust fini (N, lbf)', '%11.4f', [thrust_fini, thrust_fini*N2lb]),
        ('thrust (N, lbf)', '%11.4f', [thrust, thrust*N2lb]),
        ('wt ignite (N, lbm)', '%11.4f', [wIgnite, wIgnite*N2lb]),
        ('wt burnout (N, lbm)', '%11.4f', [wBurnout, wBurnout*N2lb]),
        ('deltaV (m/s, ft/s)', '%11.4f', [deltaV, deltaV*m2ft]),
        ('wet mass (kg, lbm)', '%11.4f', [wetmass, wetmass/lb2kg]),
        ('dry mass (kg, lbm)', '%11.4f', [drymass, drymass/lb2kg]),
    )

    return stageflows, report

if __name__ == '__main__':
    import yaml

    fh = open(sys.argv[1], 'r')
    data = yaml.load(fh)
    print ("propellant analysis using", sys.argv[1])
    results = deduce(data, 'lox-lh2', 100)
    print (results)

# vim: set sw=4 tw=80 :
