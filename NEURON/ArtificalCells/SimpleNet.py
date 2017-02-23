import neuron

import time

h = neuron.h
h.load_file("stdlib.hoc")

h.load_file("stdgui.hoc")

h("objref p")
h("p = new PythonObject()")

ns = 'NetStim'

#hPointp = getattr(h, ns)()
h('objectvar nst')
h('nst = new NetStim()')
h.nst.noise = 0.5
h.nst.number = 100


h('objectvar ac1')
h('ac1 = new acSyn100()')

h('create soma0, soma1, soma2, pre0')

h('soma0 { insert pas }')
h('objectvar syn_0')
h('soma0 {syn_0 = new syn1(0.5)} ')

h('soma1 { insert pas }')
h('objectvar syn_1')
h('soma1 {syn_1 = new syn1(0.5)} ')

h('soma2 { insert pas }')
h('objectvar syn_2')
h('soma2 {syn_2 = new syn1(0.5)} ')

h(" objectvar pf100 ")
h('pre0 { pf100 = new poissonFiringSyn100(0.5) }')

h('objectvar nc0')
h('nc0 = new NetCon(nst,syn_0)')
h('nc0.weight = 1')

h('objectvar nc1')
h('nc1 = new NetCon(pf100,syn_1)')
h('nc1.weight = 1')

h('objectvar nc2')
h('nc2 = new NetCon(ac1,syn_2)')
h('nc2.weight = 1')

h('forall psection()')

h.tstop = 300

h.dt = 0.025

h.steps_per_ms = 1/h.dt

d1 = h.Graph(0)
d1.size(0,h.tstop,-72,10)
d1.view(0, -72, h.tstop, 10, 80, 330, 330, 250)
h.graphList[0].append(d1)
# Line, plotting: E_net/0/IF_curr_alpha_E_net/v
d1.addexpr("soma0.v", "soma0.v", 1, 1, 0.8, 0.9, 2)
d1.addexpr("soma1.v", "soma1.v", 2, 1, 0.8, 0.9, 2)
d1.addexpr("soma2.v", "soma2.v", 3, 1, 0.8, 0.9, 2)

d2 = h.Graph(0)
d2.size(0,h.tstop,-80.0,50.0)
d2.view(0, -10, h.tstop, 30, 80, 330, 330, 250)
h.graphList[0].append(d2)
# Line, plotting: E_net/0/IF_curr_alpha_E_net/v
d2.addexpr("poissonFiringSyn100[0].tsince", "poissonFiringSyn100[0].tsince", 1, 1, 0.8, 0.9, 2)



print('Running for %s (dt=%s)'%(h.tstop,h.dt))
h.run()

print('Done')