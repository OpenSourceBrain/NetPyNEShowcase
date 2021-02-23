#!/bin/bash
set -ex

python NetPyNE_init.py -run

python reload.py

jnml LEMS_HHSimple.xml -nogui
jnml LEMS_HHSimple.xml -neuron -run -nogui
jnml LEMS_HHSimple.xml -netpyne -run -nogui

python LEMS_HHSimple_netpyne.py -json
