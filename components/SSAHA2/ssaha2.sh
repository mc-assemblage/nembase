#!/bin/bash
. ./functions.sh


vectorfile=$( getinput "vector")
inputfile=$( getinput "inputfile")
ssaha2out=$( getoutput "ssaha2out")
mode=$( getparameter "rtype")


echo $inputfile >> $logfile
echo $vectorfile >> $logfile

if [ -n "$vectorfile" ] && [ -s "$vectorfile" ]
then
	ssaha2 -output ssaha2 -rtype $mode $inputfile $vectorfile > $ssaha2out
elif [ -n "$vectorfile" ]
then
	# custom vector file is empty, just create an empty output file
	touch $ssaha2out
else
	# use the default vector file (downloaded from NCBI UniVec database)
	ssaha2 -output ssaha2 -rtype $mode $inputfile UniVec > $ssaha2out
fi


