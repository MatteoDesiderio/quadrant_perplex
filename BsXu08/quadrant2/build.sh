#!/bin/sh
var=$@
printf $var'\nstx11ver.dat\n\nn\n2\nn\nn\nCAO\nFEO\nMGO\nAL2O3\nSIO2\nNA2O\n\nn\n2\n300.0\n2150.0\n700000.5\n1400000.0\ny\n12.61\n8.22\n9.76\n16.84\n50.39\n2.19\ny\nn\ny\nstx11_solution_model.dat\nPl\nSp\nO\nWad\nRing\nOpx\nCpx\nPv\nPpv\nCF\nC2/c\nWus\nAki\nGt\n\n'$var'\n' | ./build ; sleep 0.1
