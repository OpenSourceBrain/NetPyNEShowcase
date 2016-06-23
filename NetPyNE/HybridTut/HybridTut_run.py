import HybridTut  # import parameters file
from netpyne import sim  # import netpyne sim module

sim.createAndSimulate(netParams = HybridTut.netParams, simConfig = HybridTut.simConfig)  # create and simulate network