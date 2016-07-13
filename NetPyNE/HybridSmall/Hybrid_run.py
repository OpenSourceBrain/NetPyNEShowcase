import sys

import HybridSmall  # import parameters file

showgui = not '-nogui' in sys.argv
simConfig = HybridSmall.simConfig
simConfig.addAnalysis('plotRaster', showgui)
simConfig.addAnalysis('plotTraces', {'include': [2]} if showgui else {})
simConfig.addAnalysis('plot2Dnet', showgui)

from netpyne import sim  # import netpyne sim module

sim.createSimulateAnalyze(netParams = HybridSmall.netParams, simConfig = simConfig)  # create and simulate network

from neuron import h

h('forall psection()')