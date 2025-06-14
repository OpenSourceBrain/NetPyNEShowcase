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

    ## Why do these need to be set?? TODO: take out!
    sim.nhosts = 5
    sim.rank = 1

    fullLemsFileName = os.path.abspath(lemsFileName)
    if verbose:
        print(
            "Importing LEMSSimulation with NeuroML 2 network from: %s"
            % fullLemsFileName
        )

    success = pynml.run_lems_with_jneuroml_netpyne(lemsFileName, only_generate_json=True, verbose=True)

    if not success == True:
        raise Exception('Problem running netpyne: %s'%success)
    else:
        print('Successful generation of the NetPyNE files...')

    #lems = pynml.read_lems_file(lemsFileName)

    json_filename = lemsFileName.replace('.xml','_netpyne_data.json')
    print('Loading JSON file: %s'%json_filename)

    with open(json_filename, 'r') as f:
        netpyne_info = json.load(f)

        print("All keys: {}".format(netpyne_info.keys()))
        print("net keys: {}".format(netpyne_info['net'].keys()))

    sim.loadAll(json_filename)

    print("Loaded network into NetPyNE containing %s which would run for %s ms"%([d for d in sim.net.params.popParams.keys()], sim.cfg.duration))




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
    elif '-nml2' in sys.argv:
        convertAndImportNeuroML2("../../NeuroML2/multicomp/DendConn.net.nml")
    elif '-nml3' in sys.argv:
        convertAndImportNeuroML2("../ACnet/MediumNet.net.nml")
    elif '-l2' in sys.argv:
        convertAndImportLEMSSimulation("../Dir with spaces/LEMS_MediumNet.xml")
    else:
        convertAndImportLEMSSimulation("LEMS_HHSimple.xml")
