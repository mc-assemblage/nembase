#!/bin/bash
. ./functions.sh


fastafile=$( getinput "fastafile")
identity=$( getparameter "id")
resultsuc=$( getoutput "resultsuc")
resultsfa=$( getoutput "resultsfa")


usearch -cluster_fast $fastafile -id $identity -uc $resultsuc -centroids $resultsfa


