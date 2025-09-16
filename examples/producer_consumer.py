import sys
sys.path.append('../pyspn')

from components.spn import *
from components.spn_simulate import simulate
from components.spn_io import print_petri_net
from components.spn_visualization import *

spn = SPN()

p1 = Place("Producing",1)
p2 = Place("Produced",0)
p3 = Place("BusyBuffers",0)
p4 = Place("FreeBuffers",2)
p5 = Place("Consuming",1)
p6 = Place("Consumed",0)


t1 = Transition("Produce","T")
t1.set_distribution("expon", a=0.0, b=1.0/1.0)
#t1.set_distribution("det",1)
t2 = Transition("Fill","I")
t3 = Transition("Remove","I")
t4 = Transition("Consume","T")
t4.set_distribution("expon", a=0.0, b=1.0/1.0)
#t3.set_distribution("det",1)

spn.add_place(p1)
spn.add_place(p2)
spn.add_place(p3)
spn.add_place(p4)
spn.add_place(p5)
spn.add_place(p6)

spn.add_transition(t1)
spn.add_transition(t2)
spn.add_transition(t3)
spn.add_transition(t4)

spn.add_input_arc(p1,t1)
spn.add_output_arc(t1,p2)
spn.add_input_arc(p2,t2)
spn.add_output_arc(t2,p1)
spn.add_output_arc(t2,p3)
spn.add_input_arc(p3,t3)
spn.add_output_arc(t3,p4)
spn.add_input_arc(p4,t2)
spn.add_output_arc(t3,p5)
spn.add_input_arc(p5,t4)
spn.add_output_arc(t4,p6)
spn.add_input_arc(p6,t3)

simulate(spn, max_time = 100, verbosity = 1, protocol = True, event_log= False)

#print_petri_net(spn)
draw_spn(spn, show=True, rankdir="LR")
