<p align="center">
    <img src="https://img.shields.io/badge/contributions-welcome!-green" alt="Contributions welcome!"/>
    <img src="https://img.shields.io/github/last-commit/jo-chr/spn-simulator?color=blue">
</p>

# PySPN

A lightweight tool for modeling and simulation of Stochastic Petri Nets (SPNs).

## Getting Started

:information_source: *Tested with Python 3.11*

### via git

```bash
git clone https://github.com/jo-chr/pyspn.git  # 1. Clone repository
pip install -r requirements.txt  # 2. Install requirements
python3 examples/one_server.py  # 3. Run single-server queue example
```

## Modeling

Formally, the class of SPNs that can be modeled using *PySPN* is defined as:

$$SPN = (P, T, A, G, m_0)$$

where:

* $P = \{P_1,P_2,..,P_m\}$ is the set of places, drawn as circles;
* $T = \{T_1,T_2,..,T_n\}$ is the set of transitions along with their distribution functions or weights, drawn as bars;
* $A = A^I \cup A^O \cup A^H$ is the set of arcs, where $A^O$ is the set of output arcs, $A^I$ is the set of input arcs and $A^H$ is the set of inhibitor arcs and each of the arcs has a multiplicity assigned to it;
* $G = \{g_1,g_2,..,g_r\}$ is the set of guard functions which are associated with different transitions;
* and $m_0$ is the initial marking, defining the distribution of tokens in the places.

Each transition is represented as $T_i = (type, F)$, where $type \in \{timed,immediate\}$ indicates the type of the transition, and $F$ is either a probability distribution function if the corresponding transition is timed, or a firing weight or probability if it is immediate. 

Find sample SPNs under `examples/`. Currently, places, timed transitions (t\_type = "T"), immediate transitions (t\_type = "I"), output arcs, input arcs, inhibitor arcs, guard functions, and memory policies are supported.

### Places

A place with its required arguments is defined like so:
```bash
p1 = Place(label="Place 1", n_tokens=0)
```

### Transitions

A timed transition with its required arguments and a sample distribution function is defined like so:
```bash
t1 = Transition(label="Transition 1", t_type="T")
t1.set_distribution(distribution="expon", a=0.0, b=1.0/1.0)
```

An immediate transition with its required arguments and a sample weight is defined like so:
```bash
t2 = Transition(label="Transition 2", t_type="I")
t2.set_weight(weight=0.8)
```

For timed transitions, some of the supported distributions are:

| Distribution           | Parameter        |
|------------------------|------------------|
| Deterministic ("det")  | `a` (fixed delay)|
| Exponential ("expon")  | `a`, `b`         |
| Normal ("norm")        | `a`, `b`         |
| Lognormal ("lognorm")  | `a`, `b`, `c`    |
| Uniform ("uniform")    | `a`, `b`         |
| Triangular ("triang")  | `a`, `b`, `c`    |
| Weibull ("weibull_min")| `a`, `b`, `c`    |

More distributions can be easily implemented in `RNGFactory.py`. See [Scipy's documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) for details regarding the distributions and their parameters.

### Guard Functions for Transitions

Guard functions are defined like so:
```bash
def guard_t1():
    if len(p1.n_tokens) >= 2:
        return True
    else: return False
t1.set_guard_function(guard_t1)
```

### Memory Policies for Timed Transitions

The default setting is Race Enable ("ENABLE").

The memory policy can be set during instantiation
```bash
t1 = Transition(label="Transition_1",t_type="T",memory_policy="AGE")
```
or by using a function call
```bash
t1.set_memory_policy("AGE")
```

### Join  and Fork Transitions
To configure a transition that joins two or more input places, set the "Join" parameter to True. 
This indicates that the transition will act upon the confluence of tokens from multiple places.
```bash
t1 = Transition(label="", t_type="", Join=True)
```
Similarly, to set up a transition that splits its output to multiple places, utilize the "Fork" parameter. 
Setting split to True designates that the transition's output will be distributed to several output places.
```bash
t1 = Transition(label="", t_type="", Fork=True)
```

## Export & Import of SPNs

Export and import SPNs as [pickle](https://docs.python.org/3/library/pickle.html) files using the `export_spn()` and `import_spn()` functions of `spn_io` module.

## Simulation

Simulate a SPN like so:
```bash
simulate(spn, max_time = 100, verbosity = 2, protocol = True)
```

For the verbosity there are 3 levels of what is printed in the terminal:
 
* 0: No information;
* 1: Only final simulation statistics;
* 2: Initial markings, firing of transitions, and final statistics;  
* 3: Initial markings, firing of transitions and the resulting marking and state, and final statistics.

The simulation protocol capturing the markings throughtout the simulation can be found under `output/protocol/`.

## Visualization

Visualize a SPN like so:
```bash
draw_spn(spn, show=False, file="sample_spn", rankdir="LR")
```
The graph can be found under `output/graphs/`. 

## Usage & Attribution

If you are using the tool for a scientific project please consider citing our [publication](https://www.researchgate.net/publication/375758652_PySPN_An_Extendable_Python_Library_for_Modeling_Simulation_of_Stochastic_Petri_Nets):

    # EAI SIMUtools 2023 - 15th EAI International Conference on Simulation Tools and Techniques (preprint, accepted for presentation)
    @misc{friederich_2023,
        doi = {10.13140/RG.2.2.25334.16967},
        url = {https://www.researchgate.net/publication/375758652_PySPN_An_Extendable_Python_Library_for_Modeling_Simulation_of_Stochastic_Petri_Nets},
        year = 2023,
        month = {Nov},
        author = {Friederich, Jonas and Lazarova-Molnar, Sanja},
        title = {{PySPN}: An Extendable Python Library for Modeling & Simulation of Stochastic Petri Nets},
        conference = {EAI SIMUtools 2023 - 15th EAI International Conference on Simulation Tools and Techniques},
        note = {preprint}
    } 

For questions/feedback feel free to contact me: jofr@mmmi.sdu.dk.


 
