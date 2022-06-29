from pyneuroml import pynml
from pyneuroml.lems import generate_lems_file_for_neuroml
from pyneuroml.pynml import read_neuroml2_file

import os
import sys
import shutil
import subprocess
import neuron
import json

from netpyne import sim


'''
    Converts a LEMS Simulation file (https://docs.neuroml.org/Userdocs/LEMSSimulation.html)
    pointing to a NeuroML 2 file into the equivalent in NetPyNE

'''
def convertAndImportLEMSSimulation(lemsFileName, verbose=True):

    fullLemsFileName = os.path.abspath(lemsFileName)
    if verbose:
        print(
            "Importing LEMSSimulation with NeuroML 2 network from: %s"
            % fullLemsFileName
        )

    pynml.run_lems_with_jneuroml_netpyne(lemsFileName, only_generate_json=True)

    lems = pynml.read_lems_file(lemsFileName)

    #print(lems.components[lems.targets[0]])
    #network = lems.components[lems.targets[0]].parameters['target']
    json_filename = lemsFileName.replace('.xml','_netpyne_data.json')
    print('Loading JSON file: %s'%json_filename)

    with open(json_filename, 'r') as f:
        netpyne_info = json.load(f)

        print("All keys: {}".format(netpyne_info.keys()))
        print("net keys: {}".format(netpyne_info['net'].keys()))
        netParams_dict = netpyne_info['net']['params']
        simConfig_dict = netpyne_info['simConfig']


        sim.createSimulateAnalyze(netParams=netParams_dict, simConfig=simConfig_dict,
                                      output=False)


    '''
    netpyne_file = lemsFileName.replace(".xml", "_netpyne")

    compileModMechFiles(compileMod=True, modFolder=os.path.dirname(fullLemsFileName))

    import_str = "from %s import NetPyNESimulation" % netpyne_file

    exec(import_str, globals())

    if verbose:
        print("Loading from python generated from jnml (using: %s)..." % import_str)

    ns = eval("NetPyNESimulation()")

    simConfig = ns.simConfig
    fileName = ns.nml2_file_name

    from netpyne.conversion.neuromlFormat import importNeuroML2

    gids = importNeuroML2(
        fileName,
        simConfig,
        simulate=False,
        analyze=False,
    )
    from netpyne import sim
    netParams = sim.net.params

    if verbose:
        print("Finished NeuroML/LEMS import!...")

        print(
            " - simConfig (%s) with keys: \n      %s"
            % (type(simConfig), simConfig.todict().keys())
        )
        print(
            " - netParams (%s) with keys: \n      %s"
            % (type(netParams), netParams.todict().keys())
        )

    from netpyne.sim.save import saveData

    simConfig.saveJson = True

    saveData(filename="test.json", include=["simConfig", "netParams", "net"])

    return simConfig, netParams'''

'''
    Compiles the mod files in a directory, removing the old compiled files if found
    and throwing an erro if they had already been loaded
'''
'''
def compileModMechFiles(compileMod, modFolder):
    # Create Symbolic link
    if compileMod:
        modPath = os.path.join(str(modFolder), "x86_64")

        if os.path.exists(modPath):
            print("Deleting existing %s"%modPath)
            shutil.rmtree(modPath)

        os.chdir(modFolder)
        subprocess.call(["nrnivmodl"])

        try:
            neuron.load_mechanisms(str(modFolder))
            print("Loaded mod file mechanisms from %s" % modFolder)
        except:
            print(
                "************************************************************\n"
                +"Error loading the newly generated mod file mechanisms from folder: %s"
                % modFolder
            )
            print(
                "\nNote: if this is the current folder, this may be due to a preexisting "
                + "mod file of the same name being already compiled in that folder and "
                + "NEURON attempting to load it agian. \nRemove any previous x86_64 etc. "
                + "directories before calling this method.\n"+
                "************************************************************"
            )
            raise'''


'''
    Loads a NeuroML 2 file into NetPyNE by creating a new LEMS Simulation
    file (https://docs.neuroml.org/Userdocs/LEMSSimulation.html) and using jNeuroML
    to convert it.

    Returns:
        simConfig, netParams for the model in NetPyNE
'''
def convertAndImportNeuroML2(nml2FileName, verbose=True):

    fullNmlFileName = os.path.abspath(nml2FileName)
    if verbose:
        print(
            "Importing NeuroML 2 network from: %s"
            % fullNmlFileName
        )
    nml_model = read_neuroml2_file(fullNmlFileName)

    target = nml_model.networks[0].id
    sim_id = "Sim_%s"%target
    duration = 1000
    dt = 0.025
    lems_file_name = "LEMS_%s.xml" % sim_id
    target_dir = "."

    generate_lems_file_for_neuroml(
        sim_id,
        fullNmlFileName,
        target,
        duration,
        dt,
        lems_file_name,
        target_dir,
        include_extra_files=["PyNN.xml"],
        gen_plots_for_all_v=True,
        plot_all_segments=False,
        gen_plots_for_quantities={},  # Dict with displays vs lists of quantity paths
        gen_plots_for_only_populations=[],  # List of populations, all pops if = []
        gen_saves_for_all_v=True,
        save_all_segments=False,
        gen_saves_for_only_populations=[],  # List of populations, all pops if = []
        gen_saves_for_quantities={},  # Dict with file names vs lists of quantity paths
        gen_spike_saves_for_all_somas=True,
        report_file_name="report.txt",
        copy_neuroml=False,
        verbose=verbose,
    )
    return convertAndImportLEMSSimulation(lems_file_name)


if __name__ == "__main__":


    if '-nml' in sys.argv:
        convertAndImportNeuroML2("../../NeuroML2/Spikers.net.nml")
    else:
        convertAndImportLEMSSimulation("LEMS_HHSimple.xml")
