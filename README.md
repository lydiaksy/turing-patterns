# Original fork

This repository contains the notebook and code for [my blogpost](http://www.degeneratestate.org/posts/2017/May/05/turing-patterns/) on Turing-Patterns. 

# README for TwoDimensionalRDEquations Simulation

## Introduction
This README provides instructions on how to set up and run the TwoDimensionalRDEquations simulation. The simulation models two-dimensional reaction-diffusion equations, allowing users to explore various parameters' effects on the system's evolution.

## Prerequisites
- Python 3.x
- Pip (Python package installer)
- Virtual Environment (recommended)

## Setup
### 1. Virtual Environment Setup
It's a good practice to use a virtual environment to manage dependencies for your Python project. To set up a virtual environment:

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS and Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Once your virtual environment is activated, install the required Python packages:

```bash
pip install numpy matplotlib click scipy
```

## Usage
The script can be run from the command line with several options to customize the parameters of the simulation.

### Running the Simulation
Execute the script with optional parameters:

```bash
python generate_pattern.py --da [Da value] --db [Db value] --alpha [alpha value] --beta [beta value] --steps [number of steps] --output [output file name] --gif [boolean]
```

### Parameters
- `--da`: Diffusion coefficient for A. Default is 1.
- `--db`: Diffusion coefficient for B. Default is 100.
- `--alpha`: Alpha parameter. Default is -0.005.
- `--beta`: Beta parameter. Default is 10.
- `--steps`: Number of steps in the simulation. Default is 150.
- `--output`: Name of the output file to save the plot. Default is "image".
- `--gif`: Produce a gif.

### Example
To run the simulation with the default parameters and save the output as "result.png" and generate a gif "result.gif":

```bash
python generate_pattern.py --output result --gif true
```

## Deactivating Virtual Environment
After running the simulation, you can deactivate the virtual environment:

```bash
deactivate
```

