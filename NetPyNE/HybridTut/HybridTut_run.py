import sys

if '-nogui' in sys.argv:
    import netpyne
    netpyne.__gui__ = False
    
import HybridTut  # import parameters file
from netpyne import sim 

sim.createSimulateAnalyze(netParams = HybridTut.netParams, simConfig = HybridTut.simConfig)  # create and simulate network