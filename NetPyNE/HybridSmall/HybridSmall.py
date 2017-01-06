"""
params.py 

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

Contributors: salvadordura@gmail.com
"""

from netpyne import specs

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

###############################################################################
#
# MPI HH TUTORIAL PARAMS
#
###############################################################################

###############################################################################
# NETWORK PARAMETERS
###############################################################################

pop_size = 3

# Population parameters
netParams.popParams['PYR_HH'] = {'cellModel': 'HH', 'cellType': 'PYR', 'numCells': pop_size} # add dict with params for this pop 
netParams.popParams['PYR_Izhi'] = {'cellModel': 'Izhi', 'cellType': 'PYR', 'numCells': pop_size} # add dict with params for this pop 


# Cell parameters list
## PYR cell properties (HH)
cellRule = {'conds': {'cellType': 'PYR', 'cellModel': 'HH'},  'secs': {}}
cellRule['secs']['soma'] = {'geom': {}, 'topol': {}, 'mechs': {}}  # soma properties
cellRule['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0, 'pt3d':[]}
cellRule['secs']['soma']['geom']['pt3d'].append((0, 0, 0, 18.8))
cellRule['secs']['soma']['geom']['pt3d'].append((0, 0, 18.8, 18.8))
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} 

netParams.cellParams['PYR_HH'] = cellRule  # add dict to list of cell properties

## PYR cell properties (Izhi)
cellRule = {'conds': {'cellType': 'PYR', 'cellModel': 'Izhi'},  'secs': {}}
cellRule['secs']['soma'] = {'geom': {}, 'pointps':{}}  # soma properties
cellRule['secs']['soma']['geom'] = {'diam': 10, 'L': 10, 'cm': 31.831}
cellRule['secs']['soma']['pointps']['Izhi'] = {'mod':'Izhi2007b', 
    'C':1, 'k':0.7, 'vr':-60, 'vt':-40, 'vpeak':35, 'a':0.03, 'b':-2, 'c':-50, 'd':100, 'celltype':1}
netParams.cellParams['PYR_Izhi'] = cellRule  # add dict to list of cell properties


# Synaptic mechanism parameters
netParams.synMechParams['syn1'] = {'mod': 'ExpSyn', 'tau': 30, 'e': 0}
netParams.synMechParams['syn2'] = {'mod': 'ExpSyn', 'tau': 4, 'e': 0}
 

# Stimulation parameters
netParams.stimSourceParams['bkg1'] = {'type': 'NetStim', 'rate': 20, 'noise': 0}
netParams.stimSourceParams['bkg2'] = {'type': 'NetStim', 'rate': 20, 'noise': 1}
netParams.stimTargetParams['bg->PYR_Izhi'] = {'source': 'bkg1', 'conds': {'cellType': 'PYR', 'cellModel': 'Izhi'}, 
                                            'connFunc': 'fullConn','weight': 0.01, 'delay': 0, 'synMech': 'syn2'}  
netParams.stimTargetParams['bg->PYR_HH'] = {'source': 'bkg2', 'conds': {'cellType': 'PYR', 'cellModel': 'HH'}, 
                                            'connFunc': 'fullConn','weight': 0.005, 'synMech': 'syn1', 'sec': 'soma', 'loc': 1.0, 'delay': 0}


# Connectivity parameters
netParams.connParams['PYR->PYR'] = {
    'preConds': {'cellType': 'PYR'}, 'postConds': {'cellType': 'PYR'},
    'weight': 0.0,                    # weight of each connection
    'delay': '0.2+gauss(13.0,1.4)',     # delay min=0.2, mean=13.0, var = 1.4
    'threshold': 10,                    # threshold
    'convergence': 'uniform(0,5)',       # convergence (num presyn targeting postsyn) is uniformly distributed between 1 and 10
    'synMech': 'syn1'}    




###############################################################################
# SIMULATION PARAMETERS
###############################################################################

# Simulation parameters
simConfig.duration = 1*1e3 # Duration of the simulation, in ms
simConfig.dt = 0.005 # Internal integration timestep to use
simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.createNEURONObj = True  # create HOC objects when instantiating network
simConfig.createPyStruct = True  # create Python structure (simulator-independent) when instantiating network
simConfig.timing = True  # show timing  and save to file
simConfig.verbose = False # show detailed messages 


# Recording 
simConfig.recordCells = ['all']  # list of cells to record from 
simConfig.recordTraces = {'V':{'sec':'soma','loc':0.5,'var':'v'}, 
    'u':{'sec':'soma', 'pointp':'Izhi', 'var':'u'}, 
    'I':{'sec':'soma', 'pointp':'Izhi', 'var':'i'}, 
    'AMPA_g': {'sec':'soma', 'loc':0.5, 'synMech':'AMPA', 'var':'g'},
    'AMPA_i': {'sec':'soma', 'loc':0.5, 'synMech':'AMPA', 'var':'i'}}
simConfig.recordStim = True  # record spikes of cell stims
simConfig.recordStep = simConfig.dt # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
simConfig.filename = 'mpiHybridTut'  # Set file output name
simConfig.saveFileStep = simConfig.dt # step size in ms to save data to disk
simConfig.savePickle = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveJson = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveMat = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveTxt = False # save spikes and conn to txt file
simConfig.saveDpk = False # save to a .dpk pickled file
simConfig.saveDat = True


# Analysis and plotting 
simConfig.analysis['plotRaster'] = {'orderInverse': False} #True # Whether or not to plot a raster
simConfig.analysis['plotTraces'] = {'include': [1,51]} # plot recorded traces for this list of cells
simConfig.analysis['plotRatePSD'] = {'include': ['allCells', 'PYR_HH', 'PYR_Izhi'], 'Fs': 200, 'smooth': 10} # plot recorded traces for this list of cells

