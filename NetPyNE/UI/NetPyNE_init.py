from netpyne import specs, sim

# DOCUMENTATION ----------------------------------------------------------------
''' Script generated with NetPyNE-UI. Please visit:
    - https://www.netpyne.org
    - https://github.com/MetaCell/NetPyNE-UI
'''

# SCRIPT =======================================================================
netParams = specs.NetParams()
simConfig = specs.SimConfig()

# SINGLE VALUE ATTRIBUTES ------------------------------------------------------

# NETWORK ATTRIBUTES -----------------------------------------------------------
netParams.popParams['Exc'] = {
    "cellType": "pyr",
    "cellModel": "",
    "pop": "E",
    "numCells": 16
}
netParams.cellParams['pyr_rule'] = {
    "conds": {
        "cellType": "pyr"
    },
    "secs": {
        "soma": {
            "geom": {
                "diam": 20,
                "L": 20,
                "Ra": 100.0,
                "cm": 1
            },
            "mechs": {
                "hh": {
                    "gnabar": 0.12,
                    "gkbar": 0.036,
                    "gl": 0.003,
                    "el": -70
                }
            }
        },
        "dend": {
            "geom": {
                "diam": 5.0,
                "L": 150.0,
                "Ra": 100.0,
                "cm": 1
            },
            "topol": {
                "parentSec": "soma",
                "parentX": 1.0,
                "childX": 0
            },
            "mechs": {
                "pas": {
                    "g": 0.0004,
                    "e": -70
                }
            }
        }
    }
}
netParams.synMechParams['exc'] = {
    "mod": "Exp2Syn",
    "tau1": 0.1,
    "tau2": 1.0,
    "e": 0
}
netParams.connParams['Exc->Exc'] = {
    "preConds": {
        "pop": "Exc"
    },
    "postConds": {
        "pop": "Exc"
    },
    "weight": 0.03,
    "probability": 0.3,
    "delay": 5,
    "synMech": "exc",
    "sec": "soma"
}
netParams.stimSourceParams['IClamp1'] = {
    "type": "IClamp",
    "dur": 10,
    "del": 20,
    "amp": 0.6
}
netParams.stimTargetParams['IClamp1->cell0'] = {
    "source": "IClamp1",
    "conds": {
        "cellList": [
            0
        ]
    },
    "sec": "dend",
    "loc": 1.0
}

# NETWORK CONFIGURATION --------------------------------------------------------
simConfig.duration = 200.0
simConfig.recordCells = [
    0,1
]
simConfig.recordTraces = {
    "V_soma": {
        "sec": "soma",
        "loc": 0.5,
        "var": "v"
    },
    "V_dend": {
        "sec": "dend",
        "loc": 1.0,
        "var": "v"
    }
}
simConfig.recordStep = 0.1
simConfig.filename = "output"
simConfig.saveJson = True
simConfig.saveDat = True

# CREATE SIMULATE ANALYZE  NETWORK ---------------------------------------------
import sys
if '-run' in sys.argv:
    sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

print('Finished network creation')

# END SCRIPT ===================================================================
