#!/bin/bash
. ./functions.sh


fastafile=$( getinput "fastafile")
sortedfile=$( getoutput "sortedfile")


#usearch will generate an error if $fastafile is empty so check that it is not
if [ -n "$fastafile" ] && [ -s "$fastafile" ]
then
	usearch -sortbylength $fastafile -output $sortedfile
else
	#the input file is empty, create an empty output file so anduril doesn't complain
	touch $sortedfile
fi


