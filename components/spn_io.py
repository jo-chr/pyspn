import csv
import os
import pickle

from .spn import *

def print_place(place: Place):
    print("Place {}\n".format(place.label))
    print(" NTokens: {}\n".format(place.n_tokens))

def print_transition(transition: Transition):
    print("Transition {}\n".format(transition.label))
    if transition.t_type == "I":
        print(" Immediate transition\n")
        #print(" P:  {}\n".format(transition.dist_par1))
    elif transition.distribution == "DET":
        print(" Distribution: Deterministic")
        print(" delay:  {}\n".format(transition.dist_par1))
    elif transition.distribution == "EXP":
        print(" Distribution: Exponential")
        print(" lambda: {}\n".format(transition.dist_par1))
    elif transition.distribution == "NORM":
        print(" Distribtution: Normal/Uniform")
        print(" a:  {}".format(transition.dist_par1))
        print(" b:  {}\n".format(transition.dist_par2))

def print_input_arc(input_arc: InputArc):
    place = input_arc.from_place
    transition = input_arc.to_transition
    print(" Input arc from place {} to transition {}".format(place.label,transition.label))

def print_output_arc(output_arc: OutputArc):
    transition = output_arc.from_transition
    place = output_arc.to_place
    print(" Output arc from transition {} to place {}".format(transition.label,place.label))

def print_inhibitor_arc(inhibitor_arc: InhibitorArc):
    place = inhibitor_arc.from_place
    transition = inhibitor_arc.to_transition    
    print(" Inhibitor arc from place {} to transition {}".format(place.label,transition.label))

def print_petri_net(spn: SPN):
    
    for place in spn.places:
        print_place(place)

    transition:Transition
    for transition in spn.transitions:
        print_transition(transition)
        for input_arc in transition.input_arcs:
            print_input_arc(input_arc)
        for output_arc in transition.output_arcs:
            print_output_arc(output_arc)
        for inhibitor_arc in transition.inhibitor_arcs:
            print_inhibitor_arc(inhibitor_arc)
        print("\n")


def print_marking(spn: SPN, simulation_time):
    print("\n")
    print("Marking at time {}".format(round(simulation_time,2)))
    for place in spn.places:
        print("Place {}, #tokens: {}".format(place.label,place.n_tokens))

def print_state(spn: SPN, simulation_time):
    print("\n")
    print("State at time " + str(round(simulation_time,2)))
    place:Place
    for place in spn.places:
        print("Place " + place.label)
        print(" NTokens: " + str(place.n_tokens))
        print(" Last changed: " + str(round(place.time_changed,2)))
        print(" Total tokens: " + str(place.total_tokens))
        print(" Time not empty: " + str(round(place.time_non_empty,2)))
    
    transition:Transition
    for transition in spn.transitions:
        print("Transtion " + transition.label)
        if transition.enabled == True:
            print(" Enabled: True")
            print("     Enabled at: " + str(round(transition.enabled_at,2)))
            print("     Firing delay: " + str(round(transition.firing_delay,2)))
            print("     Firing time: " + str(round(transition.firing_time,2)))
            if transition.allow_reset == True:
                print("     Reset time: " + str(round(transition.reset_time,2)))
        else:
            print(" Enabled: False")

def print_statistics(spn: SPN, simulation_time):

    print("\nPetri Net Statistics: \n\n")
    transition:Transition
    for transition in spn.transitions:
        print("Transition {} :\n".format(transition.label))
        print(" Mean firing rate:    {}".format(transition.n_times_fired/simulation_time))
        print(" Number of firings:   {}".format(transition.n_times_fired))
        print(" P(Enabled):          {}\n".format(transition.time_enabled/simulation_time))
    
    place:Place
    for place in spn.places:
        print("Place {} :\n".format(place.label))
        #print(" P(Not Empty):        {}".format(place.time_non_empty/simulation_time))
        #print(" Mean #tokens:        {}".format(place.total_tokens/simulation_time))
        print(" Max #tokens:         {}".format(place.max_tokens))
        print(" Curr #tokens:        {}".format(place.n_tokens))    
        print(" Time non empty:      {}\n".format(place.time_non_empty))

def write_to_protocol(place, simulation_time, n_tokens):
    # Ensure the directory exists
    # Assuming the current directory is 'output/protocols' and you want to create a file in 'output/protocols'
    try:
        file_path = os.path.join(os.getcwd(), "../output/protocols/protocol.csv")

        # Since you are already in 'output/protocols', no need to navigate the directory structure
        with open(file_path, "a", newline="") as protocol:
            writer = csv.writer(protocol)
            writer.writerow([place, str(round(simulation_time,2)), str(n_tokens)])
    except:
        with open(os.getcwd() + "/output/protocols/protocol.csv", "a", newline="") as protocol:
            writer = csv.writer(protocol)
            writer.writerow([place, str(round(simulation_time,2)), str(n_tokens)])

def write_to_event_log(simulation_time, token_ids, place):
    # Ensure the directory exists
    # Assuming the current directory is 'output/protocols' and you want to create a file in 'output/protocols'
    try:
        file_path = os.path.join(os.getcwd(), "../output/event_logs/event_log.csv")

        # Since you are already in 'output/protocols', no need to navigate the directory structure
        with open(file_path, "a", newline="") as protocol:
            writer = csv.writer(protocol)
            writer.writerow([str(round(simulation_time,2)), str(token_ids), place])
    except:
        with open(os.getcwd() + "/output/event_logs/event_log.csv", "a", newline="") as event_log:
            writer = csv.writer(event_log)
            writer.writerow([str(round(simulation_time,2)), str(token_ids), place])


def export_spn(spn: SPN, name = "default_spn.pkl"):
    with open(os.getcwd() + "/output/models/" + name, 'wb') as spn_file:
        pickle.dump(spn, spn_file)

def import_spn(path):
    with open(path, 'rb') as spn_file:
        return pickle.load(spn_file)
