import HHSmall  # import parameters file
from netpyne import init  # import netpyne init module

init.createAndSimulate(netParams = HHSmall.netParams, simConfig = HHSmall.simConfig)  # create and simulate network