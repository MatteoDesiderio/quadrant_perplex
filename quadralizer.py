#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:20:52 2022

@author: matteo

classes
"""

import subprocess
import os
import glob
import numpy as np

check = lambda i : i[-2:] != "\n"

class Quadrant:
    """
    A class to build a project and save relevant files
    
    Parameters
    -------
    name  :  str
    The desired proj name, e.g. 'basalt'
    PMinMax : list
    
    TMinMax : list
    
    Solutions : list
    
    Others_1 : list
    
    Others_2 : list
    
    S
    """
    def __init__(self,
                 name="name", 
                 database="stx11ver.dat", 
                 perplex_option_file="",
                 transform="n",
                 computational_mode="2",
                 saturated="n",
                 add_independent_variables="n",
                 components=["NA2O","MGO","AL2O3",
                             "SIO2","CAO","FEO"],          # <-------
                 geotherm="n",
                 xaxis="2",
                 MinT="",   # <-------
                 MaxT="",   # <-------
                 MinP="",   # <-------
                 MaxP="",   # <-------
                 by_mass="y", 
                 amounts=["1", "1", "1",
                          "1", "1", "1"],    # <-------
                 print_file="y",
                 exclude_endmembers="n",
                 include_solution_models="y",
                 solution_model="stx11_solution_model.dat",
                 models=["C2/c","Wus","Pv",
                         "O","Wad","Ring",
                         "Opx","Aki","Ppv"]):
        
        
        """
        Initialize Project class with the desired sequence of inputs for 
        automating BUILD and VERTEX
        
        Returns
        -------
        None.

        """
        
        self.name=name
        self.database=database
        self.perplex_option_file=perplex_option_file
        self.transform=transform
        self.computational_mode=computational_mode
        self.saturated=saturated
        self.add_independent_variables=add_independent_variables
        self.components=components
        self.geotherm=geotherm
        self.xaxis=xaxis
        self.MinT=MinT
        self.MaxT=MaxT
        self.MinP=MinP
        self.MaxP=MaxP
        self.by_mass=by_mass
        self.amounts=amounts
        self.print_file=print_file
        self.exclude_endmembers=exclude_endmembers
        self.include_solution_models=include_solution_models
        self.solution_model=solution_model
        self.models=models
        self.title=self.name
        
        inputs=[]
        for el in vars(self).values():
            if not isinstance(el, list):
                inputs.append(el)
            else:
                for sub_el in el:
                    inputs.append(sub_el)
        
        self.inputs = inputs
        self.bld_stdout = "Build Not done yet"
        self.bld_stderr = "Build Not done yet"
        
        self.vtx_stdout = "Vertex Not done yet"
        self.vtx_stderr = "Vertex Not done yet"
    
    def setUpPath(self):
        os.mkdir("./" + self.name)
    
    def build(self):
        build = Automator("build", self.inputs)
        stdout, stderr = build.automate()
        self.bld_stdout = stdout
        self.bld_stderr = stderr
        return (self.bld_stdout, self.bld_stderr)
        

    def create(self):
        #self.setUpPath()
        self.build()
        #os.rename("./" + self.name + ".dat",
        #          "./" + self.name + "/" + self.name + ".dat")
    
    def vertex(self):
        vertex = Automator( "vertex", [self.name])
        stdout, stderr = vertex.automate()
        self.vtx_stdout = stdout
        self.vtx_stderr = stderr
        return (self.vtx_stdout, self.vtx_stderr)
    
    def werami(self):
        """
        For now it's hardcoded to do one thing (rho, K and G for
        the whole system, in the default PT range and with the
        last grid_level resolution used, i.e. the highest'
        """
        
        inputs = ["2", "38", "1", "2", "10", "11", "0", "n", "4", "0"]
        inputs = [self.name] + inputs
        inputs = [i + "\n" for i in inputs if check(i)]
        werami = Automator( "werami", inputs)
        stdout, stderr = werami.automate()
        self.wtx_stdout = stdout
        self.wtx_stderr = stderr
        return (self.wtx_stdout, self.wtx_stderr)
    
class Automator:
    """
    A class to automate any Perplex program
    
    Parameters
    -------
    perplex_program  :  str
    The desired perplex program e.g. VERTEX
    inputs :  list
    The list of desired inputs (of type str) for the perplex_program 
    e.g. for VERTEX : "name_of_project"
    
    """
    def __init__(self, perplex_program=None, inputs=[]):
        """
        Initialize Automator class with the desired perplex program and 
        sequence of relevant inputs
        
        Returns
        -------
        None.

        """
        if perplex_program[:2] != "./":
            perplex_program = "./" + perplex_program
        self.perplex_program = perplex_program
        
        inputs = [i + "\n" for i in inputs if check(i)]
        
        self.inputs = inputs

    def automate(self):
        """
        

        Returns
        -------
        stdout : str
            stdout of the program.
        stderr : str
            stderr of the program.

        """
        process = subprocess.Popen([self.perplex_program],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   universal_newlines=True)

        for i in self.inputs:
            process.stdin.write(i)
        
        stdout, stderr = process.communicate()
        process.stdin.close()

        return stdout, stderr

class Assembler:
    def __init__(self, path, subdivisions):
        """
        
        """
        path = path if path[-1] == "/" else path + "/"
        self.path = path
        self.subdivisions = subdivisions
        self.ntot = subdivisions**2
        self.tabfiles = [path + path[:-1] + "_quadrant%i"%i + "_1.tab"
                         for i in range(self.ntot)]
        self.P_info = []
        self.T_info = []
        self.header = []
        self.stitched = None
        
    def assemble(self):
        parts = []
        header = ""
        for i, tab in enumerate(self.tabfiles):
            if i == 0:
                min_T, step_T, nsteps_T = np.loadtxt(tab, skiprows=4, max_rows=3)
                min_P, step_P, nsteps_P = np.loadtxt(tab, skiprows=8, max_rows=3)
                header = np.loadtxt(tab, max_rows=12, dtype=str, delimiter="\n")
                self.P_info =  min_P, step_P, nsteps_P
                self.T_info =  min_T, step_T, nsteps_T
                self.header = header                
            part = np.loadtxt(tab, skiprows=13)
            parts.append(part)
            
        joined = self.join(parts)
        stitched = self.stitch(joined)
        self.stitched = stitched
        return parts, joined, stitched
    
    def join(self, parts):
        col_list = ([], [], [], [], [], [])
        for part in parts:
            # extract the columns of the tab file
            c1, c2, c3, c4, c5, c6 = part.T
            cols = [c1, c2, c3, c4, c5, c6]
            for ic, c in enumerate(cols):
                col_list[ic].append(c)
        
        nrows = int(self.P_info[-1])
        ncols = int(self.T_info[-1])
        ind_ar = np.reshape(range(self.ntot), (self.subdivisions, 
                                               self.subdivisions))
        
        joined_col_list = []
        for cols in col_list:
            vert_chain = []
            for indices in ind_ar:
                hor_chain = []
                for i in indices:
                    rr = np.reshape(cols[i], (nrows, ncols))
                    hor_chain.append(rr)
                vert_chain.append(np.hstack(hor_chain))
            joined_col_list.append(np.vstack(vert_chain).flatten())
        
        return np.column_stack(joined_col_list)
        
    
    def stitch(self, joined):
        # extract the columns of the tab file
        c1, c2, c3, c4, c5, c6 = joined.T
        cols = [c1, c2, c3, c4, c5, c6]
        # define resolution along y, x (P, T space) (nrows, ncols respectively)
        ny = int(self.P_info[-1])
        nx = int(self.T_info[-1])
        # if all is joined without deleting duplicates, the effective res is:
        nrows = ny * self.subdivisions
        ncols = nx * self.subdivisions
        # if PT space is split in quadrants, this helps locate their borders
        multipliers = np.r_[range(1, self.subdivisions - 1, 1)]
        # handle the case when only 4 quadrants were created 
        if len(multipliers) == 0:
            multipliers = 1
        # the actual indices of the columns, rows to be deleted 
        del_rows = int(nx) * multipliers 
        del_cols = int(ny) * multipliers 
        
        stitched_cols = []
        # in this example, I have 4 grids (3x3) joined. x are the repeated 
        # elements that must be eliminated. 
        #    . . x x . .
        #    . . x x . .
        #    x x x x x x
        #    x x x x x x
        #    . . x x . .
        #    . . x x . .
        # The code below generates for each variable a matrix like this from 
        # the column of tab file. the th xs are deleted and then again every
        # everyhting is reshaped properly as a tab file
        for c in cols:
            r = np.reshape(c, (nrows, ncols))
            r_del = np.delete(np.delete(r, del_rows, 0), del_cols, 1)
            stitched_cols.append(r_del.flatten())
        self.header[11] = "%i"%(ny-1)
        self.header[7] = "%i"%(nx-1)
        return np.column_stack(stitched_cols)
            
    def export_tab(self):
        name = self.path + self.path[:-1] + "_1.tab"
        header = '\n'.join(self.header)
        # TODO 1: correct numerical format (check original tab files)
        # IF num >= 1E6 save w scientific notation 0.123456 E+7
        # ELSE %1.2f
        np.savetxt(name, self.stitched, header=header, comments="")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        