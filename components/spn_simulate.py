import random
import os

from .spn import *
from .spn_io import *
from .RNGFactory import *

SIMULATION_TIME = 0
SIMULATION_TIME_UNIT = None
VERBOSITY = 0
PROTOCOL = False
SCHEDULE_ITERATOR = 0

def reset_state(spn: SPN):
    for place in spn.places:
        place:Place
        place.time_changed = 0
        place.total_tokens = 0
        place.time_non_empty = 0

def complete_statistics():
    None

def set_firing_time(transition: Transition):
    """Sets the firing time of a transition based on the transition type and distribution"""
    global SCHEDULE_ITERATOR

    transition.enabled_at = SIMULATION_TIME

    if transition.t_type == "I":
        transition.firing_delay = 0.0
    elif transition.t_type == "T":
        dist = list(transition.distribution.keys())[0]
        parameters = list(transition.distribution[dist].values())
        match dist:
            case "det":
                transition.firing_delay = get_delay("det", parameters[0])   
            case "uniform":
                transition.firing_delay = get_delay("uniform", parameters[0], parameters[1])
            case "expon":
                transition.firing_delay = get_delay("expon", parameters[0], parameters[1])
            case "norm":
                transition.firing_delay = get_delay("norm", parameters[0], parameters[1])
            case "lognorm":
                transition.firing_delay = get_delay("lognorm", parameters[0], parameters[1], parameters[2])
            case "triang":
                transition.firing_delay = get_delay("triang", parameters[0], parameters[1], parameters[2])
            case "cauchy":
                transition.firing_delay = get_delay("cauchy", parameters[0], parameters[1])
            case "exponpow":
                transition.firing_delay = get_delay("exponpow", parameters[0], parameters[1], parameters[2])
            case "gamma":
                transition.firing_delay = get_delay("gamma", parameters[0], parameters[1], parameters[2])
            case _:
                raise Exception("Distribution undefined for transition {}".format(transition))
    
    if transition.t_type == "T" and SIMULATION_TIME_UNIT != None:
        transition.firing_delay = convert_delay(transition.firing_delay, time_unit=transition.time_unit, simulation_time_unit=SIMULATION_TIME_UNIT)

    transition.firing_time = transition.enabled_at + transition.firing_delay

def set_reset_time(transition: Transition):
    transition.reset_time = transition.enabled_at + transition.reset_threshold

def convert_delay(delay, time_unit = None, simulation_time_unit = None):
    if time_unit == "d" and simulation_time_unit == "h":
        return delay * 24
    else:
        return delay

def is_enabled(transition: Transition):
    """Checks wheter a transition is currently enabled"""
    input_arcs = transition.input_arcs
    inhibitor_arcs = transition.inhibitor_arcs
    
    arc: InhibitorArc
    for arc in inhibitor_arcs:
        if arc.from_place.n_tokens >= arc.multiplicity:
            #print("inhibitor arc is blocking transition: " + transition.label)
            return False

    arc: InputArc
    for arc in input_arcs:
        if arc.from_place.n_tokens > 0:
            continue
        else:
            #print("not enough tokens to enable transition: " + transition.label)
            return False
    return True

def update_enabled_flag(spn: SPN):
    """Updates the enabled flag for all transitions in a SPN"""
    transition: Transition
    for transition in spn.transitions:
        if is_enabled(transition) == True:
            transition.enabled = True
            if transition.firing_time == 0:
                set_firing_time(transition)
            if transition.allow_reset == True and transition.reset_time == 0:
                set_reset_time(transition)
            else:
                continue
        else:
            transition.enabled = False
            if transition.t_type == "I":
                transition.reset()

def reset_transition(transition: Transition):
    set_firing_time(transition)
    set_reset_time(transition)

def fire_transition(transition: Transition):
    """Fires a transition"""
    output_arcs = transition.output_arcs
    input_arcs = transition.input_arcs

    oarc: OutputArc
    place: Place
    for oarc in output_arcs:
        place = oarc.to_place
        if place.n_tokens > 0:
            place.time_non_empty += SIMULATION_TIME - place.time_changed
        place.time_changed = SIMULATION_TIME
        place.add_n_tokens(1)            #needs to be changed based on multiplicity of arc
        if PROTOCOL == True:
            write_to_protocol(place.label,SIMULATION_TIME,place.n_tokens)
    
    iarc: InputArc
    for iarc in input_arcs:
        place = iarc.from_place
        if place.n_tokens > 0:
            place.time_non_empty += SIMULATION_TIME - place.time_changed
        place.time_changed = SIMULATION_TIME
        place.remove_n_tokens(1)        #needs to be changed based on multiplicity of arc
        if PROTOCOL == True:
            write_to_protocol(place.label,SIMULATION_TIME,place.n_tokens)

    transition.n_times_fired += 1
    transition.reset()

