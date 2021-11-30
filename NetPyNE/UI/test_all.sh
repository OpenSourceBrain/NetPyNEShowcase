#!/bin/bash
set -ex

# This python script was exported from NetPyNE UI & runs fine
# It saves output_data.json
python NetPyNE_init.py -run
# JSON file generated following that simulation is reloaded and run
python reload.py


# A LEMS simulation for a simple NML network is run in various ways
jnml LEMS_HHSimple.xml -nogui                 # run with jNeuroML
jnml LEMS_HHSimple.xml -neuron -run -nogui    # run in NEURON
jnml LEMS_HHSimple.xml -netpyne -run -nogui   # run in NetPyNE

# This python script was generated above & is rerun with -json option & so the model is saved to json
python LEMS_HHSimple_netpyne.py -json
# Try reloading that JSON model and rerunning
python reload2.py
