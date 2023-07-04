#!/usr/bin/env bash
# stagpy_movies.sh

. ~/.bashrc
#source ~/StagPy/.venv_dev/bin/activate

_vertex() {
	name=$1
    start=$2
    finish=$3
	for isq in $(seq $start 1 $finish)
	do
		pth="$name""$isq"
		cd $pth
		./vertex.sh > OUTPUT_VERTEX.txt
		cd ../..	
	done
}

_werami() {
	name=$1
    start=$2
    finish=$3
	for isq in $(seq $start 1 $finish)
	do
		pth="$name""$isq"
		cd $pth
		./werami.sh > OUTPUT_WERAMI.txt
		cd ../..
	done
}


_build() {
	name=$1
    start=$2
    finish=$3
	for isq in $(seq $start 1 $finish)
	do
		pth="$name""$isq"
		cd $pth
		./build.sh > OUTPUT_BUILD.txt
		cd ../..
	done
}

fun() {
	program=$1
    name="$2"/quadrant
    start=$3
    finish=$4
    case $program in
    	vertex) _vertex $name $start $finish ;;
		werami) _werami $name $start $finish ;;
		build)  _build  $name $start $finish ;;	
	esac
		
    # outn=~/movies_output_/$(basename $model)/$field/  
}

# this gets the max number of processes for the user
max_num_processes=$(ulimit -u)
# An arbitrary limiting factor so that there are some free processes
# in case I want to run something else
limiting_factor=4096
#num_processes=$((max_num_processes/limiting_factor))

program=$1
name=$2
num_processes=$3

#
ntot=$(ls -d $name/q*/ | wc -l) 

# let's avoid the case when Nproc > Nsnaps
num_processes=$((num_processes<ntot ? num_processes : ntot))
part=$((ntot/num_processes))
#echo ntot $ntot part $part
#echo $model/+im/$field/stagpy_field_

for start in $(seq 0 $part $(($ntot-1)))
do
    finish=$(($start+$part-1))

    if [ $finish -gt $start ]
    then
	    if [ $finish -gt $(($ntot-1)) ]
	    then
	        finish=$(($ntot-1))
	    fi
    	((i=i%num_processes)); ((i++==0)) && wait
    	fun "$program" "$name" "$start" "$finish" &
	fi
done

