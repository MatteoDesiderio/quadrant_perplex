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
import json

def add_newlines(inputs):
    check = lambda i : i[-2:] != "\n"
    return [i + "\n" for i in inputs if check(i)]

class ParamReader:
    
    @staticmethod
    def read(path):
        # each line in the file is an element of the list of type str
        lines = np.loadtxt(path, dtype="str", delimiter="/n", comments=None)
        iscomment = lambda x : x.replace(" ", "")[0] == "#"
        names = [n for n in lines if iscomment(n)]
        names = [n.replace(" ", "").replace("#", "") for n in names]
        variables = [v for v in lines if not iscomment(v)]


        str2list = lambda x : x.replace(" ", "").split(",")
        dictionary = {n:str2list(v) for n,v in zip(names, variables)}
        for key in dictionary:
            if not("mass" in key):
                dictionary[key] += [""]

        for key in ["database", "solution_model"]:
            dictionary[key] = dictionary[key][0]

        return dictionary

        """
        with open(path, "r") as file:
            lines = file.readlines()
            for j, line in enumerate(lines):
                print()
                for i, var in enumerate(names):
                    print("read", var)
                    if var in line:
                        # need to eliminate h
                        val = lines[j+1].replace(" ", "").split(",")[:-1]

                            # need to put a blank space 
                            if not("mass" in var):
                                variables[i] = val + [""]
                            else:
                                variables[i] = val

                        print(val)
                    else:
                        pass
        return variables
        """
