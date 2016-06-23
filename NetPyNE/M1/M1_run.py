import M1  # import parameters file
from netpyne import sim  # import netpyne sim module

sim.createAndSimulate(netParams = M1.netParams, simConfig = M1.simConfig)  # create and simulate network