


class SPN(object):

    def __init__(self) -> None:
        self.places = []
        self.transitions = []
        return None

    def get_places(self):
        return self.places.copy()

    def get_transitions(self):
        return self.transitions.copy()

    def add_place(self, place):            
        self.places.append(place)

    def add_transition(self, transition):
        self.transitions.append(transition)

    def add_input_arc(self, place, transition, multiplicity = 1):
        arc = InputArc()
        arc.from_place = place
        arc.to_transition = transition
        arc.multiplicity = multiplicity
        transition.input_arcs.append(arc)

    def add_inhibitor_arc(self, transition, place, multiplicity = 1):
        arc = InhibitorArc()
        arc.to_transition = transition
        arc.from_place = place
        arc.multiplicity = multiplicity
        transition.inhibitor_arcs.append(arc)

    def add_output_arc(self, transition, place, multiplicity = 1):
        arc = OutputArc()
        arc.from_transition = transition
        arc.to_place = place
        arc.multiplicity = multiplicity
        transition.output_arcs.append(arc)
        

class Place(object):

    def __init__(self, label: str, n_tokens: int) -> None:
        self.label = label
        self.n_tokens = n_tokens
        self.max_tokens = 0
        self.time_changed = 0
        self.total_tokens = 0
        self.time_non_empty = 0
    
    def add_n_tokens(self, n_tokens):
        self.n_tokens += n_tokens
        if self.n_tokens > self.max_tokens:
            self.max_tokens = self.n_tokens
        self.total_tokens += n_tokens

    def remove_n_tokens(self, n_tokens):
        self.n_tokens -= n_tokens


class Transition(object):
    def __init__(self, label: str, t_type: str) -> None:
        self.label = label
        self.t_type = t_type
        self.distribution = None
        self.dist_par1 = 0
        self.dist_par2 = 0
        self.guard_function = None
        self.memory_policy = None
        self.clock_active = False

        self.enabled = False
        self.enabled_at = 0
        self.firing_time = 0

        self.time_enabled = 0
        self.n_times_fired = 0

        self.input_arcs = []
        self.output_arcs = []
        self.inhibitor_arcs = []

    def set_distribution(self, distribution: str, parameter1, parameter2):
        self.distribution = distribution
        self.dist_par1 = parameter1
        self.dist_par2 = parameter2
    
    def reset(self):
        self.enabled = False
        self.firing_time = 0
        self.enabled_at = 0


class InputArc(object):
    def __init__(self) -> None:
        self.to_transition = None
        self.from_place = None
        self.multiplicity = 0

class InhibitorArc(object):
    def __init__(self) -> None:
        self.to_transition = None
        self.from_place = None
        self.multiplicity = 0

class OutputArc(object):
    def __init__(self) -> None:
        self.to_place = None
        self.from_transition = None
        self.multiplicity = 0


        


def print_input_arc(input_arc: InputArc):
    place = input_arc.from_place
    transition = input_arc.to_transition
    print("Input arc from place " + place.label + " to transition " + transition.label)

def print_output_arc(output_arc: OutputArc):
    transition = output_arc.from_transition
    place = output_arc.to_place
    print("Output arc from transition " + transition.label + " to place " + place.label)

def print_inhibitor_arc(inhibitor_arc: InhibitorArc):
    place = inhibitor_arc.from_place
    transition = inhibitor_arc.to_transition    
    print("Inhibitor arc from place " + place.label + " to transition " + transition.label)


        





