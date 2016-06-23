import HHSmall  # import parameters file
from netpyne import sim  # import netpyne sim module

sim.createAndExportNeuroML2(netParams = HHSmall.netParams, 
                       simConfig = HHSmall.simConfig,
                       reference = 'HHSmall')  # create and export network to NeuroML 2