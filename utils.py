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
   

def create_paths(project_name, perplex_version, subdivisions, 
                 database="stx11ver.dat", solution_model="stx11_solution_model.dat"):

    nq = subdivisions ** 2
    programs = [f"{perplex_version}/{prog}" 
                for prog in ["vertex","build", "werami"]]
    thermo_database = [f"{perplex_version}/{database}",
                       f"{perplex_version}/{solution_model}"]

    os.mkdir(project_name)
    for isq in range(nq):
        # create directory to store results
        q_nm = "quadrant%i"%isq
        os.mkdir(project_name + "/" + q_nm)
        # need to symlink the programs and the thermodynamic databases

        files = programs + thermo_database + [f"{perplex_version}/perplex_option.dat"]
        create_symlinks(project_name + "/" + q_nm, files)

def initialize_quadrants(project_name, database, solution_model,
                         components, mass_amounts, models,
                         squares):
    proj_quadrants = [] 

    os.chdir(project_name)
    # loop over PT space subdivisions (squares)
    for isq, square in enumerate(squares):
        os.chdir("quadrant%i"%isq)
        tmin, tmax = square[0]  
        pmin, pmax = square[1]
        nm = project_name + "_quadrant%i"%isq
        # Initialize the computation for the quadrant
        q = Quadrant(name=nm, components=components,
                     MinT=tmin, MaxT=tmax, 
                     MinP=pmin, MaxP=pmax, 
                     amounts=mass_amounts, models=models, 
                     database=database, solution_model=solution_model)
        proj_quadrants.append(q)
        os.chdir("../")
    os.chdir("../")
    return proj_quadrants
        
def prepare(proj_quadrants, project_name, perplex_program):
    print("Now creating the", perplex_program, 
          "stdin for",  project_name)
    os.chdir(project_name)
    
    for isq, q in enumerate(proj_quadrants):
        os.chdir("quadrant%i"%isq)
        getattr(q, perplex_program)()
        os.chdir("../")

    os.chdir("../")
    return proj_quadrants





















