#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 12:45:25 2022

@author: matteo
"""
import os
import numpy as np
from quadralizer import Quadrant

def create_squares(Trange=[300, 4000], Prange=[1, 1400000], subdivisions=2):
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
    for _ppair in P_pairs:
        ppair = "%.1f"%_ppair[0], "%.1f"%_ppair[1] 
        for _tpair in T_pairs:
            tpair = "%.1f"%_tpair[0], "%.1f"%_tpair[1] 
            squares.append([tpair, ppair])
    
    return squares

def create_symlinks(_nm, files=["vertex","build","werami","stx11ver.dat",
                                "stx11_solution_model.dat"]):
    cwd = os.getcwd() + "/"
    for f in files:
        os.symlink(cwd + f, cwd + _nm + "/" + f)
   

def create_paths(project_names):
    for _nm in project_names:  
        # create directory to store results
        os.mkdir(_nm)    
        # need to symlink the programs and the thermodynamic databases
        create_symlinks(_nm, files=["vertex","build", "werami", 
                                    "stx11ver.dat", "stx11_solution_model.dat", 
                                    "perplex_option.dat"])

def initialize_quadrants(project_names, components, mass_amounts, models, 
                         squares):
    proj_quadrants = [] 
    for _nm, c, a, m in zip(project_names, components, mass_amounts, models):
        qs = []
        os.chdir(_nm)
        # loop over PT space subdivisions (squares)
        for isq, square in enumerate(squares):
            tmin, tmax = square[0]  
            pmin, pmax = square[1]
            nm = _nm + "_quadrant%i"%isq
            # Initialize the computation for the quadrant
            q = Quadrant(name=nm, components=c,
                         MinT=tmin, MaxT=tmax,
                         MinP=pmin, MaxP=pmax,   
                         amounts=a, models=m)
            qs.append(q)
        proj_quadrants.append(qs)
        os.chdir("../")
        return proj_quadrants
        
def parallelize(proj_quadrants, project_names, perplex_program):
    for nm, proj in zip(project_names, proj_quadrants):
        os.chdir(nm)

        processes = []
        for q in proj:
            proc = getattr(q ,perplex_program)()
            processes.append(proc)
        
        for p in processes:
            stdout, stderr = p.communicate()
            q.stdout[perplex_program].append(stdout)
            #p.stdin.close()
            
        os.chdir("../")





















