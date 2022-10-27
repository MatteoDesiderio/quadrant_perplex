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
project_names = [ argv[1].replace(".txt", "") ]
# these parameters are read from a file
components, mass_amounts, models = ParamReader.read(argv[1])

components = [components]
mass_amounts = [mass_amounts]
models = [models] 
print(components)
print(mass_amounts)
print(models)

# The overall limits of the computation domain
Trange = [300, 4000] # K
Prange = [1, 1400000] # bar
# How many sectors along each axis
subdivisions = int(argv[2])
# how many parallel processes

# %% initialize
# collect squares in the PT domain
squares = create_squares(Trange, Prange, subdivisions)

create_paths(project_names, subdivisions)

# %%
proj_quadrants = initialize_quadrants(project_names, components, 
                                      mass_amounts, models, squares)

# %% Build
_ = prepare(proj_quadrants, project_names, "build")

# %% Vertex
_ = prepare(proj_quadrants, project_names, "vertex")

# %% Werami
_ = prepare(proj_quadrants, project_names, "werami")

