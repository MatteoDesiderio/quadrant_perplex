#!/usr/bin/env bash

. ~/.bashrc

# functions ---------------------------------------------------------------------
_vertex() {
	pth=$1
	cd $pth
	./vertex.sh > OUTPUT_VERTEX.txt
	cd ../..	
}

_werami() {
	pth=$1
	cd $pth
	./werami.sh > OUTPUT_WERAMI.txt
	cd ../..
}

_build() {
	pth=$1
	cd $pth
	./build.sh > OUTPUT_BUILD.txt
	cd ../..
}

wrapper() {
	program=$1
    name=$2

    case $program in
    	vertex) _vertex $2 ;;
		werami) _werami $2 ;;
		build)  _build  $2 ;;	
	esac	
}
# -------------------------------------------------------------------------------

# arguments ---------------------------------------------------------------------
program=$1 # name of the program you want to parallelize: build/vertex/werami
name=$2	   								   # name of the project (the folder) 
num_processes=$3 						   # number of the parallel jobs requested
# -------------------------------------------------------------------------------

# operations --------------------------------------------------------------------
# this gets the max number of processors on the machine
max_num_processes=$(nproc)
# the total number of tasks is the number of quadrants
ntot=$(ls -d $name/q*/ | wc -l) 
# let's avoid the case when Nproc > Nsnaps
num_processes=$((num_processes<ntot ? num_processes : ntot))
num_processes=$((num_processes<max_num_processes ? num_processes : max_num_processes))
# let's count how many parts
parts=$((ntot/num_processes))
# -------------------------------------------------------------------------------

# print info --------------------------------------------------------------------
echo directory $name
echo Requested num of processes: $3
echo Actual num of processes: $num_processes 
echo Max num of processors available: $max_num_processes
echo Total number of tasks $ntot
echo Computation divided into $parts parts 
# -------------------------------------------------------------------------------

# main loop ---------------------------------------------------------------------
for path in $name/q*/
do 
	((i=i%num_processes)); ((i++==0)) && wait
	wrapper $program $path &
done
# -------------------------------------------------------------------------------

