"""
params.py

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

Contributors: salvadordura@gmail.com
"""

from netpyne import specs

description = "HH TUTORIAL. Please specify the size of the network before running"

parameters = {'size':{'default':3,
                      'min':1,
                      'description':'The size of the network'}}

simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration


###############################################################################
#
# MPI HH TUTORIAL PARAMS
#
###############################################################################

###############################################################################
# NETWORK PARAMETERS
###############################################################################

def generate_netParams(*argv):

    netParams = specs.NetParams()   # object of class NetParams to store the network parameters
    pop_size = 3 if not 'size' in argv else argv['size']

    # Population parameters
    netParams.popParams['PYR'] = {'cellModel': 'HH', 'cellType': 'PYR', 'numCells': pop_size} # add dict with params for this pop


    # Cell parameters
    ## PYR cell properties
    cellRule = {'conds': {'cellModel': 'HH', 'cellType': 'PYR'},  'secs': {}} 	# cell rule dict
    cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}  														# soma params dict
    cellRule['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0, 'cm': 1}  			     		# soma geometry
    cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}  		# soma hh mechanism
    cellRule['secs']['soma']['vinit'] = -71
    netParams.cellParams['PYR'] = cellRule  												# add dict to list of cell params

    # Synaptic mechanism parameters
    netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 1.0, 'e': 0}


    # Stimulation parameters
    netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0, 'start': 50}
    netParams.stimTargetParams['bkg->PYR1'] = {'source': 'bkg', 'conds': {'pop': 'PYR'}, 'weight': 0.1, 'delay': 'uniform(5,15)'}
    #netParams.stimTargetParams['bkg->PYR1'] = {'source': 'bkg', 'conds': {'pop': 'PYR'}, 'weight': 0.1, 'delay': '0'}


    # Connectivity parameters
    netParams.connParams['PYR->PYR'] = {
        'preConds': {'pop': 'PYR'}, 'postConds': {'pop': 'PYR'},
        'weight': 0.002,                    # weight of each connection
        'delay': '0.2+normal(13.0,1.4)',     # delay min=0.2, mean=13.0, var = 1.4
        'threshold': 10,                    # threshold
        'convergence': pop_size-1}    # convergence (num presyn targeting postsyn) is uniformly distributed between 1 and 15

    return netParams


###############################################################################
# SIMULATION PARAMETERS
###############################################################################

# Simulation parameters
simConfig.duration = 300 # Duration of the simulation, in ms
simConfig.dt = 0.0025 # Internal integration timestep to use
simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.createNEURONObj = 1  # create HOC objects when instantiating network
simConfig.createPyStruct = 1  # create Python structure (simulator-independent) when instantiating network
simConfig.verbose = False  # show detailed messages

# Recording
simConfig.recordCells = ['all']  # which cells to record from
simConfig.recordTraces = {'Vsoma':{'sec':'soma','loc':0.5,'var':'v'}}
simConfig.recordStim = True  # record spikes of cell stims
simConfig.recordStep = simConfig.dt # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
simConfig.filename = 'HHTut'  # Set file output name
simConfig.saveFileStep = simConfig.dt # step size in ms to save data to disk
simConfig.savePickle = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveDat = True # save traces

simConfig.saveJson = True # save traces

# Analysis and plotting
simConfig.analysis['plotRaster'] = True  # Plot raster
simConfig.analysis['plotTraces'] = {'include': [2]}  # Plot raster
simConfig.analysis['plot2Dnet'] = True  # Plot 2D net cells and connections

simConfig.validateNetParams=True

cfg = simConfig
netParams = generate_netParams(None)