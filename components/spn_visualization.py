from graphviz import Digraph

from .spn import *

def draw_spn(spn: SPN, file="spn_default", show=True, print_place_labels=False, rankdir="TB"):

    if rankdir == "TB":
        spn_graph = Digraph(engine="dot")
    else:
        spn_graph = Digraph(engine="dot", graph_attr={'rankdir':'LR'})

    # draw places and marking
    place:Place
    # Draw places and marking
    for place in spn.places:
        token_count = len(place.tokens)  # Get the count of tokens from the tokens list

        if token_count == 0:
            if print_place_labels:
                spn_graph.node(place.label, shape="circle", label="", xlabel=place.label, height="0.6", width="0.6",
                               fixedsize='true')
            else:
                spn_graph.node(place.label, shape="circle", label="", height="0.6", width="0.6", fixedsize='true')
        else:
            if token_count < 5:
                lb = "<"
                for token_number in range(1, token_count + 1):
                    lb += "&#9679;"
                    if token_number % 2 == 0:
                        lb += "<br/>"
                lb += ">"
            else:
                lb = f"{token_count}"

            if print_place_labels:
                spn_graph.node(place.label, shape='circle', label=lb, xlabel=place.label, height='0.6', width='0.6',
                               fixedsize='true')
            else:
                spn_graph.node(place.label, shape='circle', label=lb, height='0.6', width='0.6', fixedsize='true')

    # draw transitions
    transition:Transition
    for transition in spn.transitions:
        if transition.t_type == "T":
            if rankdir == "TB":
                spn_graph.node(transition.label, shape='rectangle', color='black', label='', xlabel=transition.label + "\n" + str(list(transition.distribution.keys())[0]), height='0.2', width='0.6', fixedsize='true')
            else:
                spn_graph.node(transition.label, shape='rectangle', color='black', label='', xlabel=transition.label + "\n" + str(list(transition.distribution.keys())[0]), height='0.6', width='0.2', fixedsize='true')
        else:
            if rankdir == "TB":
                spn_graph.node(transition.label, shape='rectangle', style='filled', color='black', label='', xlabel=transition.label + "\n" + str(transition.weight), height='0.2', width='0.6', fixedsize='true')
            else:
                spn_graph.node(transition.label, shape='rectangle', style='filled', color='black', label='', xlabel=transition.label + "\n" + str(transition.weight), height='0.6', width='0.2', fixedsize='true')

        input_arc:InputArc
        for input_arc in transition.input_arcs:
            if input_arc.multiplicity > 1:
                spn_graph.edge(input_arc.from_place.label, input_arc.to_transition.label, xlabel=str(input_arc.multiplicity))
            else: spn_graph.edge(input_arc.from_place.label, input_arc.to_transition.label)
        
        output_arc:OutputArc
        for output_arc in transition.output_arcs:
            if output_arc.multiplicity > 1:
                spn_graph.edge(output_arc.from_transition.label, output_arc.to_place.label, xlabel=str(output_arc.multiplicity))
            else: spn_graph.edge(output_arc.from_transition.label, output_arc.to_place.label)

        inhibitor_arc:InhibitorArc
        for inhibitor_arc in transition.inhibitor_arcs:
            if inhibitor_arc.multiplicity > 1:
                spn_graph.edge(
                    inhibitor_arc.from_place.label,
                    inhibitor_arc.to_transition.label,
                    xlabel=str(inhibitor_arc.multiplicity),
                    arrowhead="odot",
                    color="black"
                )
            else:
                spn_graph.edge(
                    inhibitor_arc.from_place.label,
                    inhibitor_arc.to_transition.label,
                    arrowhead="odot",
                    color="black"
                )

    spn_graph.render('../output/graphs/{}.gv'.format(file), view=show)

    return spn_graph
