<p align="center">
    <img src="https://img.shields.io/badge/contributions-welcome!-green" alt="Contributions welcome!"/>
    <img src="https://img.shields.io/github/last-commit/jo-chr/spn-simulator?color=blue">
</p>

# SPN-Simulator

A lightweight tool for modeling and simulation of Stochastic Petri Nets (SPNs).

## Getting Started

:information_source: *Tested with Python 3.11*

### via git

```bash
git clone https://github.com/jo-chr/spn-simulator.git  # 1. Clone repository
pip install -r requirements.txt  # 2. Install requirements
python3 server_example.py  # 4. Run single-server queue example
```

## Modeling

Find example SPN in `server_example.py`. Currently, places, timed transitions (t_type = "T"), immediate transitions (t_type = "I"), output arcs, input arcs and inhibitor arcs are supported.

### Transitions

For immediate transitions, you can set the transition weight.

For timed transitions, the following distributions are currently supported:

| Distribution         | Parameter      | Transition parameter mapping in tool   |
|----------------------|----------------|----------------------------------------|
| Deterministic ("DET")| `delay`        | `parameter1 = delay`                   |
| Exponential ("EXP")  | `lambda`       | `parameter1 = lambda`                  |
| Normal ("NORM")      | `a`, `b`       | `parameter1 = a, parameter2 = b`       |
| Lognormal ("LOGN")   | `mean`, `sigma`| `parameter1 = mean, parameter2 = sigma`|
| Weibull ("WEIBULL")  | `a`, `lambda`  | `parameter1 = a, parameter2 = lambda`  |

More distributions can be easily implemented in `RNGFactory.py`.

### Export & Import of SPNs

Export and import SPNs as pickle files using `export()` and `import()` functions of `spn_io` module

## Simulation

Simulate the SPN as shown in `server_example.py`. The simulation protocol capturing the place markings can be found under `output/protocol/`.

## Visualization

Visualize the SPN as shown in `server_example.py`. The graph can be found under `output/graphs/`.

## Usage & Attribution

contact jofr@mmmi.sdu.dk


 
