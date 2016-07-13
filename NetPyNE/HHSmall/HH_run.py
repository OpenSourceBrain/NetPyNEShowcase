import sys

import HHSmall  # import parameters file

showgui = not '-nogui' in sys.argv
simConfig = HHSmall.simConfig
simConfig.addAnalysis('plotRaster', showgui)
simConfig.addAnalysis('plotTraces', {'include': [2]} if showgui else {})
simConfig.addAnalysis('plot2Dnet', showgui)

from netpyne import sim  # import netpyne sim module

sim.createSimulateAnalyze(netParams = HHSmall.netParams, simConfig = simConfig)  # create and simulate network

from neuron import h

h('forall psection()')