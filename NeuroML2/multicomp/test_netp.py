

from netpyne import specs  # import netpyne specs module
from netpyne import sim    # import netpyne sim module
from netpyne import __version__ as version

from neuron import h

import sys
import time
import datetime

class NetPyNESimulation():

    def __init__(self, tstop, dt, seed=123456789, save_json=False):

        self.setup_start = time.time()


        ###############################################################################
        # NETWORK PARAMETERS
        ###############################################################################

        self.nml2_file_name = 'DendConn.net.nml'

        ###############################################################################
        # SIMULATION PARAMETERS
        ###############################################################################

        self.simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

        # Simulation parameters
        self.simConfig.duration = self.simConfig.tstop = tstop # Duration of the simulation, in ms
        self.simConfig.dt = dt # Internal integration timestep to use

        # Seeds for randomizers (connectivity, input stimulation and cell locations)
        # Note: locations and connections should be fully specified by the structure of the NeuroML,
        # so seeds for conn & loc shouldn't affect networks structure/behaviour
        self.simConfig.seeds = {'conn': 0, 'stim': 12345, 'loc': 0}

        self.simConfig.createNEURONObj = 1  # create HOC objects when instantiating network
        self.simConfig.createPyStruct = 1  # create Python structure (simulator-independent) when instantiating network
        self.simConfig.verbose = False  # show detailed messages

        self.simConfig.hParams['celsius'] = (305.15 - 273.15)

        # Recording
        self.simConfig.recordCells = ['all']
        self.simConfig.recordTraces = {}
        self.simConfig.saveCellSecs=False
        self.simConfig.saveCellConns=False
        self.simConfig.gatherOnlySimData=True

                # For saving to file: Sim_DendConn.pop_pyr.v.dat (ref: Sim_DendConn_pop_pyr_v_dat)

        # Column: pop_pyr_0_pyr_4_sym_0_v: Pop: pop_pyr; cell: 0; segment id: 0; segment name: soma; Neuron loc: soma(0.5); value: v (v)
        self.simConfig.recordTraces['Sim_DendConn_pop_pyr_v_dat_pop_pyr_0_soma_v'] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':'pop_pyr','cellLabel':0}}

        # Column: pop_pyr_1_pyr_4_sym_0_v: Pop: pop_pyr; cell: 1; segment id: 0; segment name: soma; Neuron loc: soma(0.5); value: v (v)
        self.simConfig.recordTraces['Sim_DendConn_pop_pyr_v_dat_pop_pyr_1_soma_v'] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':'pop_pyr','cellLabel':1}}

        # Column: pop_pyr_2_pyr_4_sym_0_v: Pop: pop_pyr; cell: 2; segment id: 0; segment name: soma; Neuron loc: soma(0.5); value: v (v)
        self.simConfig.recordTraces['Sim_DendConn_pop_pyr_v_dat_pop_pyr_2_soma_v'] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':'pop_pyr','cellLabel':2}}

        # Column: pop_pyr_3_pyr_4_sym_0_v: Pop: pop_pyr; cell: 3; segment id: 0; segment name: soma; Neuron loc: soma(0.5); value: v (v)
        self.simConfig.recordTraces['Sim_DendConn_pop_pyr_v_dat_pop_pyr_3_soma_v'] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':'pop_pyr','cellLabel':3}}


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
        self.simConfig.filename = 'DendConn.txt'  # Set file output name
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

        return self.simConfig


    def save_results(self):

        ###############################################################################
        #   Saving data (this ensures the data gets saved in the format/files
        #   as specified in the LEMS <Simulation> element)
        ###############################################################################

        if sim.rank==0:

            print("Saving traces to file: Sim_DendConn.pop_pyr.v.dat (ref: Sim_DendConn_pop_pyr_v_dat)")


            # Column: t
            col_Sim_DendConn_pop_pyr_v_dat_t = [i*self.simConfig.dt for i in range(int(self.simConfig.duration/self.simConfig.dt))]

            # Column: pop_pyr_0_pyr_4_sym_0_v: Pop: pop_pyr; cell: 0; segment id: 0; segment name: soma; value: v
            col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_0_pyr_4_sym_0_v = sim.allSimData['Sim_DendConn_pop_pyr_v_dat_pop_pyr_0_soma_v']['cell_%s'%self.gids['pop_pyr'][0]]

            # Column: pop_pyr_1_pyr_4_sym_0_v: Pop: pop_pyr; cell: 1; segment id: 0; segment name: soma; value: v
            col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_1_pyr_4_sym_0_v = sim.allSimData['Sim_DendConn_pop_pyr_v_dat_pop_pyr_1_soma_v']['cell_%s'%self.gids['pop_pyr'][1]]

            # Column: pop_pyr_2_pyr_4_sym_0_v: Pop: pop_pyr; cell: 2; segment id: 0; segment name: soma; value: v
            col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_2_pyr_4_sym_0_v = sim.allSimData['Sim_DendConn_pop_pyr_v_dat_pop_pyr_2_soma_v']['cell_%s'%self.gids['pop_pyr'][2]]

            # Column: pop_pyr_3_pyr_4_sym_0_v: Pop: pop_pyr; cell: 3; segment id: 0; segment name: soma; value: v
            col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_3_pyr_4_sym_0_v = sim.allSimData['Sim_DendConn_pop_pyr_v_dat_pop_pyr_3_soma_v']['cell_%s'%self.gids['pop_pyr'][3]]

            dat_file_Sim_DendConn_pop_pyr_v_dat = open('Sim_DendConn.pop_pyr.v.dat', 'w')
            for i in range(len(col_Sim_DendConn_pop_pyr_v_dat_t)):
                dat_file_Sim_DendConn_pop_pyr_v_dat.write( '%s\t'%(col_Sim_DendConn_pop_pyr_v_dat_t[i]/1000.0) +  '%s\t'%(col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_0_pyr_4_sym_0_v[i]/1000.0) +  '%s\t'%(col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_1_pyr_4_sym_0_v[i]/1000.0) +  '%s\t'%(col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_2_pyr_4_sym_0_v[i]/1000.0) +  '%s\t'%(col_Sim_DendConn_pop_pyr_v_dat_pop_pyr_3_pyr_4_sym_0_v[i]/1000.0) +  '\n')
            dat_file_Sim_DendConn_pop_pyr_v_dat.close()



            save_end = time.time()
            save_time = save_end - self.sim_end
            print("Finished saving results in %f seconds"%(save_time))



if __name__ == '__main__':

    ns = NetPyNESimulation(tstop=500.0, dt=0.025, seed=12345, save_json=True)

    simConfig = ns.run()

    print(' >> Finished run!...')

    print(' >> simConfig (%s) with keys: \n      %s'%(type(simConfig),simConfig.todict().keys()))
