from components.spn import *
from components.spn_simulate import simulate
from components.spn_io import print_petri_net
from components.spn_visualization import *

spn = SPN()

p1 = Place(label="Queue", n_tokens=0)
p2 = Place(label="Server", n_tokens=0)

t1 = Transition(label="TArrive", t_type="T")
t1.set_distribution(distribution="expon", a=0.0, b=1.0/1.0)
t2 = Transition(label="TApproach", t_type="I")
t2.set_weight(weight=1)
t3 = Transition(label="TService", t_type="T")
t3.set_distribution(distribution="expon", a=0.0, b=1.0/1.1)

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

#simulate(spn, max_time = 100, verbosity = 2, protocol = True)

#print_petri_net(spn)
draw_spn(spn, show=False)