import random

from .spn import *
from .spn_io import *
from .RNGFactory import *

SIMULATION_TIME = 0

def reset_state(spn: SPN):
    None

def set_firing_time(transition: Transition):
    """Sets the firing time of a transition based on the transition type and distribution"""
    if transition.t_type == "I":
        transition.firing_time = 0.0
        transition.enabled_at = SIMULATION_TIME
    elif transition.t_type == "T" and transition.distribution == "EXP":
        transition.firing_time = get_delay("EXP", lmbda = transition.dist_par1)
    elif transition.t_type == "T" and transition.distribution == "DET":
        transition.firing_time = get_delay("DET", delay= transition.dist_par1)

def is_enabled(transition: Transition):
    """Checks wheter a transition is currently enabled"""
    input_arcs = transition.input_arcs
    inhibitor_arcs = transition.inhibitor_arcs
    
    arc: InhibitorArc
    for arc in inhibitor_arcs:
        if arc.from_place.n_tokens > 0:
            print("inhibitor arc is blocking transition: " + transition.label)
            return False

    arc: InputArc
    for arc in input_arcs:
        if arc.from_place.n_tokens > 0:
            continue
        else:
            print("not enough tokens to enable transition: " + transition.label)
            return False
    return True

def update_enabled_flag(spn: SPN):
    """Updates the enabled flag for all transitions in a SPN"""
    transition: Transition
    for transition in spn.transitions:
        if is_enabled(transition) == True:
            transition.enabled = True
            transition.enabled_at = SIMULATION_TIME
            set_firing_time(transition)
        else:
            continue

def fire_transition(transition: Transition):
    "Fires a transition"
    output_arcs = transition.output_arcs
    input_arcs = transition.input_arcs

    arc: OutputArc
    for arc in output_arcs:
        place = arc.to_place
        place.add_n_tokens(1)
        place.time_changed = SIMULATION_TIME
    
    arc: InputArc
    for arc in input_arcs:
        place = arc.from_place
        place.remove_n_tokens(1)
        place.time_changed = SIMULATION_TIME

    transition.n_times_fired += 1
    transition.reset()

def find_next_firing(spn: SPN):
    "Finds the next transition that need to be fired based on min(firing times)"
    firing_times = {}
    transition: Transition
    for transition in spn.get_transitions():
        if transition.enabled == False:
            continue
        else:
            firing_times[transition] = transition.firing_time
    return random.choice([t for t in firing_times if firing_times[t] == min(firing_times.values())])   #random choice in case there are two ore more transitions fulfilling min() condition        


def process_next_event(spn: SPN):

    global SIMULATION_TIME

    next_transition: Transition
    next_transition = find_next_firing(spn)
    
    SIMULATION_TIME = SIMULATION_TIME + next_transition.firing_time

    fire_transition(next_transition)

    print("\n")
    print("Transition "+ next_transition.label + "fires at time " + str(SIMULATION_TIME))
    
    print_marking(spn,SIMULATION_TIME)

    update_enabled_flag(spn)

def simulate(spn: SPN, max_time: int, verbosity: int, protocol: bool):
    
    global SIMULATION_TIME

    if verbosity > 0:
        print("Starting simulation...")
        print("Simulation time limit = {}".format(max_time))
    
    reset_state(spn)

    if verbosity > 1:
        print_marking(spn,SIMULATION_TIME)
    
    update_enabled_flag(spn)
    
    print_state(spn,SIMULATION_TIME)
    while SIMULATION_TIME < max_time:
        process_next_event(spn)

    print_marking(spn,SIMULATION_TIME)
    print_state(spn,SIMULATION_TIME)

    print_statistics(spn,SIMULATION_TIME)