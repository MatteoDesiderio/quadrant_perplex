#!/bin/sh
var=$@
printf $var'\nstx11ver.dat\n\nn\n2\nn\nn\nCAO\nFEO\nMGO\nAL2O3\nSIO2\nNA2O\n\nn\n2\n300.0\n2150.0\n700000.5\n1400000.0\ny\n0.89\n8.61\n45.72\n1.33\n43.45\n0.0\ny\nn\ny\nstx11_solution_model.dat\nPl\nSp\nO\nWad\nRing\nOpx\nCpx\nPv\nPpv\nCF\nC2/c\nWus\nAki\nGt\n\n'$var'\n' | ./build ; sleep 0.1