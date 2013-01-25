#!/bin/bash
. ./functions.sh


kmersize=$( getparameter "kmersize")
fastqfile=$( getinput "fastqfile")
fastqcdir=$( getoutput "fastqcdir")


if [ ! -d $fastqcdir ]
then
	mkdir $fastqcdir
fi

fastqc -o $fastqcdir -f fastq -k kmersize $fastqfile


