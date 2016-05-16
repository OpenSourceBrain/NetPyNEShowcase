import HHSmall  # import parameters file
from netpyne import init  # import netpyne init module

init.createAndExport(netParams = HHSmall.netParams, 
                       simConfig = HHSmall.simConfig,
                       reference = 'HHSmall')  # create and export network to NeuroML 2