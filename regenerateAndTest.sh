#!/bin/bash
set -ex

################  Regenerate NetPyNE from NeuroML 2

cd NeuroML2

pynml LEMS_2007One.xml -netpyne

cp RS*.mod *_netpyne.py NET_2007One.net.nml ../NetPyNE

pynml LEMS_GJ.xml -netpyne

cp LEMS_GJ_netpyne.py pulseGen2.mod pulseGen1.mod gj1.mod iaf.mod GJ.nml ../NetPyNE/GapJunctions

cd TwoCells

rm -f *mod
pynml LEMS_TwoCell.xml -netpyne -json

# Remove generated local filename
sed -i -e "s#/Users/padraig/neuroConstruct/osb/showcase/NetPyNEShowcase/NeuroML2/TwoCells/##g" LEMS_TwoCell_netpyne_data.json

cp LEMS_TwoCell_netpyne.py *.mod *.nml *json ../../NetPyNE/TwoCells


cd ../gaps
python ExampleGaps.py -jnml

cd ..


################  Copy over nml to netpyne dirs (for testing)

cp *.cell.nml *.channel.nml ../NetPyNE/HHSmall
cp *.cell.nml *.channel.nml ../NetPyNE/HybridSmall
cp *.cell.nml *.channel.nml ../NetPyNE/HybridTut
cp *.cell.nml *.channel.nml ../NetPyNE/M1

################  Test Izh can run

cd ../NetPyNE

nrnivmodl
python LEMS_2007One_netpyne.py



################  Test NetPyNE examples

cd HHSmall

python HH_run.py -nogui

cd ../HybridSmall

nrnivmodl
python Hybrid_run.py -nogui

cd ../HybridTut

nrnivmodl
python HybridTut_run.py -nogui

################ Export NeuroML 2

cd ../HHSmall
python HH_export.py
cp *.nml ../../NeuroML2
cp LEMS*.xml ../../NeuroML2

cd ../HybridSmall
python Hybrid_export.py
cp *.nml ../../NeuroML2
cp LEMS*.xml ../../NeuroML2

cd ../HybridTut
python HybridTut_export.py
cp *.nml ../../NeuroML2
cp LEMS*.xml ../../NeuroML2

cd ../M1
nrnivmodl
python M1_export.py
cp *.nml ../../NeuroML2
cp LEMS*.xml ../../NeuroML2

cd ../../NeuroML2
pynml -validate *cell.nml *channel.nml *synapse.nml HHCellNetwork.net.nml  HHSmall.net.nml  HybridSmall.net.nml  HybridTut.net.nml  M1.net.nml SimpleNet.net.nml



################ Test scripts for UI

cd ../NetPyNE/UI
./test_all.sh

cd ../ACnet
rm -rf x86_64
python convert.py


################  Done

cd ../..

echo "Finished all tests"
