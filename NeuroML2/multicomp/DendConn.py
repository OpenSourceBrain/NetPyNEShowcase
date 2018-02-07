import opencortex.core as oc
import sys

'''
Simple network using cells from ACNet model

'''


def generate(reference = "DendConn",
             num_pyr = 4,
             num_bask = 0,
             scalex=1,
             scaley=1,
             scalez=1,
             connections=True,
             global_delay = 0,
             duration = 500,
             segments_to_plot_record = {'pop_pyr':[0],'pop_bask':[0]},
             format='xml'):


    nml_doc, network = oc.generate_network(reference)

    oc.include_opencortex_cell(nml_doc, 'acnet2/pyr_4_sym.cell.nml')
    oc.include_opencortex_cell(nml_doc, 'acnet2/bask.cell.nml')
    
    xDim = 500*scalex
    yDim = 50*scaley
    zDim = 500*scalez

    pop_pyr = oc.add_population_in_rectangular_region(network, 'pop_pyr',
                                                  'pyr_4_sym', num_pyr,
                                                  0,0,0, xDim,yDim,zDim)

    pop_bask = oc.add_population_in_rectangular_region(network, 'pop_bask',
                                                  'bask', num_bask,
                                                  0,yDim,0, xDim,yDim+yDim,zDim)
                   
    ampa_syn = oc.add_exp_two_syn(nml_doc, id="AMPA_syn", 
                             gbase="30e-9S", erev="0mV",
                             tau_rise="0.003s", tau_decay="0.0031s")


    pg = oc.add_pulse_generator(nml_doc,
                           id="pg0",
                           delay="10ms",
                           duration="300ms",
                           amplitude="0.7nA")          
                                
    total_conns = 0
    if connections:

        this_syn=ampa_syn.id
        proj = oc.add_targeted_projection(network,
                                        "Proj_pyr_pyr",
                                        pop_pyr,
                                        pop_pyr,
                                        targeting_mode='convergent',
                                        synapse_list=[this_syn],
                                        pre_segment_group = 'soma_group',
                                        post_segment_group = 'dendrite_group',
                                        number_conns_per_cell=1,
                                        delays_dict = {this_syn:global_delay})
        if proj:                           
            total_conns += len(proj[0].connection_wds)


            
            
    oc.add_targeted_inputs_to_population(network, "Stim0",
                                pop_pyr, pg.id, 
                                segment_group='soma_group',
                                number_per_cell = 1,
                                all_cells=False,
                                only_cells=[0])
        
    
        
    nml_file_name = '%s.net.%s'%(network.id,'nml.h5' if format == 'hdf5' else 'nml')
    target_dir = 'HDF5/' if format == 'hdf5' else './'
    
    oc.save_network(nml_doc, 
                    nml_file_name, 
                    validate=(format=='xml'),
                    format = format,
                    target_dir=target_dir)


    gen_plots_for_quantities = {}   #  Dict with displays vs lists of quantity paths
    gen_saves_for_quantities = {}   #  Dict with file names vs lists of quantity paths

    for pop in segments_to_plot_record.keys():
        pop_nml = network.get_by_id(pop)
        if pop_nml is not None and pop_nml.size>0:

            group = len(segments_to_plot_record[pop]) == 1
            if group:
                display = 'Display_%s_v'%(pop)
                file_ = 'Sim_%s.%s.v.dat'%(nml_doc.id,pop)
                gen_plots_for_quantities[display] = []
                gen_saves_for_quantities[file_] = []

            for i in range(int(pop_nml.size)):
                if not group:
                    display = 'Display_%s_%i_v'%(pop,i)
                    file_ = 'Sim_%s.%s.%i.v.dat'%(nml_doc.id,pop,i)
                    gen_plots_for_quantities[display] = []
                    gen_saves_for_quantities[file_] = []

                for seg in segments_to_plot_record[pop]:
                    quantity = '%s/%i/%s/%i/v'%(pop,i,pop_nml.component,seg)
                    gen_plots_for_quantities[display].append(quantity)
                    gen_saves_for_quantities[file_].append(quantity)

    lems_file_name = oc.generate_lems_simulation(nml_doc, 
                            network, 
                            target_dir+nml_file_name, 
                            duration =      duration, 
                            dt =            0.025,
                            gen_plots_for_all_v = False,
                            gen_plots_for_quantities = gen_plots_for_quantities,
                            gen_saves_for_all_v = False,
                            gen_saves_for_quantities = gen_saves_for_quantities,
                            target_dir=target_dir)
                                
    return nml_doc, nml_file_name, lems_file_name


if __name__ == '__main__':
    
    generate(global_delay = 5)
