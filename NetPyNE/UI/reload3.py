
import logging
from LEMS_HHSimple_netpyne import NetPyNESimulation

logging.info(' >> Loading from python generated from jnml...')
ns = NetPyNESimulation(tstop=450.0, dt=0.05, seed=123456789, save_json=False)

#ns.run()

simConfig = ns.simConfig
fileName = ns.nml2_file_name

from netpyne.conversion.neuromlFormat import importNeuroML2

gids, netParams = importNeuroML2(fileName, simConfig, simulate=False, analyze=False, return_net_params_also=True)

logging.info(' >> Finished import!...')

print(' - simConfig (%s) with keys: \n      %s'%(type(simConfig),simConfig.todict().keys()))
print(' - netParams (%s) with keys: \n      %s'%(type(netParams),netParams.todict().keys()))

from netpyne.sim.save import saveData
simConfig.saveJson = True

saveData(filename='test.json', include=['simConfig','netParams','net'])

logging.info(' >> Done...')
