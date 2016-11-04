import sys

if '-nogui' in sys.argv:
    import netpyne
    netpyne.__gui__ = False
    
import HHSmall  # import parameters file 
from netpyne import sim  # import netpyne sim module

sim.createSimulateAnalyze(netParams = HHSmall.netParams, simConfig = HHSmall.simConfig)  # create and simulate network