import HybridSmall  # import parameters file
from netpyne import sim  # import netpyne sim module

sim.createExportNeuroML2(netParams = HybridSmall.netParams, 
                       simConfig = HybridSmall.simConfig,
                       reference = 'HybridSmall')  # create and export network to NeuroML 2