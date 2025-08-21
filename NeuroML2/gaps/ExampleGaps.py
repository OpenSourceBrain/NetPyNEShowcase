from neuromllite import Network, Cell, InputSource, Population, Synapse
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id="Example_GapJunctions")
net.notes = "Example: testing gap junctions..."

net.seed = 123
net.temperature = 32

net.parameters = {"N": 3, "weightInput": 1}

cell = Cell(id="pascell", neuroml2_source_file="pas.cell.nml")
net.cells.append(cell)


input_source = InputSource(id='iclamp0',
                           pynn_input='DCSource',
                           parameters={'amplitude':0.1, 'start':100., 'stop':200.})

net.input_sources.append(input_source)


pop_pre = Population(
    id="PopPre",
    size="1",
    component=cell.id,
    properties={"color": ".7 0 0"},
)
pop_post = Population(
    id="PopPost",
    size="N",
    component=cell.id,
    properties={"color": "0 0 .7"},
)

net.populations.append(pop_pre)
net.populations.append(pop_post)

net.synapses.append(
    Synapse(id="gj", neuroml2_source_file="gj.synapse.nml")
)


net.projections.append(
    Projection(
        id="projGJ",
        type="electricalProjection",
        presynaptic=pop_pre.id,
        postsynaptic=pop_post.id,
        synapse="gj",
        weight=1,
        random_connectivity=RandomConnectivity(probability=1),
    )
)


net.inputs.append(
    Input(
        id="stim",
        input_source=input_source.id,
        population=pop_pre.id,
        percentage=100,
        weight="weightInput",
    )
)

print(net)
print(net.to_json())
new_file = net.to_json_file("%s.json" % net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(
    id="SimExampleGJ",
    network=new_file,
    duration="300",
    seed="1111",
    dt="0.025",
    record_traces={"all": "*"},
)

sim.to_json_file()


################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)
