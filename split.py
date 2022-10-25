#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:34:44 2022

@author: matteo
"""

from utils import *
from quadralizer import Quadrant, Assembler
import os

#%% User defined inputs
# Name of the projects
project_names = ["primRef", "HzXu08", "BsXu08"]

# Components of the system... 
components = [["MGO", "FEO", "SIO2", ""], # the last empty one is to end list
              ["CAO", "FEO", "MGO", "AL2O3", "SIO2", "NA2O", ""],
              ["CAO", "FEO", "MGO", "AL2O3", "SIO2", "NA2O", ""]]

# ...and their amount, in mass
mass_amounts = [["32.24", "14.37", "60.08"],
                ["0.89", "8.61", "45.72", "1.33", "43.45", "0.0"],
                ["12.61", "8.22", "9.76", "16.84", "50.39", "2.19"]]

# Solution models
models = [["C2/c", "Wus", "Pv", "O", "Wad", "Ring", "Opx", 
           "Aki", "Ppv", ""],
          ["Pl", "Sp", "O", "Wad", "Ring", "Opx", "Cpx", 
           "Pv", "Ppv", "CF", "C2/c", "Wus", "Aki", "Gt", ""],
          ["Pl", "Sp", "O", "Wad", "Ring", "Opx", "Cpx", 
           "Pv", "Ppv", "CF", "C2/c", "Wus", "Aki", "Gt", ""]]

# The overall limits of the computation domain
Trange = [300, 4000]
Prange = [1, 1400000]
# How many sectors along each axis
subdivisions = 2

# %% initialize
# collect squares in the PT domain
squares = create_squares(Trange, Prange, subdivisions)

create_paths(project_names, subdivisions)

proj_quadrants = initialize_quadrants(project_names, components, 
                                      mass_amounts, models, squares)

# %% Compute
_ = parallelize(proj_quadrants, project_names, "build")
_ = parallelize(proj_quadrants, project_names, "vertex")
proj_quadrants = parallelize(proj_quadrants, project_names, "werami")

# %% Join the separate results of the computation
for nm in project_names:
    # initialize class to stitch every thing together
    ass = Assembler(nm, subdivisions)#
    # assemble everything together (return different stages, if u like)
    parts, joined, stitched = ass.assemble()
    # export the result as one single neat tab file
    ass.export_tab()
