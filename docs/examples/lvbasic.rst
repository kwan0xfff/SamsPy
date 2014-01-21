===========================
Launch Vehicle Basic Report
===========================

A prototype launch vehicle *ProtoLV* is used as an example for
illustrating the output of the ``lvbasic.py`` command.
The vehicle is described by the input file, ``protolv.yaml``.
Basically, it is a three-stage rocket, with all stages burning a mixture
of liquid oxygen (LOX) and kerosene (RP-1).
(Note: As the source code is refined, the ``protolv.yaml`` file content
may vary from the description given here.)

Vehicle description
===================

Specific impulse (Isp) is assumed to be 293, 290, and 293 seconds for
the first, second, and third stages.  These numbers are somewhat low
for peak LOX/RP-1 performance, but if someone is developing a new set
of engines, early tests may result in the lower numbers until combustion
chamber pressure is pushed up.

Maximum acceleration is to 3 Gs.
This is more representative of large launch vehicles, such as those
carrying astronauts, than sounding rockets.

The program (command) makes very simplistic assumptions about its environment.
There is no atmosphere and no gravity.
As a result, the performance numbers reported are higher than they would
be in a real launch environment.
But they are nevertheless useful while comparing different vehicle configurations.

The vehicle description (``protolv.yaml``) currently looks like this::

    # Launch vehicle profile:  hypothetical Prototype Launch Vehicle
    #
    # Measures in meters, kilograms, seconds
    
    name:  Prototype LV
    stageorder: [ Proto LV-1, Proto LV-2, Proto LV-3, payload ]
    maxG: 3.0
    stages:
        Proto LV-1:
            Mwet: 17934.0 # kg
            Mdry: 2886.0 # kg
            Isp: 293 # sec
            mixture: lox-rp1
        Proto LV-2:
            Mwet: 4331.0 # kg
            Mdry: 416.0 # kg
            Isp: 290 # sec
            mixture: lox-rp1
        Proto LV-3:
            Mwet: 985.0 # kg
            Mdry: 203.0 # kg
            mixture: lox-rp1
            Isp: 293 # sec
        payload:
            Mwet: 443.0 # kg
            Mdry: 443.0 # kg
            mixture: lox-rp1
            Isp: 0 # sec

The file describes the sequencing of stages (``stageorder``),
the maximum acceleration allowed (``maxG``),
and then describes the stages themselves.
The wet (propellant fully loaded) and dry masses (``Mwet`` and ``Mdry``)
are the values for the stage itself.
The cumulative mass sums are computed by the program, and reported later.
The last stage is really the payload, which has no change in mass, and no propulsion.
(It reality, a satellite might have propellant for station-keeping,
but that has no impact on launch.)

Command
=======

Before executing the command, the path the the SamsPy library needs to be set up.
For example,::

    $ export PYTHONPATH=/home/myuserid/samspy/lib

Within the ``samspy/lib`` directory, the subdirectory ``samspy`` can
be found.  This allows the command to execute Python code such as::

    from samspy.vehicle import multistage, propel

Using the example files provided in the source code, the command executed is::

    $ cmds/lvbasic.py -p share/propellants.yaml share/protolv.yaml

The ``-p`` flag points to the file with propellant information.

Program output
==============

The current output of the program does not repeat the input numbers from
the vehicle description file.

The first part of the shows the masses of the launch vehicle at stage ignition and burnout,
and the resulting velocity change (deltaV)::

    Proto LV-1                       Mignite 23693.0 Mburnout  8645.0 kilo
    Proto LV-1                       Mignite 52234.1 Mburnout 19059.0 lbm
    Proto LV-1                        deltaV  2896.9
    Proto LV-2                       Mignite  5759.0 Mburnout  1844.0 kilo
    Proto LV-2                       Mignite 12696.4 Mburnout  4065.3 lbm
    Proto LV-2                        deltaV  3238.7
    Proto LV-3                       Mignite  1428.0 Mburnout   646.0 kilo
    Proto LV-3                       Mignite  3148.2 Mburnout  1424.2 lbm
    Proto LV-3                        deltaV  2279.2
    payload                          Mignite   443.0 Mburnout   443.0 kilo
    payload                          Mignite   976.6 Mburnout   976.6 lbm
    payload                           deltaV     0.0
        Total deltaV (m/s, ft/s)   8414.8755  27607.8592

