#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:20:52 2022

@author: matteo

classes
"""

import subprocess
import os

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
        self.stdout = "Not done yet"
        self.stderr = "Not done yet"
        
        self.vtx_stdout = ""
        self.vtx_stderr = ""
    
    def setUpPath(self):
        os.mkdir("./" + self.name)
    
    def build(self):
        build = Automator( "build", self.inputs)
        stdout, stderr = build.automate()
        self.bld_stdout = stdout
        self.bld_stderr = stderr
        return (stdout, stderr)
        

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
        return (stdout, stderr)
    
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
        