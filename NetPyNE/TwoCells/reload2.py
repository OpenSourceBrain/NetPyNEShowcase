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
cfg.validateNetParams = True
cfg.verbose = True


for cell in netParams_dict['cellParams']:
    for sec in netParams_dict['cellParams'][cell]['secs']:
        if len(netParams_dict['cellParams'][cell]['secs'][sec]['ions'])==0:
            netParams_dict['cellParams'][cell]['secs'][sec]['ions']['none']={'e':0,'i':0,"o":0}
        for ion_name in netParams_dict['cellParams'][cell]['secs'][sec]['ions']:
            ion = netParams_dict['cellParams'][cell]['secs'][sec]['ions'][ion_name]
            if not 'o' in ion: ion['o'] = 0 
            if not 'i' in ion: ion['i'] = 0 
            print('>> %s - %s - %s'%(cell, sec, ion))

netParams = NetParams(netParams_dict)

print(' - simConfig (%s) with keys: \n      %s'%(type(cfg),cfg.todict().keys()))
print(' - netParams (%s) with keys: \n      %s'%(type(netParams),netParams.todict().keys()))




import netpyne
#netpyne.sim.validator.validateNetParams = lambda a: (False, False)

from netpyne.sim.validator import validateNetParams

print('==============================')
validateNetParams(netParams)
print('==============================')

print('> Done...')
