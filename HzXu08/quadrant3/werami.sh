#!/bin/sh
var=$@
printf $var'\n2\n38\n1\n2\n10\n11\n0\nn\n1\n0\n' | ./werami ; sleep 0.1