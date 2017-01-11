'''
Generates a NeuroML 2 file with many types of cells, populations and inputs
for testing purposes
'''

import opencortex.build as oc
import sys


min_pop_size = 3

def scale_pop_size(baseline, scale):
    return max(min_pop_size, int(baseline*scale))



def generate(reference = "Balanced",
             scalePops = 1,
             scalex=1,
             scaley=1,
             scalez=1,
             connections=True,
             connections_scaling=1,
             duration = 1000,
             global_delay = 0,
             max_in_pop_to_plot_and_save = 5,
             gen_spike_saves_for_all_somas = True,
             format='xml'):

    num_exc = scale_pop_size(80,scalePops)
    num_inh = scale_pop_size(40,scalePops)
    
    if scalePops!=1:
        reference += '_%s'%scalePops
    
    nml_doc, network = oc.generate_network(reference)

    oc.add_cell_and_channels(nml_doc, 'AllenInstituteCellTypesDB_HH/HH_464198958.cell.nml','HH_464198958')
    oc.add_cell_and_channels(nml_doc, 'AllenInstituteCellTypesDB_HH/HH_471141261.cell.nml','HH_471141261')
    
    xDim = 400*scalex
    yDim = 500*scaley
    zDim = 300*scalez

    xs = -200
    ys = -150
    zs = 100

    #####   Synapses

    synAmpa1 = oc.add_exp_two_syn(nml_doc, id="synAmpa1", gbase="1nS",
                             erev="0mV", tau_rise="0.5ms", tau_decay="5ms")

    synGaba1 = oc.add_exp_two_syn(nml_doc, id="synGaba1", gbase="2nS",
                             erev="-80mV", tau_rise="1ms", tau_decay="20ms")

    #####   Input types


    pfs1 = oc.add_poisson_firing_synapse(nml_doc,
                                       id="psf1",
                                       average_rate="150 Hz",
                                       synapse_id=synAmpa1.id)


    #####   Populations

    popExc = oc.add_population_in_rectangular_region(network,
                                                  'popExc',
                                                  'HH_464198958',
                                                  num_exc,
                                                  xs,ys,zs,
                                                  xDim,yDim,zDim)

    popInh = oc.add_population_in_rectangular_region(network,
                                                  'popInh',
                                                  'HH_471141261',
                                                  num_inh,
                                                  xs,ys,zs,
                                                  xDim,yDim,zDim)


    #####   Projections

    total_conns = 0
    if connections:
        proj = oc.add_probabilistic_projection(network, "proj0",
                                        popExc, popExc,
                                        synAmpa1.id, connections_scaling*0.3, delay = global_delay)
        total_conns += len(proj.connection_wds)

        proj = oc.add_probabilistic_projection(network, "proj1",
                                        popExc, popInh,
                                        synAmpa1.id, connections_scaling*0.5, delay = global_delay)
        total_conns += len(proj.connection_wds)

        proj = oc.add_probabilistic_projection(network, "proj3",
                                        popInh, popExc,
                                        synGaba1.id, connections_scaling*0.7, delay = global_delay)
        total_conns += len(proj.connection_wds)

        proj = oc.add_probabilistic_projection(network, "proj4",
                                        popInh, popInh,
                                        synGaba1.id, connections_scaling*0.5, delay = global_delay)
        total_conns += len(proj.connection_wds)


    #####   Inputs

    oc.add_inputs_to_population(network, "Stim0",
                                popExc, pfs1.id,
                                all_cells=True)



    #####   Save NeuroML and LEMS Simulation files      
    

    nml_file_name = '%s.net.%s'%(network.id,'nml.h5' if format == 'hdf5' else 'nml')
    oc.save_network(nml_doc, 
                    nml_file_name, 
                    validate=(format=='xml'),
                    format = format)

    if format=='xml':
        
        plot_v = {popExc.id:[],popInh.id:[]}
        save_v = {'%s_v.dat'%popExc.id:[],'%s_v.dat'%popInh.id:[]}
        
        for i in range(min(max_in_pop_to_plot_and_save,num_exc)):
            plot_v[popExc.id].append("%s/%i/%s/v"%(popExc.id,i,popExc.component))
            save_v['%s_v.dat'%popExc.id].append("%s/%i/%s/v"%(popExc.id,i,popExc.component))
            
        for i in range(min(max_in_pop_to_plot_and_save,num_inh)):
            plot_v[popInh.id].append("%s/%i/%s/v"%(popInh.id,i,popInh.component))
            save_v['%s_v.dat'%popInh.id].append("%s/%i/%s/v"%(popInh.id,i,popInh.component))
            
        lems_file_name = oc.generate_lems_simulation(nml_doc, network, 
                                nml_file_name, 
                                duration =      duration, 
                                dt =            0.025,
                                gen_plots_for_all_v = False,
                                gen_plots_for_quantities = plot_v,
                                gen_saves_for_all_v = False,
                                gen_saves_for_quantities = save_v,
                                gen_spike_saves_for_all_somas = gen_spike_saves_for_all_somas)
    else:
        lems_file_name = None
                                
    return nml_doc, nml_file_name, lems_file_name
                               

if __name__ == '__main__':
    
    if '-all' in sys.argv:
        
        for format in ['xml','hdf5']:

            generate(format=format)

            generate(scalePops = 10,
                 scalex=2,
                 scalez=2,
                 connections_scaling=0.002,
                 gen_spike_saves_for_all_somas = False,
                 format=format)
        
             
             
    elif '-test' in sys.argv:
        
        generate(num_bbp =0,
             scalePops = 0.2,
             scalex=2,
             scalez=2,
             duration = 200,
             max_in_pop_to_plot_and_save = 3,
             global_delay = 2)
    else:
        generate()