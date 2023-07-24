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
git clone https://github.com/jo-chr/pyspn.git  # 1. Clone repository
pip install -r requirements.txt  # 2. Install requirements
python3 examples/one_server.py  # 4. Run single-server queue example
```

## Modeling

Find sample SPN in `one_server.py`. Currently, places, timed transitions (t_type = "T"), immediate transitions (t_type = "I"), output arcs, input arcs, inhibitor arcs, and guard functions are supported.

### Transitions

For immediate transitions, you can set the transition weight.

For timed transitions, some of the supported distributions are:

| Distribution           | Parameter      |
|------------------------|----------------|
| Deterministic ("det")  | `a`            |
| Exponential ("expon")  | `a`, `b`       |
| Normal ("norm")        | `a`, `b`       |
| Lognormal ("lognorm")  | `a`, `b`, `c`  |
| Uniform ("uniform")    | `a`, `b`       |
| Triangular ("triang")  | `a`, `b`, `c`  |
| Weibull ("weibull_min")| `a`, `b`, `c`  |

More distributions can be easily implemented in `RNGFactory.py`. See [Scipy's documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) for detials regarding the distribtuions and their parameters.

### Export & Import of SPNs

Export and import SPNs as pickle files using `export()` and `import()` functions of `spn_io` module

## Simulation

Simulate the SPN as shown in `one_server.py`. The simulation protocol capturing the place markings can be found under `output/protocol/`.

## Visualization

Visualize the SPN as shown in `one_server.py`. The graph can be found under `output/graphs/`.

## Usage & Attribution

contact jofr@mmmi.sdu.dk


 
