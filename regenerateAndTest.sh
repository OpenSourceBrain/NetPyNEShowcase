set -e
################  Regenerate NetPyNE from NeuroML 2

cd NeuroML2

jnml LEMS_2007One.xml -netpyne

cp *.mod *_netpyne.py *definition.py ../NetPyNE


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

cd ../HybridSmall
python Hybrid_export.py 
cp *.nml ../../NeuroML2

cd ../HybridTut
python HybridTut_export.py 
cp *.nml ../../NeuroML2

cd ../M1
python M1_export.py 
cp *.nml ../../NeuroML2

cd ../../NeuroML2
jnml -validate *.nml

################  Done

cd ../..


