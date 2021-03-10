

import logging
from LEMS_HHSimple_netpyne import NetPyNESimulation

logging.info('Loading from python generated from jnml...')
ns = NetPyNESimulation(tstop=450.0, dt=0.05, seed=123456789, save_json=False)

simConfig, netParams = ns.run()
logging.info('Finished run!...')


print(' - simConfig (%s) with keys: \n      %s'%(type(simConfig),simConfig.todict().keys()))
print(' - netParams (%s) with keys: \n      %s'%(type(netParams),netParams.todict().keys()))
print(' - netParams.cellParams: \n      %s'%(netParams.cellParams))


logging.info('> Done...')
