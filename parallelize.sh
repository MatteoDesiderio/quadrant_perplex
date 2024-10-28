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

if [ $program == '--help' ]
then
	echo 'Usage: program_name [build/vertex/werami] name_of_project number_of_processes [e.g. 8]'
fi


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
# based on 
# https://unix.stackexchange.com/questions/103920/parallelize-a-bash-for-loop/436713#436713

# start a job at each iteration of the loop
for path in $name/q*/
do 
	# if the program is vertex the computation is very long
	# it makes sense to check first if it's been done already
	# if not, then we start the job
	if [[ $program == "vertex" ]]
	then
		capitalized=$(echo ${program^^})
		grep "End of job" $path*OUTPUT*$capitalized*txt > /dev/null
		a=$?
		if [[ $a > 0 ]]
		then 
			# echo $path
			wrapper $program $path &
		fi
	else
		wrapper $program $path &
	fi
		
	# allow to execute only up to $num_processes jobs in parallel
    if [[ $(jobs -r -p | wc -l) -ge $num_processes ]]; then
        # wait with the option -n waits for any job to throw an exit status
        # before advancing the loop to the next step
        wait -n
    fi
    # as soon a slot is freed, the loop will advance and a new job will be 
    # started to fill the empty slot

done
# at the end of the loop, there are no more jobs to be started 
# but there'll be pending jobs for sure and we need them to finish before 
# moving on 

wait

echo "all done"
# -------------------------------------------------------------------------------
