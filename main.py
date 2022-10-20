from spn_simulator.spn import *
from spn_simulator.spn_simulate import simulate
from spn_simulator.spn_io import print_petri_net
from spn_simulator.spn_visualization import *

spn = SPN()

p1 = Place("Queue",0)
p2 = Place("Server",0)

t1 = Transition("TArrive","T")
t1.set_distribution("EXP", 0.1, 0.0)
#t1.set_distribution("DET",1,0)
t2 = Transition("TApproach","I")
t3 = Transition("TService","T")
t3.set_distribution("EXP", 0.11, 0.0)
#t3.set_distribution("DET",1,0)

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


simulate(spn, max_time = 10, verbosity = 1, protocol = True)

#print_petri_net(spn)
draw_spn(spn, show=False)