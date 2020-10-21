
'''
    The main function that's called by the NeytPyNE loader, i.e.
    
        from np import load_netpyne
        netParams, simConfig = load_netpyne()
    
    That functionality should fail if this method is missing or doesn't 
    return 2 dict like objects
'''
def load_netpyne(*argv):
    from HHSmall import simConfig, description, generate_netParams
    netParams = generate_netParams(argv)

    return netParams, simConfig, description

    
def get_model_parameters():
    
    from HHSmall import parameters
    return parameters

'''
    Not necessary to have this here, just a useful way to serialise the model
'''
def save_as_json(filename):
    netParams, simConfig, desc = load_netpyne()
    
    info = {'netParams':netParams.__dict__,
            'simConfig':simConfig.__dict__}
            
    from netpyne.sim.save import saveJSON
    saveJSON(filename, info)
    
    print('Saved netParams and simConfig to file: %s'%filename)
   
    
'''
    This obviously wouldn't be called with: from np import load_netpyne
'''
if __name__ == "__main__":
    save_as_json('./HHSmall.json')


