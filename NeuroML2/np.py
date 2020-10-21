
'''
    The main function that's called by the NetPyNE loader, i.e.
    
        from np import load_netpyne
        netParams, simConfig = load_netpyne()
    
    That functionality should fail if this method is missing or doesn't 
    return 2 dict like objects
'''
def load_netpyne():

    nml2_file_name = 'HHCellNetwork.net.nml'
    from netpyne import sim    # import netpyne sim module
    from netpyne import specs
    
    simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration
    netParams = sim.importNeuroML2(nml2_file_name, simConfig, simulate=False, analyze=True, returnNetParams =True)


    return netParams, simConfig


'''
    Not necessary to have this here, just a useful way to serialise the model
'''
def save_as_json(filename):
    netParams, simConfig = load_netpyne()
    
    info = {'netParams':netParams.__dict__,
            'simConfig':simConfig.__dict__}
            
    from netpyne.sim.save import saveJSON
    saveJSON(filename, info)
    
    print('Saved netParams and simConfig to file: %s'%filename)
   
    
'''
    This obviously wouldn't be called with: from np import load_netpyne
'''
if __name__ == "__main__":
    save_as_json('./HHSim.json')


