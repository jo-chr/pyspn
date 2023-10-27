import sys
sys.path.append('../pyspn')

from components.spn import *
from components.spn_simulate import simulate
from components.spn_io import print_petri_net
from components.spn_visualization import *

spn = SPN()

p1 = Place("Queue",0)
p2 = Place("Server1",0)
p3 = Place("Server2",0)

t1 = Transition("Arrive","T")
#t1.set_distribution("expon", a=0.0, b=1.0/1.0)
t1.set_distribution("det",1)
t2 = Transition("Approach_Server1","I")
t2.set_weight(0.5)
t3 = Transition("Approach_Server2","I")
t3.set_weight(0.5)
t4 = Transition("Service_Server1","T")
#t4.set_distribution("expon", a=0.0, b=1.0/0.9)
t4.set_distribution("det",2)
t5 = Transition("Service_Server2","T")
#t5.set_distribution("expon", a=0.0, b=1.0/0.9)
t5.set_distribution("det",1)

spn.add_place(p1)
spn.add_place(p2)
spn.add_place(p3)

spn.add_transition(t1)
spn.add_transition(t2)
spn.add_transition(t3)
spn.add_transition(t4)
spn.add_transition(t5)

spn.add_output_arc(t1,p1)
spn.add_input_arc(p1,t2)
spn.add_input_arc(p1,t3)
spn.add_output_arc(t2,p2)
spn.add_output_arc(t3,p3)
spn.add_input_arc(p2,t4)
spn.add_inhibitor_arc(t2,p2)
spn.add_input_arc(p3,t5)
spn.add_inhibitor_arc(t3,p3)


simulate(spn, max_time = 10, verbosity = 2, protocol = True)

#print_petri_net(spn)
draw_spn(spn, show=False)