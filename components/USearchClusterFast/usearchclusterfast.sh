#!/bin/bash
. ./functions.sh


fastafile=$( getinput "fastafile")
identity=$( getparameter "id")
resultsuc=$( getoutput "resultsuc")
resultsfa=$( getoutput "resultsfa")


#usearch will generate an error if $fastafile is empty so check that it is not
if [ -n "$fastafile" ] && [ -s "$fastafile" ]
then
	usearch -cluster_fast $fastafile -id $identity -uc $resultsuc -centroids $resultsfa
else
	#the input file is empty, create an empty output file so anduril doesn't complain
	touch $resultsuc
	touch $resultsfa
fi


