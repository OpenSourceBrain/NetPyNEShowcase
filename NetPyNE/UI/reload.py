# From https://github.com/harshagurnani/GoC_Varied_Inputs/blob/ankur/Tests/single_cell/test_single_cell_netpyne_load.py

from pathlib import Path
from netpyne import sim
import json

json_file = Path('output_data.json')
with json_file.open(mode='r') as f:
    netpyne_info = json.load(f)

    print("All keys: {}".format(netpyne_info.keys()))
    print("net keys: {}".format(netpyne_info['net'].keys()))
    # TODO: what does the 'cell' key hold?
    netParams = netpyne_info['net']['params']
    simConfig = netpyne_info['simConfig']
    sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig,
                                  output=False)