def find_next_resetting(spn: SPN):
    """Finds the next transition that need to be resetted based on min(resetting times)"""
    transition: Transition

    resetting_times = {}
    for transition in spn.transitions:
        if transition.enabled == True and transition.allow_reset == True:
            resetting_times[transition] = transition.reset_time
        else:
            continue    

    if not resetting_times:
        return None
    else:
        return random.choice([t for t in resetting_times if resetting_times[t] == min(resetting_times.values())])


def find_next_firing(spn: SPN):
    """Finds the next transition that need to be fired based on min(firing times)"""
    transition: Transition

    total_prob = 0
    inc_prob = 0
    for transition in spn.transitions:
        if transition.enabled == True and transition.t_type == "I":
            total_prob = total_prob + transition.weight
    
    if total_prob > 0:
        ran = random.uniform(0,total_prob)
        for transition in spn.transitions:
            if transition.enabled == True and transition.t_type == "I":
                inc_prob = inc_prob + transition.weight
                if inc_prob > ran:
                    return transition

    firing_times = {}
    for transition in spn.transitions:
        if transition.enabled == True:
            firing_times[transition] = transition.firing_time
        else:
            continue    
    return random.choice([t for t in firing_times if firing_times[t] == min(firing_times.values())])

def process_next_event(spn: SPN, max_time):

    global SIMULATION_TIME

    next_transition_reset: Transition
    next_transition: Transition
    next_transition_reset = find_next_resetting(spn)
    next_transition = find_next_firing(spn)

    if next_transition_reset == None:
        if next_transition.firing_time > max_time:
            SIMULATION_TIME = max_time
            return None     
        else:
            SIMULATION_TIME = next_transition.firing_time
    else:
        if next_transition.firing_time > max_time or next_transition_reset.reset_time > max_time:
            SIMULATION_TIME = max_time
            return None
        else:
            SIMULATION_TIME = min([next_transition.firing_time,next_transition_reset.reset_time])
    
    if next_transition_reset == None:
        fire_transition(next_transition)
        if VERBOSITY > 1:
            print("\nTransition {} fires at time {}".format(next_transition.label, round(SIMULATION_TIME,2)))
    else:
        if next_transition.firing_time < next_transition_reset.reset_time:
            fire_transition(next_transition)
            if VERBOSITY > 1:
                print("\nTransition {} fires at time {}".format(next_transition.label, round(SIMULATION_TIME,2)))
        else:
            reset_transition(next_transition_reset)
            if VERBOSITY > 1:
                print("\nTransition {} resets at time {}".format(next_transition_reset.label, round(SIMULATION_TIME,2)))
    
    if VERBOSITY > 2:
        print_marking(spn,SIMULATION_TIME)

    update_enabled_flag(spn)

def simulate(spn: SPN, max_time = 10, start_time = 0, time_unit = None, verbosity = 2, protocol = True):
    
    global SIMULATION_TIME, SIMULATION_TIME_UNIT, VERBOSITY, PROTOCOL, SCHEDULE_ITERATOR

    if start_time == 0:
        SIMULATION_TIME = 0
    else:
        SIMULATION_TIME = start_time
        max_time = max_time + start_time
    SIMULATION_TIME_UNIT = time_unit
    VERBOSITY = verbosity
    PROTOCOL = protocol
    SCHEDULE_ITERATOR = 0

    #clear protocol
    if protocol == True:
        with open(os.getcwd() + "/output/protocol/protocol.csv", "w", newline="") as protocol:
            writer = csv.writer(protocol)
            writer.writerow(["Place","Time","Marking"])


    if VERBOSITY > 0:
        print("Starting simulation...")
        print("Simulation time limit = {}".format(max_time))
    
    reset_state(spn)

    if VERBOSITY > 1:
        print_marking(spn,SIMULATION_TIME)
    
    update_enabled_flag(spn)
    
    if VERBOSITY > 1:
        print_state(spn,SIMULATION_TIME)
    
    while SIMULATION_TIME < max_time:
        process_next_event(spn, max_time)
        if verbosity > 2:
            print_state(spn,SIMULATION_TIME)

    if VERBOSITY > 0:
        print("\nTime: {}. Simulation terminated.\n".format(SIMULATION_TIME))

    complete_statistics()

    if VERBOSITY > 0:
        print_statistics(spn,SIMULATION_TIME)