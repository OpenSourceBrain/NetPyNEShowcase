# From https://github.com/harshagurnani/GoC_Varied_Inputs/blob/ankur/Tests/single_cell/test_single_cell_netpyne_load.py

from pathlib import Path
from netpyne import sim
import json

json_file = Path('LEMS_TwoCell_netpyne_data.json')
netParams_dict = None
simConfig_dict = None

with json_file.open(mode='r') as f:
    netpyne_info = json.load(f)

    netParams_dict = netpyne_info['net']['params']
    simConfig_dict = netpyne_info['simConfig']

'''
    simConfig_dict['saveJson'] = False # Prevent overwriting json gnerated by nml export
    simConfig_dict['saveDat'] = True # Save data from this run
    print('> Creating, simulating, analyzing...')
    sim.createSimulateAnalyze(netParams=netParams_dict, simConfig=simConfig_dict,
                                  output=False)

print(' - simConfig_dict (%s) with keys: \n      %s'%(type(simConfig_dict),simConfig_dict.keys()))
print(' - netParams_dict (%s) with keys: \n      %s'%(type(netParams_dict),netParams_dict.keys()))
print(" - netParams_dict['cellParams']: \n      %s"%(netParams_dict['cellParams']))
'''

from netpyne.specs.simConfig import SimConfig
from netpyne.specs.netParams import NetParams

cfg = SimConfig(simConfig_dict)
netParams = NetParams(netParams_dict)
print(' - simConfig (%s) with keys: \n      %s'%(type(cfg),cfg.todict().keys()))
print(' - netParams (%s) with keys: \n      %s'%(type(netParams),netParams.todict().keys()))


print('> Done...')
