#!/bin/bash

choice=$1
argument1=$2
argument2=$3
argument3=$4
argument4=$5

if [ "$choice" == "print" ]
then
	python iproute.py print > route.txt

elif [ "$choice" == "create" ]
then
	python iproute.py create $argument1 $argument2 $argument3 > route.txt

elif [ "$choice" == "update" ]
then 
        python iproute.py update $argument1 $argument2 $argument3 $argument4 > route.txt
elif [ "$choice" == "delete" ]
then 
        python iproute.py delete $argument1 > route.txt
fi
