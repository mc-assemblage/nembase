#!/bin/bash
. ./functions.sh



kmer=$( getparameter "kmer")
nhashes=$( getparameter "nhashes")
minhashsize=$( getparameter "minhashsize")
cutoff=$( getparameter "cutoff")

inputfile=$( getinput "inputfile")
outputfile=$( getoutput "outputfile")


normalize-by-median.py -k $kmer -N $nhashes -x $minhashsize -C $cutoff $inputfile -R $outputfile


