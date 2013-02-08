#!/bin/bash
. ./functions.sh


vectorfile=$( getinput "vector")
fastqfile=$( getinput "fastqfile")
ssaha2out=$( getoutput "ssaha2out")
mode=$( getparameter "rtype")


echo $fastqfile >> $logfile
echo $vectorfile >> $logfile

if [ -n "$vectorfile" ] && [ -s "$vectorfile" ]
then
	ssaha2 -output ssaha2 -rtype $mode $fastqfile $vectorfile > $ssaha2out
else
	touch $ssaha2out
fi


