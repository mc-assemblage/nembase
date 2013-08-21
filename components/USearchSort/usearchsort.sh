#!/bin/bash
. ./functions.sh


fastafile=$( getinput "fastafile")
sortedfile=$( getoutput "sortedfile")


usearch -sortbylength $fastafile -output $sortedfile


