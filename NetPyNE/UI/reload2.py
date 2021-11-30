# From https://github.com/harshagurnani/GoC_Varied_Inputs/blob/ankur/Tests/single_cell/test_single_cell_netpyne_load.py

from pathlib import Path
from netpyne import sim
import json

json_file = Path('HHCellNetwork.txt_data.json')
with json_file.open(mode='r') as f:
    netpyne_info = json.load(f)

    netParams = netpyne_info['net']['params']
    simConfig = netpyne_info['simConfig']


    simConfig['saveJson'] = False # Prevent overwriting json gnerated by nml export
    simConfig['saveDat'] = True # Save data from this run
    print('> Creating, simulating, analyzing...')
    sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig,
                                  output=False)
    print('> Done...')
