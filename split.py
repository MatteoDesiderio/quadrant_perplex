#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:34:44 2022

@author: matteo
"""

import numpy as np
from quadralizer import  Quadrant
import os
import shutil

project_names = ["primRef", "HzXu08", "BsXu08"][:1]
components = [["MGO", "FEO", "SIO2", ""], # the last empty one is to end 
              (),
              ()]
mass_amounts = [["32", "14", "60"],
                (),
                ()]
models = [["C2/c", "Wus", "Pv", "O", "Wad", "Ring", "Opx", "Aki", "Ppv", ""],
          (),
          ()]

Trange = [300, 4000]
Prange = [1, 1400000]


subdivisions = 2

_n = subdivisions + 1

T, P = np.linspace(*Trange, _n), np.linspace(*Prange, _n)
T_pairs = []
P_pairs = []
for i_t, _ in enumerate(T):
    try:
        T_pairs.append([T[i_t], T[i_t + 1]])
    except IndexError:
        pass
    
for i_p, _ in enumerate(P):
    try:
        P_pairs.append([P[i_p], P[i_p + 1]])
    except IndexError:
        pass

squares = []
for _tpair in T_pairs:
    tpair = "%.1f"%_tpair[0], "%.1f"%_tpair[1] 
    for _ppair in P_pairs:
        ppair = "%.1f"%_ppair[0], "%.1f"%_ppair[1] 
        squares.append([tpair, ppair])

for _nm, c, a, m in zip(project_names, components, mass_amounts, models):
    os.mkdir(_nm)
    cwd = os.getcwd() + "/"
    os.symlink(cwd + "vertex", cwd + _nm + "/vertex")
    os.symlink(cwd + "build", cwd + _nm + "/build")
    os.chdir(_nm)
    for isq, square in enumerate(squares):
        tmin, tmax = square[0]
        pmin, pmax = square[1]
        nm = _nm + "_quadrant%i"%isq
        q = Quadrant(name=nm, components=c,
                     MinT=tmin, MaxT=tmax,
                     MinP=pmin, MaxP=pmax,   
                     amounts=a, models=m)
        ob, eb = q.build()
        ov, ev = q.vertex()
    os.chdir("../")
        
