from __future__ import annotations

class SPN(object):

    def __init__(self):
        self.places = []
        self.transitions = []

    def get_place_by_label(self, label: str):
        try:
            place: Place
            for place in self.places:
                if place.label == label:
                    return place
        except: print("No place found with specified label")
        
    def add_place(self, place: Place):            
        self.places.append(place)

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def add_input_arc(self, place: Place, transition: Transition, multiplicity = 1):
        arc = InputArc()
        arc.from_place = place
        arc.to_transition = transition
        arc.multiplicity = multiplicity
        transition.input_arcs.append(arc)
        place.input_arcs.append(arc)

    def add_inhibitor_arc(self, transition: Transition, place: Place, multiplicity = 1):
        arc = InhibitorArc()
        arc.to_transition = transition
        arc.from_place = place
        arc.multiplicity = multiplicity
        transition.inhibitor_arcs.append(arc)
        place.inhibitor_arcs.append(arc)

    def add_output_arc(self, transition: Transition, place: Place, multiplicity = 1):
        arc = OutputArc()
        arc.from_transition = transition
        arc.to_place = place
        arc.multiplicity = multiplicity
        transition.output_arcs.append(arc)
        place.output_arcs.append(arc)
        

class Place():

    def __init__(self, label: str, n_tokens: int):
        self.label = label
        self.n_tokens = n_tokens
        self.max_tokens = 0
        self.time_changed = 0
        self.total_tokens = 0
        self.time_non_empty = 0

        self.input_arcs = []
        self.output_arcs = []
        self.inhibitor_arcs = []
    
    def add_n_tokens(self, n_tokens: int):
        self.n_tokens += n_tokens
        if self.n_tokens > self.max_tokens:
            self.max_tokens = self.n_tokens
        self.total_tokens += n_tokens

    def remove_n_tokens(self, n_tokens: int):
        self.n_tokens -= n_tokens


class Transition(object):
    def __init__(self, label: str, t_type: str):
        self.label = label
        self.t_type = t_type

        if self.t_type == "T":
            self.distribution = None
            self.dist_par1 = 0
            self.dist_par2 = 0
        elif self.t_type == "I":
            self.weight = 0
        else: raise Exception("Not a valid transition type.")
        
        self.guard_function = None
        self.memory_policy = None
        self.clock_active = False

        self.enabled = False
        self.enabled_at = 0
        self.firing_delay = 0
        self.firing_time = 0

        self.time_enabled = 0
        self.n_times_fired = 0

        self.input_arcs = []
        self.output_arcs = []
        self.inhibitor_arcs = []

    def set_distribution(self, distribution: str, parameter1: float, parameter2: float):
        if self.t_type == "T":
            self.distribution = distribution
            self.dist_par1 = parameter1
            self.dist_par2 = parameter2
        else: raise Exception("Can not set distribution for immediate transition.")
    
    def set_weight(self, weight: float):
        if self.t_type == "I":
            self.weight = weight
        else: raise Exception("Can not set weight for timed transition.")

    def reset(self):
        self.enabled = False
        self.enabled_at = 0
        self.firing_delay = 0
        self.firing_time = 0


class InputArc(object):
    def __init__(self):
        self.to_transition = None
        self.from_place = None
        self.multiplicity = 0

class InhibitorArc(object):
    def __init__(self):
        self.to_transition = None
        self.from_place = None
        self.multiplicity = 0

class OutputArc(object):
    def __init__(self):
        self.to_place = None
        self.from_transition = None
        self.multiplicity = 0