TITLE Mod file for component: Component(id=iaf type=iafCell)

COMMENT

    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.7.2
         org.neuroml.model   v1.7.2
         jLEMS               v0.10.4

ENDCOMMENT

NEURON {
    POINT_PROCESS iaf
    
    
    NONSPECIFIC_CURRENT i                    : To ensure v of section follows v_I
    RANGE leakConductance                   : parameter
    RANGE leakReversal                      : parameter
    RANGE thresh                            : parameter
    RANGE reset                             : parameter
    RANGE C                                 : parameter
    
    RANGE iSyn                              : exposure
    
    RANGE iMemb                             : exposure
    
    RANGE copy_v                           : copy of v on section
    
}

UNITS {
    
    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (A) = (amp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (kHz) = (kilohertz)
    (mM) = (millimolar)
    (um) = (micrometer)
    (umol) = (micromole)
    (S) = (siemens)
    
}

PARAMETER {
    
    leakConductance = 2.0E-4 (uS)
    leakReversal = -70 (mV)
    thresh = -55 (mV)
    reset = -70 (mV)
    C = 3.2E-6 (microfarads)
}

ASSIGNED {
    v (mV)
    i (mA/cm2)
    
    copy_v (mV)
    
    v_I (nA) 
    
    iSyn (nA)                              : derived variable
    
    iMemb (nA)                             : derived variable
    rate_v (mV/ms)
    
}

STATE {
    
}

INITIAL {
    rates()
    rates() ? To ensure correct initialisation.
    
    net_send(0, 1) : go to NET_RECEIVE block, flag 1, for initial state
    
}

BREAKPOINT {
    
    rates()
    
    copy_v = v
    i = v_I * C
}

NET_RECEIVE(flag) {
    
    if (flag == 1) { : Setting watch for top level OnCondition...
        WATCH (v >  thresh) 1000
    }
    if (flag == 1000) {
    
        v = reset
    
        v_I = 0 : Setting rate of change of v to 0
    }
    if (flag == 1) { : Set initial states
    
        v = leakReversal
    }
    
}

PROCEDURE rates() {
    
    ? DerivedVariable is based on path: synapses[*]/i, on: Component(id=iaf type=iafCell), from synapses; null
    iSyn = 0 ? Was: synapses[*]_i but insertion of currents from external attachments not yet supported ? path based, prefix = 
    
    iMemb = leakConductance  * (  leakReversal   - v) +  iSyn ? evaluable
    rate_v = iMemb  /  C ? Note units of all quantities used here need to be consistent!
    
    v_I = -1 * rate_v
     
    
}

