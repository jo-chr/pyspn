from __future__ import annotations
import uuid
class SPN(object):

    def __init__(self):
        self.places = []
        self.transitions = []
        
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

    '''
    def get_current_marking(self):
        marking = {}
        for place in self.places:
            place:Place
            marking[place]=place.n_tokens
            return marking
    '''
    def get_place_by_label(self, label: str):
        try:
            place: Place
            for place in self.places:
                if place.label == label:
                    return place
        except: print("No place found with specified label.")

    def get_transition_by_label(self, label: str):
        try:
            transition: Transition
            for transition in self.transitions:
                if transition.label == label:
                    return transition
        except: print("No transition found with specified label.")

    def get_arrival_transitions(self):
        try:
            transition: Transition
            arrival_transitions = []
            for transition in self.transitions:
                if transition.input_arcs == []:
                    arrival_transitions.append(transition)
            return arrival_transitions
        except: print("Failed to find arrival transitions.")

        

class Place:

    def __init__(self, label: str, n_tokens: int):
        self.label = label
        self.n_tokens = n_tokens
        self.tokens = []

        # Generate initial tokens and ensure they are unique and use the global ID system
        for _ in range(n_tokens):
            self.tokens.append(Token())

        self.max_tokens = 0
        self.time_changed = 0
        self.total_tokens = 0
        self.time_non_empty = 0

        self.input_arcs = []
        self.output_arcs = []
        self.inhibitor_arcs = []

    def set_tokens(self, n_tokens: int):
        # Adjust the tokens list to the new number of tokens, handling both increases and decreases
        current_tokens = len(self.tokens)
        if n_tokens > current_tokens:
            # Add new tokens if the number has increased
            self.tokens.extend([str(uuid.uuid4()) for _ in range(n_tokens - current_tokens)])
        elif n_tokens < current_tokens:
            # Remove tokens if the number has decreased
            self.tokens = self.tokens[:n_tokens]

class Transition(object):

    def __init__(self, label: str, t_type: str, Join=0, Fork=0):
        self.label = label
        self.t_type = t_type

        if self.t_type == "T":
            self.distribution = None
            self.time_unit = None
        elif self.t_type == "I":
            self.weight = 1
        else: raise Exception("Not a valid transition type.")

        self.handicap = 1 #Handicap for experiments with new configurations; Handicap will influence firing times of transition; <1 -> transition fill fire faster; >1 -> transition will fire slower
        self.handicap_type = None
        self.allow_reset = False
        self.reset_threshold = 0 #Threshold; can be used e.g., for testing preventive maintenance with equipment failure transitions
        self.reset_time = 0

        self.guard_function = None
        self.memory_policy = "ENABLE"
        self.clock_active = False

        self.enabled = False
        self.enabled_at = 0
        self.disabled_at = 0
        self.disabled_time = 0
        self.firing_delay = 0
        self.firing_time = 0

        self.time_enabled = 0
        self.n_times_fired = 0

        self.input_arcs = []
        self.output_arcs = []
        self.inhibitor_arcs = []

        self.counter = 0
        self.Join = Join
        self.Fork=Fork

    def set_distribution(self, distribution, a=0.0, b=0.0, c=0.0, d=0.0, time_unit:str = None):
        if self.t_type == "T":
            self.distribution = {distribution:{"a":a,"b":b,"c":c,"d":d}}
            self.time_unit = time_unit
        else: raise Exception("Can not set distribution for immediate transition.")
    
    def set_weight(self, weight: float):
        if self.t_type == "I":
            self.weight = weight
        else: raise Exception("Can not set weight for timed transition.")

    def set_guard_function(self, guard_function):
        self.guard_function = guard_function

    def set_memory_policy(self, type):
        self.memory_policy = type

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


# Hypothetical Token class implementation
class Token:
    _id_counter = 0

    def __init__(self):
        type(self)._id_counter += 1
        self.id = type(self)._id_counter

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Token({self.id})"
