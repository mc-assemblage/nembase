#!/bin/bash
. ./functions.sh



kmersize=$( getparameter "kmersize")
nhashes=$( getparameter "nhashes")
minhashsize=$( getparameter "minhashsize")
cutoff=$( getparameter "cutoff")

inputfile=$( getinput "inputfile")
outputfile=$( getoutput "outputfile")


normalize-by-median.py --ksize $kmersize -N $nhashes -x $minhashsize -C $cutoff $inputfile -R $outputfile


