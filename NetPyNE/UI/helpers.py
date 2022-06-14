

from pyneuroml import pynml

def convertAndImportLEMSSimulation(lemsFileName, simulate=True, analyze=True):

    print("Importing LEMSSimulation with NeuroML 2 network from: %s"%lemsFileName)

    results1 = pynml.run_lems_with_jneuroml_netpyne(
        lemsFileName, only_generate_scripts=True
    )
    netpyne_file = lemsFileName.replace('.xml', '_netpyne')

    #import_str = 'from %s import NetPyNESimulation'%netpyne_file
    import importlib
    importlib.import_module('%s'%netpyne_file)

    from LEMS_HHSimple_netpyne import NetPyNESimulation

    print('Loading from python generated from jnml (using: %s)...'%netpyne_file)

    print(importlib)

    ns = eval('NetPyNESimulation(tstop=450.0, dt=0.05, seed=1234, save_json=False)')

    print(ns)

    simConfig = ns.simConfig
    fileName = ns.nml2_file_name

    from netpyne.conversion.neuromlFormat import importNeuroML2

    gids, netParams = importNeuroML2(fileName, simConfig, simulate=False, analyze=False, return_net_params_also=True)

    print(' >> Finished NeuroML/LEMS import!...')

    print(' - simConfig (%s) with keys: \n      %s'%(type(simConfig),simConfig.todict().keys()))
    print(' - netParams (%s) with keys: \n      %s'%(type(netParams),netParams.todict().keys()))

    from netpyne.sim.save import saveData
    simConfig.saveJson = True

    saveData(filename='test.json', include=['simConfig','netParams','net'])

    print(' >> Done...')


convertAndImportLEMSSimulation("LEMS_HHSimple.xml", simulate=False)
