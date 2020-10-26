from HHSmall import generate_netParams, simConfig
netParams = generate_netParams(None)
from netpyne import sim  # import netpyne sim module

sim.createExportNeuroML2(netParams = netParams, 
                       simConfig = simConfig,
                       reference = 'HHSmall')  # create and export network to NeuroML 2