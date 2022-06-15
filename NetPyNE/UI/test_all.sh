#!/bin/bash
set -ex

rm -f output_data.json HHCellNetwork.txt_data.json # Remove previous versions

# This python script was exported from NetPyNE UI & runs fine
# It saves output_data.json
python NetPyNE_init.py -run
# JSON file generated following that simulation is reloaded and run
python reload.py


# A LEMS simulation for a simple NML network is run in various ways
pynml LEMS_HHSimple.xml -nogui                 # run with jNeuroML
pynml LEMS_HHSimple.xml -neuron -run -nogui    # run in NEURON
pynml LEMS_HHSimple.xml -netpyne -run -nogui   # run in NetPyNE

# This python script was generated above & is rerun with -json option & so the model is saved to json
python LEMS_HHSimple_netpyne.py -json
# Try reloading that JSON model and rerunning
python reload2.py


# Try loading & running file LEMS_HHSimple_netpyne.py
python reload3.py


# Test helper methods

rm -rf x86_64
python helpers.py
rm -rf x86_64
python helpers.py -nml
