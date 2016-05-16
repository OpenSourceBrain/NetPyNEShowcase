##  Regenerate NetPyNE from NeuroML 2

cd NeuroML2

jnml LEMS_2007One.xml -netpyne

cp *.mod *_netpyne.py *definition.py ../NetPyNE


##  Test Izh

cd ../NetPyNE

nrnivmodl
python LEMS_2007One_netpyne.py


##  Test NetPyNE examples

cd HHSmall

python HH_run.py -nogui

cd ../HybridSmall

python Hybrid_run.py -nogui


##  Done

cd ../..


