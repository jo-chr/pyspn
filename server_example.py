from spn_simulator.spn import *
from spn_simulator.spn_simulate import simulate
from spn_simulator.spn_io import print_petri_net
from spn_simulator.spn_visualization import *

spn = SPN()

p1 = Place(label="Queue", n_tokens=0)
p2 = Place(label="Server", n_tokens=0)

t1 = Transition(label="TArrive", t_type="T")
t1.set_distribution(distribution="EXP", parameter1=1.0, parameter2=0.0)
t2 = Transition(label="TApproach", t_type="I")
t2.set_weight(weight=1)
t3 = Transition(label="TService", t_type="T")
t3.set_distribution(distribution="EXP", parameter1=0.9, parameter2=0.0)

spn.add_place(p1)
spn.add_place(p2)

spn.add_transition(t1)
spn.add_transition(t2)
spn.add_transition(t3)

spn.add_output_arc(t1,p1)
spn.add_input_arc(p1,t2)
spn.add_output_arc(t2,p2)
spn.add_input_arc(p2,t3)
spn.add_inhibitor_arc(t2,p2)

simulate(spn, max_time = 100, verbosity = 3, protocol = True)

#print_petri_net(spn)
draw_spn(spn, show=False)