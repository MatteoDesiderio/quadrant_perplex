#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:34:44 2022

@author: matteo
"""

from utils import *
from quadralizer import Quadrant, Assembler, ParamReader
import os
from sys import argv

#%% User defined inputs
# Name of the projects
try:
    project_name = argv[2].replace(".txt", "")
except IndexError:
    raise ValueError("Specify Project Name (xyz.txt) ")
        
# these parameters are read from a file
inputs = ParamReader.read(project_name + ".txt")

_ = [print(i, "-->" , inputs[i]) for i in inputs]

perplexVersion = inputs["perplexVersion"]
database = inputs["database"]
solution_model = inputs["solution_model"]
components = inputs["components"] 
mass_amounts = inputs["mass_amounts"]
models = inputs["models"]

# The overall limits of the computation domain
Trange = [300, 4000] # K
Prange = [1, 1400000] # bar
# How many sectors along each axis, i.e. parallel processes
try:    
    subdivisions = int(argv[2])
except IndexError:
    print("Will use 2 subdivisions")
    subdivisions = 2

# %% initialize
# collect squares in the PT domain
squares = create_squares(Trange, Prange, subdivisions)

create_paths(project_name, subdivisions, database, solution_model)

# %%
proj_quadrants = initialize_quadrants(project_name, **inputs, squares=squares)

# %% Build
_ = prepare(proj_quadrants, project_name, "build") 

# %% Vertex
_ = prepare(proj_quadrants, project_name, "vertex")

# %% Werami
_ = prepare(proj_quadrants, project_name, "werami")

