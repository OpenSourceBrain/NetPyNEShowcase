import sys

if '-nogui' in sys.argv:
    import netpyne
    netpyne.__gui__ = False
    
from HHSmall import generate_netParams, simConfig
netParams = generate_netParams(None)
from netpyne import sim  # import netpyne sim module

sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)  # create and simulate network