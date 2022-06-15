from pyneuroml import pynml
import os
import shutil
import subprocess
import neuron


def convertAndImportLEMSSimulation(
    lemsFileName, simulate=False, analyze=False, verbose=True
):

    fullLemsFileName = os.path.abspath(lemsFileName)
    if verbose:
        print(
            "Importing LEMSSimulation with NeuroML 2 network from: %s"
            % fullLemsFileName
        )

    pynml.run_lems_with_jneuroml_netpyne(lemsFileName, only_generate_scripts=True)
    netpyne_file = lemsFileName.replace(".xml", "_netpyne")

    compileModMechFiles(compileMod=True, modFolder=os.path.dirname(fullLemsFileName))

    #print(os.getcwd())

    import_str = "from %s import NetPyNESimulation" % netpyne_file

    exec(import_str, globals())

    if verbose:
        print("Loading from python generated from jnml (using: %s)..." % import_str)

    ns = eval("NetPyNESimulation(tstop=1000, dt=0.025)")

    simConfig = ns.simConfig
    fileName = ns.nml2_file_name

    from netpyne.conversion.neuromlFormat import importNeuroML2

    gids, netParams = importNeuroML2(
        fileName,
        simConfig,
        simulate=simulate,
        analyze=analyze,
        return_net_params_also=True,
    )

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
            raise


if __name__ == "__main__":

    convertAndImportLEMSSimulation("LEMS_HHSimple.xml", simulate=False)
