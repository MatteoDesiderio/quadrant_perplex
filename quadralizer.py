#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:20:52 2022

@author: matteo

classes
"""

import subprocess

class Automator:
    """
    A class to automate any (?) Perplex program
    
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
        
        f = lambda i : i[-2:] != "\n"
        inputs = [i + "\n" for i in inputs if f(i)]
        
        self.inputs = inputs

    def automate(self):
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
        