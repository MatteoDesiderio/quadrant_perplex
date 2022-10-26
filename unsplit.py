#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 17:34:34 2022

@author: matteo
"""
from utils import *
from quadralizer import Quadrant, Assembler, ParamReader
import os
from math import sqrt
from sys import argv


project_names = [ argv[1].replace(".txt", "") ]


# %% Join the separate results of the 
filt = lambda d : "quadrant" in d
for nm in project_names:
    dirs = os.listdir(nm)
    dirs = filter(filt, dirs)
    subdivisions = max([int(d.replace("quadrant", "")) for d in dirs]) + 1
    subdivisions = int(sqrt(subdivisions))
    
    # initialize class to stitch every thing together
    ass = Assembler(nm, subdivisions)#
    # assemble everything together (return different stages, if u like)
    parts, joined, stitched = ass.assemble()
    # export the result as one single neat tab file
    ass.export_tab()
