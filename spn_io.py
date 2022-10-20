from spn import SPN, Place, Transition

def print_petri_net(spn: SPN):
    return None


def print_marking(spn: SPN, simulation_time):
    print("\n")
    print("Marking at time " + str(simulation_time))
    for place in spn.get_places():
        print("Place " + place.label + ", #tokens: " + str(place.n_tokens))

def print_state(spn: SPN, simulation_time):
    print("\n")
    print("State at time " + str(simulation_time))
    place:Place
    for place in spn.get_places():
        print("Place " + place.label)
        print(" NTokens: " + str(place.n_tokens))
        print(" Last changed: " + str(place.time_changed))
        print(" Total tokens: " + str(place.total_tokens))
        print(" Time not empty: " + str(place.time_non_empty))
    
    transition:Transition
    for transition in spn.get_transitions():
        print("Transtion " + transition.label)
        if transition.enabled == True:
            print(" Enabled: True")
            print("     Enabled at: " + str(transition.enabled_at))
            print("     Firing time: " + str(transition.firing_time))
        else:
            print(" Enabled: False")

def print_statistics(spn: SPN, simulation_time):

    print("\nPetri Net Statistics: \n\n")
    transition:Transition
    for transition in spn.get_transitions():
        print("Transition {} :\n".format(transition.label))
        print(" Mean firing rate:    {}".format(transition.n_times_fired/simulation_time))
        print(" Number of firings:   {}".format(transition.n_times_fired))
        print(" P(Enabled):          {}\n".format(transition.time_enabled/simulation_time))
    
    place:Place
    for place in spn.get_places():
        print("Place {} :\n".format(place.label))
        print(" P(Not Empty):        {}".format(place.time_non_empty/simulation_time))
        #print(" Mean #tokens:        {}".format(place.total_tokens/simulation_time))
        print(" Max #tokens:         {}".format(place.max_tokens))
        print(" Curr #tokens:        {}\n".format(place.n_tokens))        

