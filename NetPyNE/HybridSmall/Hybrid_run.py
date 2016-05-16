import sys

import HybridSmall  # import parameters file

showgui = not '-nogui' in sys.argv
simConfig = HybridSmall.simConfig
simConfig['plotRaster'] = showgui
simConfig['plotCells'] = [0] if showgui else []
simConfig['plot2Dnet'] = showgui

from netpyne import init  # import netpyne init module

init.createAndSimulate(netParams = HybridSmall.netParams, simConfig = simConfig)  # create and simulate network