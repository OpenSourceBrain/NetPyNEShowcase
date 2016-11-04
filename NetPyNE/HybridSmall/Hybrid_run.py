import sys

if '-nogui' in sys.argv:
    import netpyne
    netpyne.__gui__ = False
    
import HybridSmall  # import parameters file
from netpyne import sim  # import netpyne init module

sim.createSimulateAnalyze(netParams = HybridSmall.netParams, simConfig = HybridSmall.simConfig)  # create and simulate network