class Quadrant:
    """
    A class to represent a project in a given subset of the PT space.


    Attributes
    ----------
    name : str
        name of the perplex project, e.g. 'Basalt'
    database : str
    
    perplex_option_file : str

    name : str
        name of the perplex project, e.g. 'Basalt'
    database : str
    
    perplex_option_file : str

    name : str
        name of the perplex project, e.g. 'Basalt'
    database : str
    
    perplex_option_file : str

    name : str
        name of the perplex project, e.g. 'Basalt'
    database : str
    
    perplex_option_file : str

    name : str
        name of the perplex project, e.g. 'Basalt'
    database : str
    
    perplex_option_file : str

    name : str
        name of the perplex project, e.g. 'Basalt'
    database : str
    
    perplex_option_file : str


    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
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
        self.stdout = {"build":"", "vertex":"", "werami":""}
        
    def build(self):
        # TODO leave out $VAR etc because no longer necessary, RETVRN
        # the $var is necessary because the self.name of the dat file is passed
        # into it when spawning the subprocess
        build = Automator("build", self.inputs, self.name)
        build.automate()
    
    def vertex(self):
        vertex = Automator("vertex", [self.name])
        vertex.automate()
    
    def werami(self):
        """
        For now it's hardcoded to do one thing (rho, K and G for
        the whole system, in the default PT range and with the
        1st grid_level resolution used, i.e. the lowest of the refine stage'
        """
        inputs = ["2", "38", "1", "2", "10", "11", "0", "n", "1", "0"]
        # inputs = ["2", "38", "1", "2", "10", "11", "0", "n", "4", "y", "0"]
        inputs = [self.name] + inputs
        werami = Automator("werami", inputs)
        werami.automate()
    
class Automator:
    """
    A class to automate any Perplex program
    
    Attributes
    -------
    perplex_program  :  str
        The desired perplex program e.g. VERTEX
    inputs :  list
        The list of desired inputs (of type str) for the perplex_program 
    e.g. for VERTEX : ["name_of_project"]
    
    """
    def __init__(self, perplex_program=None, inputs=[], name=""):
        """
        Initialize Automator class with the desired perplex program and 
        sequence of relevant inputs
        
        Attributes
        -------
        perplex_program  :  str
            The desired perplex program e.g. VERTEX
        inputs :  list
            The sequential list of desired inputs (of type str) for the 
            perplex_program, e.g. for VERTEX : ["name_of_project"]. Note that
            it must include "empty" inputs, if any are required by the program
            at any point in the sequence (i.e., some times a program may ask 
            a return to signify the end of a list of values. This can be done
            by putting an empty character "" after that set of values).
            
        Methods
        -------
        automate
            Method to automate the program stored in self.perplex_program, with 
            the desired sequential list of inputs stored in self.inputs.

        """
        if perplex_program[:2] != "./":
            perplex_program = "./" + perplex_program
        self.perplex_program = perplex_program
        
        self.inputs = add_newlines(inputs)
        self.name = name
        
    def automate(self):
        """
        Method to automate the program stored in self.perplex_program, with the
        desired sequential list of inputs stored in self.inputs.

        Returns
        -------
        stdout : str
            stdout of the program.
        stderr : str
            stderr of the program.

        """
        # let subprocess know I want a script
        header = "#!/bin/sh" 
        inputs = "".join(self.inputs) # join in one line
        inputs = inputs.replace("\n", "\\n") # need escape
        command = ["printf '" + inputs + "' | " + self.perplex_program]
        title = self.perplex_program + ".sh"
        np.savetxt(title, command, header=header, fmt="%s",
                   comments="")
        # now I created a shell script, go take a look at it
        # permission to execute, sir
        st = os.stat(title)
        os.chmod(title, st.st_mode | 0o0111)

        
class Assembler:
    """
    A class to assemble the WERAMI outputs, assuming that they each represent
    the properties on a quadrant of the PT space and that these quadrant are
    contiguous, and are ordered consistently, and share the same values along 
    their mutual boundaries. Like this, for 4 quadrants of 3x3 values:
    0 . x x . 1
    . . x x . .
    x x x x x x             The "x"s represent the numbers 
    x x x x x x             The numbers represent the order
    . . x x . .
    2 . x x . 3
    A scheme like this is granted when the quadrants are generated by the
    function "create_squares" in the module "utils"
    
    Attributes
    -------
    path  :  str
        The name of the project, e.g. "Basalt"
    subdivisions :  int
        The number of quadrants along each axis. 
        
    ntot : int
        The total number of quadrants, ntot = subdivisions**2
    tabfiles : list
        The list of tab file names generated by PYWERAMI. This is generated on 
        initialization based on "self.path" and "self.ntot".
    P_info : list
        List of strings of independent variable info extracted from the tab of 
        a single quadrant. They are min_var, step_var, nsteps_var.
        
    T_info : list
        List of strings of independent variable info extracted from the tab of 
        a single quadrant. They are min_var, step_var, nsteps_var.
        
    header : list
        Each element of the list is a line of the header extracrted from a 
        the tab file of a single quadrant. The values of nsteps_P and nsteps_T
        are changed to the final value of the assembled tab files when running 
        method "assemble" (7th and 11th line). The name of the tab (2nd line)
        is changed to "path_1.tab" (e.g. Basalt_1.tab) when running the 
        method "export_tab".
        
    self.stitched : numpy.ndarray
        The array containing the generated tab file assembled from the 
        quadrants.

    Methods
    -------
    assemble
        Method to collect the WERAMI output for all the quadrants and stitch 
        them together into one neat tab file 
    join
        Helper method for assemble. Succintly, puts the quadrants next to each 
        other.
    stitch
        Helper method for assemble. Succintly, eliminates the seams between the 
        quadrants.
     export_tab
         Method to export "self.stitched" into a tab file with the correct 
         header. 
    """
    
    def __init__(self, path, subdivisions):
        """
        Initialize the Assembler class
        
        Parameters
        -------
        path  :  str
            The name of the project, e.g. "Basalt"
        subdivisions :  int
            The number of quadrants along each axis. 
            n_quadrants = subdivisions ** 2
        """
        path = path if path[-1] == "/" else path + "/"
        self.path = path 
        self.subdivisions = subdivisions
        self.ntot = subdivisions**2
        self.tabfiles = [path + r"quadrant%i/"%i + path[:-1] + 
                         "_quadrant%i"%i + "_1.tab" for i in range(self.ntot)]
        self.P_info = []
        self.T_info = []
        self.header = []
        self.stitched = None
        
    def assemble(self):
        """
        Method to collect the WERAMI output for all the quadrants and stitch 
        them together into one neat tab file 

        Returns
        -------
        parts : list
            A list of numpy.ndarrays. Each array is the tab file of each
            quadrant.
        joined : numpy.ndarray
            The array is the tab file generated by putting the quadrants next
            to each other. 
            joined.shape = (steps_P*subdivisions)x(steps_T*subdivisions)
        stitched : numpy.ndarray
            The array is the tab file generated by putting the quadrants next
            to each other and eliminating the seams. 
            stitched.shape = (steps_P*subdivisions-1)x(steps_T*subdivisions-1)
        """
        parts = []
        header = ""
        for i, tab in enumerate(self.tabfiles):
            print(i)
            if i == 0:
                min_T, step_T, nsteps_T = np.loadtxt(tab, skiprows=4, 
                                                     max_rows=3)
                min_P, step_P, nsteps_P = np.loadtxt(tab, skiprows=8, 
                                                     max_rows=3)
                header = np.loadtxt(tab, max_rows=12, dtype=str, 
                                    delimiter="\n")
                col_names = np.loadtxt(tab, skiprows=12, max_rows=1, dtype=str, 
                                    delimiter="\n")
                self.P_info =  min_P, step_P, nsteps_P
                self.T_info =  min_T, step_T, nsteps_T
                self.col_names = col_names
                self.header = np.hstack([header, col_names])          
            part = np.loadtxt(tab, skiprows=13)
            parts.append(part)
            
        joined = self.join(parts)
        stitched = self.stitch(joined)
        self.stitched = stitched
        return parts, joined, stitched
    
    def join(self, parts):
        """
        Helper method for assemble. 
        
        A) Join the variables
            1) Take the tab file from a quadrant
            2) Take the columns of the tab file separately
            3) Reshape them into an actual square in the PT space
            4) Go to next quadrant and repeat
            5) Join the squares 
        B) Create the tab file from joined quadrants
            1) Take the reshaped coumns and flatten them into a column vector
            2) Put these vectors side by side

        Parameters
        ----------
        parts : list
            A list of numpy.ndarrays. Each array is the tab file of each
            quadrant.

        Returns
        -------
        numpy.ndarray
            The tab file generated by putting the quadrants next to each other. 
        """
        col_list = ([], [], [], [], [])
        for part in parts:
            # extract the columns of the tab file
            c1, c2, c3, c4, c5 = part.T
            cols = [c1, c2, c3, c4, c5]
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
        """
        Helper method for assemble. Succintly, eliminates the seams between the 
        quadrants.
        
        Parameters
        -------
        joined : numpy.ndarray
            The array is the tab file generated by putting the quadrants next
            to each other. 
            joined.shape = (steps_P*subdivisions)x(steps_T*subdivisions)
            
        Returns
        -------
        numpy.ndarray
            The tab file generated by putting the quadrants next
            to each other and eliminating the seams. 
            stitched.shape = (steps_P*subdivisions-1)x(steps_T*subdivisions-1)
        
        """
        # extract the columns of the tab file
        c1, c2, c3, c4, c5 = joined.T
        cols = [c1, c2, c3, c4, c5]
        # define resolution along y, x (P, T space) (nrows, ncols respectively)
        ny = int(self.P_info[-1])
        nx = int(self.T_info[-1])
        # if all is joined without deleting duplicates, the effective res is:
        nrows = ny * self.subdivisions
        ncols = nx * self.subdivisions
        # if PT space is split in quadrants, this helps locate their borders
        multipliers = np.r_[range(1, self.subdivisions, 1)]
        # handle the case when only 4 quadrants were created 
        if len(multipliers) == 1:
            multipliers = 1
        # the actual indices of the columns, rows to be deleted 
        del_rows = int(ny) * multipliers 
        del_cols = int(nx) * multipliers 
        
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
        
        # has new resolution now
        newx = (nx * self.subdivisions - (self.subdivisions - 1))
        newy = (ny * self.subdivisions - (self.subdivisions - 1))
        self.header[6] = self.header[6].replace("%i" % nx, "%i" % newx)
        self.header[10] = self.header[10].replace("%i" % ny, "%i" % newy)
        
        return np.column_stack(stitched_cols)
            
    def export_tab(self):
        """
        Method to export "self.stitched" into a tab file with the correct 
        header.
        """
        title = self.path[:-1] + "_1.tab"
        name = self.path + title
        self.header[1] =  title
        header = '\n'.join(self.header)
        # TODO 1: correct numerical format (check original tab files)
        # IF num >= 1E6 save w scientific notation 0.123456 E+7
        # ELSE %1.2f
        np.savetxt(name, self.stitched, header=header, comments="")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        