from spn import *
from spn_simulate import simulate

spn = SPN()

p1 = Place("Queue",0)
p2 = Place("Server",0)

t1 = Transition("TArrive","T")
t1.set_distribution("EXP", 0.1, 0.0)
t2 = Transition("TApproach","I")
t3 = Transition("TService","T")
t3.set_distribution("EXP", 0.11, 0.0)

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


#print(t2.inhibitor_arcs)
#print_input_arc(t2.input_arcs[0])
#print_output_arc(t1.output_arcs[0])
#print_inhibitor_arc(t2.inhibitor_arcs[0])

#print(spn)

simulate(spn, max_time = 2, verbosity = 0, protocol = True)