import sys

import HHSmall  # import parameters file

showgui = not '-nogui' in sys.argv
simConfig = HHSmall.simConfig
simConfig['plotRaster'] = simConfig['plotRaster'] if showgui else False
simConfig['plotCells'] = simConfig['plotCells'] if showgui else []
simConfig['plot2Dnet'] = simConfig['plot2Dnet'] if showgui else False

from netpyne import sim  # import netpyne sim module

sim.createAndSimulate(netParams = HHSmall.netParams, simConfig = simConfig)  # create and simulate network

from neuron import h

h('forall psection()')