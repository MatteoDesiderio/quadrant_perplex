#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:34:44 2022

@author: matteo
"""

from utils import create_squares, create_symlinks
from quadralizer import Quadrant, Assembler
import os

project_names = ["primRef", "HzXu08", "BsXu08"][:1]
components = [["MGO", "FEO", "SIO2", ""], # the last empty one is to end list
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
subdivisions = 3
squares = create_squares(Trange, Prange, subdivisions)

for _nm, c, a, m in zip(project_names, components, mass_amounts, models):    
    os.mkdir(_nm)
    create_symlinks(_nm, files=["vertex","build", "werami",
                                "stx11ver.dat", "stx11_solution_model.dat"])
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
        ow, ew = q.werami()     
  
    os.chdir("../")

# %%
for nm in project_names:
    ass = Assembler(nm, subdivisions)
    parts, joined, stitched = ass.assemble()
    ass.export_tab()
