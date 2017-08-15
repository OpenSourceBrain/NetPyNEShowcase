'''
Generates a NeuroML 2 file with many types of cells, populations and inputs
for testing purposes
'''

import opencortex.core as oc
import sys

from random import random

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
             global_delay = 2,
             max_in_pop_to_plot_and_save = 5,
             gen_spike_saves_for_all_somas = True,
             deterministic = True,
             format='xml'):

    num_exc = scale_pop_size(80,scalePops)
    num_inh = scale_pop_size(40,scalePops)
    
    if scalePops!=1:
        reference += '_%s'%scalePops
    
    nml_doc, network = oc.generate_network(reference)
    
    oc.include_opencortex_cell(nml_doc, 'AllenInstituteCellTypesDB_HH/HH_477127614.cell.nml')
    oc.include_opencortex_cell(nml_doc, 'AllenInstituteCellTypesDB_HH/HH_476686112.cell.nml')
    
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

    if not deterministic:
        pfs1 = oc.add_poisson_firing_synapse(nml_doc,
                                           id="psf1",
                                           average_rate="150 Hz",
                                           synapse_id=synAmpa1.id)



    #####   Populations

    popExc = oc.add_population_in_rectangular_region(network,
                                                  'popExc',
                                                  'HH_477127614',
                                                  num_exc,
                                                  xs,ys,zs,
                                                  xDim,yDim,zDim)

    popInh = oc.add_population_in_rectangular_region(network,
                                                  'popInh',
                                                  'HH_476686112',
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

    if not deterministic:
        oc.add_inputs_to_population(network, "Stim0",
                                popExc, pfs1.id,
                                all_cells=True)
                                
    else:

        for i in range(num_exc):

            pg = oc.add_pulse_generator(nml_doc,
                                   id="pg_%i"%i,
                                   delay="0ms",
                                   duration="10000ms",
                                   amplitude="%snA"%(random()*0.5))

            oc.add_inputs_to_population(network, "Stim_%i"%i,
                                    popExc, pg.id,
                                    all_cells=False,
                                    only_cells=[i])
                               



    #####   Save NeuroML and LEMS Simulation files      
    

    nml_file_name = '%s%s.net.%s'%('XH_' if format == 'xml_hdf5' else '', network.id,'nml.h5' if format == 'hdf5' else 'nml')
    
    oc.save_network(nml_doc, 
                    nml_file_name, 
                    validate=(format=='xml'),
                    format = format)


    plot_v = {popExc.id:[],popInh.id:[]}
    save_v = {'%s_v.dat'%popExc.id:[],'%s_v.dat'%popInh.id:[]}

    for i in range(min(max_in_pop_to_plot_and_save,num_exc)):
        plot_v[popExc.id].append("%s/%i/%s/v"%(popExc.id,i,popExc.component))
        save_v['%s_v.dat'%popExc.id].append("%s/%i/%s/v"%(popExc.id,i,popExc.component))

    for i in range(min(max_in_pop_to_plot_and_save,num_inh)):
        plot_v[popInh.id].append("%s/%i/%s/v"%(popInh.id,i,popInh.component))
        save_v['%s_v.dat'%popInh.id].append("%s/%i/%s/v"%(popInh.id,i,popInh.component))
        
    lems_file_name = "LEMS_%s.xml"%network.id
    if format != 'xml':
        lems_file_name = "LEMS_%s_%s.xml"%(network.id,format)
        

    lems_file_name = oc.generate_lems_simulation(nml_doc, network, 
                            nml_file_name, 
                            duration =      duration, 
                            dt =            0.025,
                            gen_plots_for_all_v = False,
                            gen_plots_for_quantities = plot_v,
                            gen_saves_for_all_v = False,
                            gen_saves_for_quantities = save_v,
                            gen_spike_saves_for_all_somas = gen_spike_saves_for_all_somas,
                            lems_file_name = lems_file_name)
                                
    return nml_doc, nml_file_name, lems_file_name
                               

if __name__ == '__main__':
    
    if '-all' in sys.argv:
        
        for format in ['xml','hdf5']:

            generate(format=format)
            
            generate(scalePops = .2,
                 scalex=1,
                 scalez=1,
                 connections_scaling=0.1,
                 gen_spike_saves_for_all_somas = False,
                 global_delay = 5,
                 format=format)

            generate(scalePops = 10,
                 scalex=2,
                 scalez=2,
                 connections_scaling=0.2,
                 gen_spike_saves_for_all_somas = False,
                 global_delay = 5,
                 deterministic = False,
                 format=format)
            
            if format == 'hdf5':
                generate(scalePops = 33,
                     scalex=6,
                     scalez=6,
                     duration = 100,
                     connections_scaling=0.2,
                     gen_spike_saves_for_all_somas = False,
                     global_delay = 5,
                     deterministic = False,
                     format=format)
            '''
            if format == 'hdf5':
                generate(scalePops = 100,
                     scalex=6,
                     scalez=6,
                     connections_scaling=0.2,
                     gen_spike_saves_for_all_somas = False,
                     global_delay = 5,
                     format=format)'''
        
             
             
    elif '-test' in sys.argv:
        
        import logging
        logging.basicConfig(level=logging.INFO, format="%(name)-19s %(levelname)-5s - %(message)s")
        
        for format in ['xml','hdf5']:
            generate(scalePops = .2,
                 scalex=1,
                 scalez=1,
                 connections_scaling=0.1,
                 gen_spike_saves_for_all_somas = False,
                 global_delay = 5,
                 format=format)
    else:
        generate()