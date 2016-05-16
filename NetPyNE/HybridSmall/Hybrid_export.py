import HybridSmall  # import parameters file
from netpyne import init  # import netpyne init module

init.createAndExport(netParams = HybridSmall.netParams, 
                       simConfig = HybridSmall.simConfig,
                       reference = 'HybridSmall')  # create and export network to NeuroML 2