The initial mass of the vehicle is 23,693 kg (52,234.1 lbm);
this is the culmulative gross mass of all the stages.

The culmulative deltaV achieved by all three stages is about 8.4 km/s.
Note, however,
(1) orbital speed in low Earth orbit is about 7.8 km/s;
(2) this above computation did not factor in atmospheric drag or gravity.
So actual deltaV is likely somewhat lower.
Furthermore, the engines are not throttled; they burn at full thrust until burnout.

The second part of the output gives details on each stage.
Knowing the densities of the propellants, and the oxidizer/fuel ratios,
it is possible to compute their masses and volumes.
Using LOX/RP-1, it can be seen that the LOX tanks need to be
about twice the size of the RP-1 tanks.

The detailed output appears as follows::

    Stage: Proto LV-1
        matl names                   LOX     RP1   [sum]
        liqdens (kg/l)             1.141   0.910
        masses (kg)              10821.034 4226.966 15048.000
        volume (l)               9483.816 4645.018 14128.834
        avg dens (kg/l)               1.0651
        massflow (kg/s)              88.5154
        burn time (s)               170.0044
        G (ignite, burnout)        1.095   3.000
        thrust (N, lbf)          254335.4678  57176.8877
        wt ignite (N, lbm)       232348.9584  52234.1238
        wt burnout (N, lbm)       84778.4892  19058.9626
        deltaV (m/s, ft/s)         2896.9057   9504.2837
        wet mass                  23693.0000  52234.1238
        dry mass                   8645.0000  19058.9626
    Stage: Proto LV-2
        matl names                   LOX     RP1   [sum]
        liqdens (kg/l)             1.141   0.910
        masses (kg)              2815.281 1099.719 3915.000
        volume (l)               2467.380 1208.483 3675.863
        avg dens (kg/l)               1.0651
        massflow (kg/s)              19.0759
        burn time (s)               205.2332
        G (ignite, burnout)        0.961   3.000
        thrust (N, lbf)           54250.3878  12195.9723
        wt ignite (N, lbm)        56476.4973  12696.4217
        wt burnout (N, lbm)       18083.4626   4065.3241
        deltaV (m/s, ft/s)         3238.7418  10625.7932
        wet mass                   5759.0000  12696.4217
        dry mass                   1844.0000   4065.3241
    Stage: Proto LV-3
        matl names                   LOX     RP1   [sum]
        liqdens (kg/l)             1.141   0.910
        masses (kg)              562.337 219.663 782.000
        volume (l)               492.846 241.388 734.234
        avg dens (kg/l)               1.0651
        massflow (kg/s)               6.6143
        burn time (s)               118.2281
        G (ignite, burnout)        1.357   3.000
        thrust (N, lbf)           19005.2877   4272.5586
        wt ignite (N, lbm)        14003.8962   3148.2011
        wt burnout (N, lbm)        6335.0959   1424.1862
        deltaV (m/s, ft/s)         2279.2280   7477.7823
        wet mass                   1428.0000   3148.2011
        dry mass                    646.0000   1424.1862
    Totals:
        dry mass                   3948.0000   8703.8501

Burn times for the three stages are 170, 205, and 118 seconds.
Since the engines burn at full thrust the entire time,
G force starts low and creeps up to max G.
The initial G forces computed are 1.095, 0.961, and 1.357.
If these were for a vertical launch from Earth sea level,
the first stage would slowly get off the ground,
and the second stage would be waging a losing battle against gravity.
Fortunately, the first stage typically starts off vertically,
but after a minute or so has a significant horizontal component.

The last reported number is the cumulative dry mass of the vehicle.
That is, before propellants are pumped into it,
this is what ground transport vehicles must support for the fully assembled,
but empty vehicle.
