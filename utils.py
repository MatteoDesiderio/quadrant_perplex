#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 12:45:25 2022

@author: matteo
"""
import os
import numpy as np

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
   