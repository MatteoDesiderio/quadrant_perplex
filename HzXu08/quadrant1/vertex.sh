#!/bin/sh
var=$@
printf $var'\n' | ./vertex ; sleep 0.1
