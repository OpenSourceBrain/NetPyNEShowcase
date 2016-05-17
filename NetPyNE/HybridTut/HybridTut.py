"""
params.py 

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

Contributors: salvadordura@gmail.com
"""

netParams = {}  # dictionary to store sets of network parameters
simConfig = {}  # dictionary to store sets of simulation configurations


###############################################################################
#
# MPI HH TUTORIAL PARAMS
#
###############################################################################

###############################################################################
# NETWORK PARAMETERS
###############################################################################

# Population parameters
netParams['popParams'] = []  # create list of populations - each item will contain dict with pop params
netParams['popParams'].append({'popLabel': 'PYR_HH', 'cellModel': 'HH', 'cellType': 'PYR', 'numCells': 50}) # add dict with params for this pop 
netParams['popParams'].append({'popLabel': 'PYR_Izhi', 'cellModel': 'Izhi2007b', 'cellType': 'PYR', 'numCells': 50}) # add dict with params for this pop 
netParams['popParams'].append({'popLabel': 'background', 'cellModel': 'NetStim', 'rate': 10, 'noise': 0.5, 'source': 'random'})  # background inputs


# Cell parameters list
netParams['cellParams'] = []

## PYR cell properties (HH)
cellRule = {'label': 'PYR_HH', 'conditions': {'cellType': 'PYR', 'cellModel': 'HH'},  'sections': {}}

soma = {'geom': {}, 'topol': {}, 'mechs': {}}  # soma properties
soma['geom'] = {'diam': 6.3, 'L': 5, 'Ra': 123.0, 'pt3d':[]}
soma['geom']['pt3d'].append((0, 0, 0, 20))
soma['geom']['pt3d'].append((0, 0, 20, 20))
soma['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} 

dend = {'geom': {}, 'topol': {}, 'mechs': {}}  # dend properties
dend['geom'] = {'diam': 5.0, 'L': 150.0, 'Ra': 150.0, 'cm': 1, 'pt3d': []}
dend['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}
dend['mechs']['pas'] = {'g': 0.0000357, 'e': -70} 

cellRule['sections'] = {'soma': soma, 'dend': dend}  # add sections to dict
netParams['cellParams'].append(cellRule)  # add dict to list of cell properties

## PYR cell properties (Izhi)
cellRule = {'label': 'PYR_Izhi', 'conditions': {'cellType': 'PYR', 'cellModel': 'Izhi2007b'},  'sections': {}}

soma = {'geom': {}, 'pointps':{}}  # soma properties
soma['geom'] = {'diam': 6.3, 'L': 5, 'Ra': 123.0}
soma['pointps']['Izhi'] = {'_type':'Izhi2007b', 'C':100, 'k':0.7, 'vr':-60, 'vt':-40, 'vpeak':35, 'a':0.03, 'b':-2, 'c':-50, 'd':100, 'celltype':1}
cellRule['sections'] = {'soma': soma}  # add sections to dict
netParams['cellParams'].append(cellRule)  # add dict to list of cell properties


# Synaptic mechanism parameters
netParams['synMechParams'] = []
netParams['synMechParams'].append({'label': 'NMDA', 'mod': 'ExpSyn', 'tau': 0.1, 'e': 0})
 

# Connectivity parameters
netParams['connParams'] = []  

netParams['connParams'].append(
    {'preTags': {'cellType': 'PYR'}, 'postTags': {'cellType': 'PYR'},
    'weight': 0.004,                    # weight of each connection
    'delay': '0.2+gauss(13.0,1.4)',     # delay min=0.2, mean=13.0, var = 1.4
    'threshold': 10,                    # threshold
    'convergence': 'uniform(0,5)',       # convergence (num presyn targeting postsyn) is uniformly distributed between 1 and 10
    'synMech': 'NMDA'})    


netParams['connParams'].append(
    {'preTags': {'popLabel': 'background'}, 'postTags': {'cellType': 'PYR','cellModel': 'Izhi2007b'}, # background -> PYR (Izhi2007b)
    'connFunc': 'fullConn',
    'weight': 0.004, 
    'delay': 'uniform(1,5)',
    'synMech': 'NMDA'})  


netParams['connParams'].append(
    {'preTags': {'popLabel': 'background'}, 'postTags': {'cellType': 'PYR', 'cellModel': 'HH'}, # background -> PYR (HH)
    'connFunc': 'fullConn',
    'weight': 20, 
    'synMech': 'NMDA',
    'sec': 'dend',
    'loc': 1.0,
    'delay': 'uniform(1,5)'})  



###############################################################################
# SIMULATION PARAMETERS
###############################################################################

simConfig = {}  # dictionary to store simConfig

# Simulation parameters
simConfig['duration'] = 1*1e3 # Duration of the simulation, in ms
simConfig['dt'] = 0.025 # Internal integration timestep to use
simConfig['randseed'] = 1 # Random seed to use
simConfig['createNEURONObj'] = True  # create HOC objects when instantiating network
simConfig['createPyStruct'] = True  # create Python structure (simulator-independent) when instantiating network
simConfig['timing'] = True  # show timing  and save to file
simConfig['verbose'] = False # show detailed messages 


# Recording 
simConfig['recordCells'] = []  # list of cells to record from 
simConfig['recordTraces'] = {'V':{'sec':'soma','loc':0.5,'var':'v'}, 
    'u':{'sec':'soma', 'pointp':'Izhi', 'var':'u'}, 
    'I':{'sec':'soma', 'pointp':'Izhi', 'var':'i'}, 
    'NMDA_g': {'sec':'soma', 'loc':'0.5', 'synMech':'NMDA', 'var':'g'},
    'NMDA_i': {'sec':'soma', 'loc':'0.5', 'synMech':'NMDA', 'var':'i'}}
simConfig['recordStim'] = True  # record spikes of cell stims
simConfig['recordStep'] = 0.025 # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
simConfig['filename'] = 'mpiHybridTut'  # Set file output name
simConfig['saveFileStep'] = 1000 # step size in ms to save data to disk
simConfig['savePickle'] = False # Whether or not to write spikes etc. to a .mat file
simConfig['saveJson'] = False # Whether or not to write spikes etc. to a .mat file
simConfig['saveMat'] = False # Whether or not to write spikes etc. to a .mat file
simConfig['saveTxt'] = False # save spikes and conn to txt file
simConfig['saveDpk'] = False # save to a .dpk pickled file


# Analysis and plotting 
simConfig['plotRaster'] = True # Whether or not to plot a raster
simConfig['plotCells'] = [1,51] # plot recorded traces for this list of cells
simConfig['plotLFPSpectrum'] = False # plot power spectral density
simConfig['maxspikestoplot'] = 3e8 # Maximum number of spikes to plot
simConfig['plotConn'] = False # whether to plot conn matrix
simConfig['plotWeightChanges'] = False # whether to plot weight changes (shown in conn matrix)
simConfig['plot3dArch'] = False # plot 3d architecture

