import sys

import HybridSmall  # import parameters file

showgui = not '-nogui' in sys.argv
simConfig = HybridSmall.simConfig
simConfig['plotRaster'] = simConfig['plotRaster'] if showgui else False
simConfig['plotCells'] = simConfig['plotCells'] if showgui else []
#simConfig['plot2Dnet'] = simConfig['plot2Dnet'] if showgui else False

from netpyne import init  # import netpyne init module

init.createAndSimulate(netParams = HybridSmall.netParams, simConfig = simConfig)  # create and simulate network

from neuron import h

h('forall psection()')