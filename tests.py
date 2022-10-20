#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:12:35 2022

@author: matteo
"""

import unittest
from quadralizer import Automator, Project


class TestAutomator(unittest.TestCase):
    def test_setUp(self):
        perplex_program = "vertex"
        inputs = ["Anna_Fugazzi"]
        vertex = Automator(perplex_program, inputs)
        result = vertex.perplex_program
        self.assertEqual(result, "./vertex")
        result = vertex.inputs
        self.assertEqual(result, ["Anna_Fugazzi\n"])
        
    def test_NotFound(self):
        perplex_program = "vertex"
        inputs = ["Anna_Fugazzi", ""] # the second itemq is to answer "no"
        vertex = Automator(perplex_program, inputs)
        stdout, stderr = vertex.automate()
        #print(stdout)
        #print(stderr)
        expected = "Enter a different project name (y/n)?\n"
        self.assertEqual(stdout[-38:], expected)
        self.assertEqual(stderr, '')
    
    def test_Found(self):
        perplex_program = "vertex"
        inputs = ["basalt"] 
        vertex = Automator(perplex_program, inputs)
        stdout, stderr = vertex.automate()
        expected = "Endofjob:basalt"
        s = stdout.replace("\n", "").replace("-", "").replace(" ", "")[-15:]
        self.assertEqual(s, expected)
        # print(stdout)
        # print(stderr)
        
    def test_Project(self): 
        project = Project()        
        
if __name__ == "__main__":
    unittest.main()
