'''
NETPYNE simulator compliant export for:

Components:
    pas (Type: ionChannelPassive:  conductance=1.0E-11 (SI conductance))
    hhcell (Type: cell)
    HHCellNetwork (Type: network)
    sim1 (Type: Simulation:  length=0.45 (SI time) step=5.0E-5 (SI time))


    This NETPYNE file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.11.0
         org.neuroml.model   v1.11.0
         jLEMS               v0.12.0

'''
# Main NetPyNE script for: HHCellNetwork

# See https://github.com/Neurosim-lab/netpyne

from netpyne import specs  # import netpyne specs module
from netpyne import sim    # import netpyne sim module
from netpyne import __version__ as version

from neuron import h

import sys
import time
import datetime

class NetPyNESimulation():

    def __init__(self, tstop=450.0, dt=0.05, seed=123456789, save_json=False, abs_tol=None):

        self.setup_start = time.time()
        

        ###############################################################################
        # NETWORK PARAMETERS
        ###############################################################################

        self.nml2_file_name = 'NET_HHSimple.net.nml'

        ###############################################################################
        # SIMULATION PARAMETERS
        ###############################################################################

        self.simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

        # Simulation parameters
        self.simConfig.duration = self.simConfig.tstop = tstop # Duration of the simulation, in ms
        self.simConfig.dt = dt # Internal integration timestep to use

        # cvode
        if abs_tol is not None:
            self.simConfig.cvode_active = True
            self.simConfig.cvode_atol = abs_tol
        else:
            self.simConfig.cvode_active = False

        # Seeds for randomizers (connectivity, input stimulation and cell locations)
        # Note: locations and connections should be fully specified by the structure of the NeuroML,
        # so seeds for conn & loc shouldn't affect networks structure/behaviour
        self.simConfig.seeds = {'conn': 0, 'stim': 123456789, 'loc': 0}

        self.simConfig.createNEURONObj = 1  # create HOC objects when instantiating network
        self.simConfig.createPyStruct = 1  # create Python structure (simulator-independent) when instantiating network
        self.simConfig.verbose = False  # show detailed messages
        
        # Recording
        self.simConfig.recordCells = ['all']
        self.simConfig.recordTraces = {}
        self.simConfig.saveCellSecs=False
        self.simConfig.saveCellConns=False
        self.simConfig.gatherOnlySimData=True

                # For saving to file: hh_v.dat (ref: of0)
                                
        # Column: v0: Pop: hhpop; cell: 0; segment id: 0; segment name: soma; Neuron loc: soma(0.5); value: v (v)
        self.simConfig.recordTraces['of0_hhpop_0_soma_v'] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':'hhpop','cellLabel':0}}
                                
        # Column: v1: Pop: hhpop; cell: 1; segment id: 0; segment name: soma; Neuron loc: soma(0.5); value: v (v)
        self.simConfig.recordTraces['of0_hhpop_1_soma_v'] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':'hhpop','cellLabel':1}}
                        
        
        self.simConfig.plotCells = ['all']

        self.simConfig.recordStim = True  # record spikes of cell stims
        self.simConfig.recordStep = self.simConfig.dt # Step size in ms to save data (eg. V traces, LFP, etc)

        # Analysis and plotting, see http://neurosimlab.org/netpyne/reference.html#analysis-related-functions
        self.simConfig.analysis['plotRaster'] = False  # Plot raster
        self.simConfig.analysis['plot2Dnet'] = False  # Plot 2D net cells and connections
        self.simConfig.analysis['plotSpikeHist'] = False # plot spike histogram
        self.simConfig.analysis['plotConn'] = False # plot network connectivity
        self.simConfig.analysis['plotSpikePSD'] = False # plot 3d architecture

        # Saving
        self.simConfig.filename = 'HHCellNetwork.txt'  # Set file output name
        self.simConfig.saveFileStep = self.simConfig.dt # step size in ms to save data to disk
        # self.simConfig.saveDat = True # save to dat file
        self.simConfig.saveJson = save_json # save to json file


    def run(self):

        ###############################################################################
        # IMPORT & RUN
        ###############################################################################

        print("Running a NetPyNE based simulation for %sms (dt: %sms) at %s degC"%(self.simConfig.duration, self.simConfig.dt, self.simConfig.hParams['celsius']))

        self.setup_sim_start = time.time()
        self.gids = sim.importNeuroML2SimulateAnalyze(self.nml2_file_name,self.simConfig)

        self.sim_end = time.time()
        self.setup_sim_time = self.sim_end - self.setup_sim_start
        print("Finished NetPyNE simulation in %f seconds (%f mins)..."%(self.setup_sim_time, self.setup_sim_time/60.0))

        try:
            self.save_results()
        except Exception as e:
            print("Exception saving results of NetPyNE simulation: %s" % (e))
            return

    def generate_json_only(self):

          ###############################################################################
          # GENERATE NETPYNE JSON REPRESENTATION OF NETWORK
          ###############################################################################

          print("Generating NetPyNE JSON (and mod files)")

          self.simConfig.saveJson = True # save to json file
          from netpyne.conversion.neuromlFormat import importNeuroML2
          self.gids = sim.importNeuroML2(self.nml2_file_name,
                                         self.simConfig,
                                         simulate=False,
                                         analyze=False)

          from netpyne.sim.save import saveData

          json_filename=__file__.replace(".py","")
          saveData(filename=json_filename, include=["simConfig", "netParams", "net"])
          real_json_filename='%s_data.json'%json_filename

          print("Finished exporting the NetPyNE JSON to %s"%real_json_filename)

          return real_json_filename


    def save_results(self):

        ###############################################################################
        #   Saving data (this ensures the data gets saved in the format/files
        #   as specified in the LEMS <Simulation> element)
        ###############################################################################

        if sim.rank==0:
        
            print("Saving traces to file: hh_v.dat (ref: of0)")

                
            # Column: t
            col_of0_t = [i*self.simConfig.dt for i in range(int(self.simConfig.duration/self.simConfig.dt))]
                        
            # Column: v0: Pop: hhpop; cell: 0; segment id: 0; segment name: soma; value: v
            col_of0_v0 = sim.allSimData['of0_hhpop_0_soma_v']['cell_%s'%self.gids['hhpop'][0]]
                        
            # Column: v1: Pop: hhpop; cell: 1; segment id: 0; segment name: soma; value: v
            col_of0_v1 = sim.allSimData['of0_hhpop_1_soma_v']['cell_%s'%self.gids['hhpop'][1]]
                
            dat_file_of0 = open('hh_v.dat', 'w')
            for i in range(len(col_of0_t)):
                dat_file_of0.write( '%s\t'%(col_of0_t[i]/1000.0) +  '%s\t'%(col_of0_v0[i]/1000.0) +  '%s\t'%(col_of0_v1[i]/1000.0) +  '\n')
            dat_file_of0.close()

        
        
            save_end = time.time()
            save_time = save_end - self.sim_end
            print("Finished saving results in %f seconds"%(save_time))


        
if __name__ == '__main__':

    save_json = '-json' in sys.argv
    no_run = '-norun' in sys.argv

    ns = NetPyNESimulation(tstop=450.0, dt=0.05, seed=123456789, save_json=save_json, abs_tol=None)

    if not no_run:
      ns.run()
    else:
      if save_json:
        fn = ns.generate_json_only()
        print("Generated: %s"%fn)
        quit()

    if '-nogui' in sys.argv:
        quit()
